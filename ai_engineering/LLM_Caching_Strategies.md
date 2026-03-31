# Skill: LLM Caching Strategies

## Purpose
To reduce API costs and latency by caching LLM responses and avoiding redundant calls for identical or similar prompts.

## When to Use
- When users frequently ask similar questions
- When implementing RAG systems with recurring queries
- When building applications with repetitive patterns
- When optimizing for cost reduction

## Procedure

### 1. Simple Exact Match Caching
Cache responses based on exact prompt matches.

```python
import hashlib
import json
from functools import wraps
from openai import OpenAI

client = OpenAI()

# Simple in-memory cache
response_cache = {}

def cache_key(prompt, model, temperature=0):
    """Generate a unique cache key."""
    content = f"{model}:{temperature}:{prompt}"
    return hashlib.sha256(content.encode()).hexdigest()

def cached_completion(prompt, model="gpt-4", temperature=0):
    """Get completion with caching."""
    key = cache_key(prompt, model, temperature)
    
    if key in response_cache:
        print("Cache hit!")
        return response_cache[key]
    
    print("Cache miss - calling API...")
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature
    )
    
    result = response.choices[0].message.content
    response_cache[key] = result
    return result
```

### 2. Semantic Caching with Embeddings
Cache responses based on semantic similarity.

```python
import numpy as np
from sentence_transformers import SentenceTransformer

class SemanticCache:
    def __init__(self, similarity_threshold=0.85):
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        self.prompts = []
        self.responses = []
        self.embeddings = []
        self.threshold = similarity_threshold
    
    def get(self, prompt):
        """Try to get a cached response based on semantic similarity."""
        if not self.prompts:
            return None
        
        # Embed the query prompt
        query_embedding = self.embedder.encode([prompt])[0]
        
        # Calculate similarities with cached prompts
        cached_embeddings = np.array(self.embeddings)
        similarities = np.dot(cached_embeddings, query_embedding) / (
            np.linalg.norm(cached_embeddings, axis=1) * np.linalg.norm(query_embedding)
        )
        
        # Find the most similar cached prompt
        max_idx = np.argmax(similarities)
        max_similarity = similarities[max_idx]
        
        if max_similarity >= self.threshold:
            print(f"Semantic cache hit! Similarity: {max_similarity:.3f}")
            return self.responses[max_idx]
        
        print(f"No semantic match found. Max similarity: {max_similarity:.3f}")
        return None
    
    def set(self, prompt, response):
        """Store a new prompt-response pair."""
        self.prompts.append(prompt)
        self.responses.append(response)
        self.embeddings.append(self.embedder.encode([prompt])[0])

# Usage
semantic_cache = SemanticCache(similarity_threshold=0.90)

def get_response_with_semantic_cache(prompt):
    # Check cache first
    cached = semantic_cache.get(prompt)
    if cached:
        return cached
    
    # Call API and cache the result
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    result = response.choices[0].message.content
    
    semantic_cache.set(prompt, result)
    return result
```

### 3. Persistent Caching with Redis
Store cache entries in Redis for persistence across restarts.

```python
import redis
import pickle
import hashlib

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def redis_cache_key(prompt, model="gpt-4"):
    """Generate Redis cache key."""
    content = f"llm_cache:{model}:{hashlib.sha256(prompt.encode()).hexdigest()}"
    return content

def get_with_redis_cache(prompt, model="gpt-4", expire_hours=24):
    """Get response with Redis caching."""
    key = redis_cache_key(prompt, model)
    
    # Try to get from Redis
    cached = redis_client.get(key)
    if cached:
        print("Redis cache hit!")
        return pickle.loads(cached)
    
    print("Redis cache miss - calling API...")
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    result = response.choices[0].message.content
    
    # Store in Redis with expiration
    redis_client.setex(key, expire_hours * 3600, pickle.dumps(result))
    return result
```

### 4. Hierarchical Caching
Combine multiple caching strategies for optimal performance.

```python
class HierarchicalCache:
    def __init__(self):
        self.memory_cache = {}  # L1: In-memory cache
        self.semantic_cache = SemanticCache()  # L2: Semantic cache
        self.redis_client = redis.Redis()  # L3: Persistent cache
    
    def get(self, prompt, model="gpt-4"):
        # Check L1: Exact match in memory
        key = cache_key(prompt, model)
        if key in self.memory_cache:
            return self.memory_cache[key]
        
        # Check L2: Semantic match
        semantic_result = self.semantic_cache.get(prompt)
        if semantic_result:
            self.memory_cache[key] = semantic_result
            return semantic_result
        
        # Check L3: Redis persistent cache
        redis_key = redis_cache_key(prompt, model)
        redis_result = self.redis_client.get(redis_key)
        if redis_result:
            result = pickle.loads(redis_result)
            self.memory_cache[key] = result
            self.semantic_cache.set(prompt, result)
            return result
        
        # Cache miss - call API
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        result = response.choices[0].message.content
        
        # Store at all levels
        self.memory_cache[key] = result
        self.semantic_cache.set(prompt, result)
        self.redis_client.setex(redis_key, 86400, pickle.dumps(result))
        
        return result

# Usage
hierarchical_cache = HierarchicalCache()
response = hierarchical_cache.get("Explain quantum computing")
```

### 5. Cache Statistics and Monitoring
Track cache performance to optimize strategies.

```python
from collections import defaultdict

class CacheWithStats:
    def __init__(self):
        self.cache = {}
        self.stats = defaultdict(int)
    
    def get(self, key):
        self.stats['total_requests'] += 1
        
        if key in self.cache:
            self.stats['cache_hits'] += 1
            self.stats['memory_cache_hits'] += 1
            return self.cache[key]
        
        self.stats['cache_misses'] += 1
        return None
    
    def set(self, key, value):
        self.cache[key] = value
        self.stats['items_cached'] += 1
    
    def get_stats(self):
        total = self.stats['total_requests']
        hits = self.stats['cache_hits']
        hit_rate = (hits / total * 100) if total > 0 else 0
        
        return {
            'total_requests': total,
            'cache_hits': hits,
            'cache_misses': self.stats['cache_misses'],
            'hit_rate': f"{hit_rate:.2f}%",
            'items_cached': self.stats['items_cached']
        }

# Usage
cache = CacheWithStats()
# ... perform operations ...
print(cache.get_stats())
```

## Constraints
- **Memory Usage**: Semantic caching stores embeddings in memory
- **Staleness**: Cached responses may become outdated
- **Similarity Threshold**: Tune based on your use case (0.85-0.95)
- **Cache Size**: Implement cache eviction policies for long-running systems
- **Cost vs. Freshness**: Balance between caching and getting fresh responses

## Expected Output
Significant reduction in API costs (50-90% in some cases) and improved latency through intelligent caching of LLM responses.

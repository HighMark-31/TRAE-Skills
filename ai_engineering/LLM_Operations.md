# Skill: LLM Operations (LLMOps)

## Purpose
To operationalize large language models in production environments with proper deployment, scaling, monitoring, and maintenance.

## When to Use
- When deploying LLMs to production
- When managing multiple LLM deployments
- When optimizing LLM performance and costs
- When implementing LLM version control and rollback

## Procedure

### 1. Model Deployment Strategy
Implement robust deployment strategies for LLMs.

```python
from abc import ABC, abstractmethod
from openai import OpenAI
import time
from functools import wraps
import logging

class LLMProvider(ABC):
    """Abstract base class for LLM providers."""
    
    @abstractmethod
    def generate(self, prompt, **kwargs):
        pass
    
    @abstractmethod
    def health_check(self):
        pass

class OpenAIProvider(LLMProvider):
    def __init__(self, api_key, model="gpt-4"):
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.logger = logging.getLogger(__name__)
    
    def generate(self, prompt, temperature=0.7, max_tokens=1000):
        """Generate text using OpenAI API."""
        try:
            start_time = time.time()
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            latency = time.time() - start_time
            
            result = {
                'text': response.choices[0].message.content,
                'tokens_used': response.usage.total_tokens,
                'latency': latency,
                'model': self.model
            }
            
            self.logger.info(f"Generated {result['tokens_used']} tokens in {latency:.2f}s")
            return result
            
        except Exception as e:
            self.logger.error(f"Generation failed: {str(e)}")
            raise
    
    def health_check(self):
        """Check if the API is accessible."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "ping"}],
                max_tokens=5
            )
            return {'status': 'healthy', 'model': self.model}
        except Exception as e:
            return {'status': 'unhealthy', 'error': str(e)}

class LocalLLMProvider(LLMProvider):
    """Provider for locally hosted LLMs (e.g., using Ollama or vLLM)."""
    
    def __init__(self, endpoint, model_name):
        self.endpoint = endpoint
        self.model_name = model_name
        self.logger = logging.getLogger(__name__)
    
    def generate(self, prompt, temperature=0.7, max_tokens=1000):
        """Generate text using local LLM."""
        import requests
        
        try:
            start_time = time.time()
            
            response = requests.post(
                f"{self.endpoint}/generate",
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "temperature": temperature,
                    "max_tokens": max_tokens
                },
                timeout=30
            )
            
            response.raise_for_status()
            data = response.json()
            
            latency = time.time() - start_time
            
            return {
                'text': data.get('text', ''),
                'tokens_used': data.get('tokens_used', 0),
                'latency': latency,
                'model': self.model_name
            }
            
        except Exception as e:
            self.logger.error(f"Local generation failed: {str(e)}")
            raise
    
    def health_check(self):
        """Check if local LLM is running."""
        try:
            import requests
            response = requests.get(f"{self.endpoint}/health", timeout=5)
            response.raise_for_status()
            return {'status': 'healthy', 'model': self.model_name}
        except Exception as e:
            return {'status': 'unhealthy', 'error': str(e)}

class LLMOrchestrator:
    """Orchestrate multiple LLM providers with fallback and load balancing."""
    
    def __init__(self, providers):
        self.providers = providers
        self.current_provider = 0
        self.logger = logging.getLogger(__name__)
    
    def generate(self, prompt, **kwargs):
        """Generate with automatic failover."""
        for attempt in range(len(self.providers)):
            provider = self.providers[self.current_provider]
            
            try:
                result = provider.generate(prompt, **kwargs)
                result['provider'] = provider.__class__.__name__
                return result
                
            except Exception as e:
                self.logger.warning(f"Provider {provider.__class__.__name__} failed: {str(e)}")
                self.current_provider = (self.current_provider + 1) % len(self.providers)
        
        raise Exception("All LLM providers failed")
    
    def health_check(self):
        """Health check for all providers."""
        health_status = {}
        for i, provider in enumerate(self.providers):
            health_status[f"provider_{i}"] = provider.health_check()
        return health_status
```

### 2. Rate Limiting and Throttling
Implement rate limiting for API calls.

```python
import threading
import time
from collections import deque

class RateLimiter:
    """Token bucket rate limiter."""
    
    def __init__(self, rate, burst):
        """
        Args:
            rate: Tokens per second
            burst: Maximum burst size
        """
        self.rate = rate
        self.burst = burst
        self.tokens = burst
        self.last_update = time.time()
        self.lock = threading.Lock()
    
    def consume(self, tokens=1):
        """Consume tokens if available."""
        with self.lock:
            now = time.time()
            elapsed = now - self.last_update
            
            # Refill tokens based on elapsed time
            self.tokens = min(self.burst, self.tokens + elapsed * self.rate)
            self.last_update = now
            
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            else:
                return False
    
    def wait_for_token(self, tokens=1):
        """Wait until tokens are available."""
        while not self.consume(tokens):
            wait_time = (tokens - self.tokens) / self.rate
            time.sleep(wait_time)

class LLMWithRateLimit:
    """LLM wrapper with rate limiting."""
    
    def __init__(self, llm_provider, requests_per_second=10):
        self.llm_provider = llm_provider
        self.rate_limiter = RateLimiter(rate=requests_per_second, burst=20)
    
    def generate(self, prompt, **kwargs):
        """Generate with rate limiting."""
        self.rate_limiter.wait_for_token()
        return self.llm_provider.generate(prompt, **kwargs)
    
    def generate_batch(self, prompts, **kwargs):
        """Generate multiple prompts with rate limiting."""
        results = []
        for prompt in prompts:
            result = self.generate(prompt, **kwargs)
            results.append(result)
        return results
```

### 3. Caching and Response Management
Implement intelligent caching for LLM responses.

```python
import hashlib
import json
from typing import Optional
import redis

class LLMCache:
    """Cache LLM responses."""
    
    def __init__(self, redis_client=None, ttl=3600):
        self.redis = redis_client
        self.ttl = ttl
        self.memory_cache = {}
    
    def _generate_cache_key(self, prompt, model, **kwargs):
        """Generate cache key from prompt and parameters."""
        params = f"{prompt}:{model}:{json.dumps(kwargs, sort_keys=True)}"
        return hashlib.sha256(params.encode()).hexdigest()
    
    def get(self, prompt, model, **kwargs) -> Optional[str]:
        """Get cached response."""
        cache_key = self._generate_cache_key(prompt, model, **kwargs)
        
        # Check memory cache first
        if cache_key in self.memory_cache:
            return self.memory_cache[cache_key]
        
        # Check Redis
        if self.redis:
            cached = self.redis.get(cache_key)
            if cached:
                self.memory_cache[cache_key] = cached
                return cached
        
        return None
    
    def set(self, prompt, response, model, **kwargs):
        """Cache response."""
        cache_key = self._generate_cache_key(prompt, model, **kwargs)
        
        # Store in memory
        self.memory_cache[cache_key] = response
        
        # Store in Redis
        if self.redis:
            self.redis.setex(cache_key, self.ttl, response)

class CachedLLM:
    """LLM with caching capability."""
    
    def __init__(self, llm_provider, cache=None):
        self.llm_provider = llm_provider
        self.cache = cache or LLMCache()
    
    def generate(self, prompt, use_cache=True, **kwargs):
        """Generate with optional caching."""
        model = getattr(self.llm_provider, 'model', 'unknown')
        
        if use_cache:
            cached_response = self.cache.get(prompt, model, **kwargs)
            if cached_response:
                return {
                    'text': cached_response,
                    'cached': True,
                    'model': model
                }
        
        result = self.llm_provider.generate(prompt, **kwargs)
        
        if use_cache:
            self.cache.set(prompt, result['text'], model, **kwargs)
        
        result['cached'] = False
        return result
```

### 4. Monitoring and Metrics
Track LLM performance and usage.

```python
from dataclasses import dataclass
from typing import List
import statistics

@dataclass
class LLMCallMetrics:
    """Metrics for individual LLM calls."""
    timestamp: float
    model: str
    tokens_used: int
    latency: float
    success: bool
    error_message: str = ""

class LLMMetricsCollector:
    """Collect and analyze LLM metrics."""
    
    def __init__(self, max_metrics=10000):
        self.metrics: List[LLMCallMetrics] = []
        self.max_metrics = max_metrics
    
    def record_call(self, model, tokens_used, latency, success, error_message=""):
        """Record metrics for an LLM call."""
        metric = LLMCallMetrics(
            timestamp=time.time(),
            model=model,
            tokens_used=tokens_used,
            latency=latency,
            success=success,
            error_message=error_message
        )
        
        self.metrics.append(metric)
        
        # Keep only recent metrics
        if len(self.metrics) > self.max_metrics:
            self.metrics = self.metrics[-self.max_metrics:]
    
    def get_statistics(self, model=None, time_window_seconds=None):
        """Get statistics for LLM calls."""
        filtered_metrics = self.metrics
        
        if model:
            filtered_metrics = [m for m in filtered_metrics if m.model == model]
        
        if time_window_seconds:
            cutoff = time.time() - time_window_seconds
            filtered_metrics = [m for m in filtered_metrics if m.timestamp > cutoff]
        
        if not filtered_metrics:
            return {'error': 'No metrics found'}
        
        successful_calls = [m for m in filtered_metrics if m.success]
        
        stats = {
            'total_calls': len(filtered_metrics),
            'successful_calls': len(successful_calls),
            'error_rate': (len(filtered_metrics) - len(successful_calls)) / len(filtered_metrics),
            'avg_tokens': statistics.mean([m.tokens_used for m in successful_calls]) if successful_calls else 0,
            'avg_latency': statistics.mean([m.latency for m in successful_calls]) if successful_calls else 0,
            'p50_latency': statistics.median([m.latency for m in successful_calls]) if successful_calls else 0,
            'p95_latency': statistics.quantiles([m.latency for m in successful_calls], n=20)[18] if len(successful_calls) > 20 else 0,
            'total_tokens': sum([m.tokens_used for m in successful_calls])
        }
        
        return stats

class InstrumentedLLM:
    """LLM with automatic metrics collection."""
    
    def __init__(self, llm_provider, metrics_collector):
        self.llm_provider = llm_provider
        self.metrics_collector = metrics_collector
    
    def generate(self, prompt, **kwargs):
        """Generate with metrics collection."""
        model = getattr(self.llm_provider, 'model', 'unknown')
        start_time = time.time()
        
        try:
            result = self.llm_provider.generate(prompt, **kwargs)
            latency = time.time() - start_time
            
            self.metrics_collector.record_call(
                model=model,
                tokens_used=result.get('tokens_used', 0),
                latency=latency,
                success=True
            )
            
            return result
            
        except Exception as e:
            latency = time.time() - start_time
            self.metrics_collector.record_call(
                model=model,
                tokens_used=0,
                latency=latency,
                success=False,
                error_message=str(e)
            )
            raise
```

### 5. Deployment Configuration
Manage deployment configurations.

```python
from typing import Dict, Any
import yaml

class LLMDeploymentConfig:
    """Configuration for LLM deployment."""
    
    def __init__(self, config_dict: Dict[str, Any]):
        self.config = config_dict
    
    @classmethod
    def from_file(cls, config_file: str):
        """Load configuration from file."""
        with open(config_file, 'r') as f:
            config_dict = yaml.safe_load(f)
        return cls(config_dict)
    
    def get_provider_config(self, provider_name: str):
        """Get configuration for specific provider."""
        return self.config.get('providers', {}).get(provider_name, {})
    
    def get_model_config(self, model_name: str):
        """Get configuration for specific model."""
        return self.config.get('models', {}).get(model_name, {})
    
    def get_rate_limits(self) -> Dict[str, int]:
        """Get rate limit configuration."""
        return self.config.get('rate_limits', {
            'requests_per_second': 10,
            'burst': 20
        })
    
    def get_cache_config(self) -> Dict[str, Any]:
        """Get cache configuration."""
        return self.config.get('cache', {
            'enabled': True,
            'ttl': 3600,
            'redis_url': None
        })

# Example configuration file
example_config = {
    'providers': {
        'openai': {
            'api_key': 'your-api-key',
            'model': 'gpt-4',
            'temperature': 0.7,
            'max_tokens': 1000
        },
        'local': {
            'endpoint': 'http://localhost:11434',
            'model': 'llama2',
            'temperature': 0.7
        }
    },
    'models': {
        'gpt-4': {
            'cost_per_1k_tokens': 0.03,
            'max_tokens': 8192
        },
        'gpt-3.5-turbo': {
            'cost_per_1k_tokens': 0.002,
            'max_tokens': 4096
        }
    },
    'rate_limits': {
        'requests_per_second': 10,
        'burst': 20
    },
    'cache': {
        'enabled': True,
        'ttl': 3600,
        'redis_url': 'redis://localhost:6379'
    }
}
```

## Constraints
- **API Costs**: Monitor and control LLM API costs carefully
- **Latency**: LLM calls can be slow, implement proper timeouts
- **Rate Limits**: Respect provider rate limits to avoid being blocked
- **Error Handling**: Implement robust error handling and retry logic
- **Monitoring**: Track usage and performance for optimization
- **Scalability**: Design for horizontal scaling when needed

## Expected Output
Production-ready LLM deployment with proper rate limiting, caching, monitoring, and multi-provider orchestration for reliable and cost-effective operations.

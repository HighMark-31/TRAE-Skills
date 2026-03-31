# Skill: Token Optimization

## Purpose
To minimize token usage while maintaining output quality, reducing API costs and improving response times.

## When to Use
- When working with large documents or contexts
- When building cost-sensitive applications
- When processing multiple documents
- When optimizing for faster responses

## Procedure

### 1. Prune Redundant Content
Remove unnecessary information from prompts.

```python
def prune_redundant_content(text):
    """Remove redundant phrases and content."""
    # Common redundant phrases to remove
    redundant_phrases = [
        "please note that",
        "it is important to mention",
        "as previously stated",
        "in conclusion",
        "additionally",
        "furthermore",
        "moreover"
    ]
    
    pruned = text
    for phrase in redundant_phrases:
        pruned = pruned.replace(phrase, "")
    
    # Remove multiple spaces
    pruned = " ".join(pruned.split())
    
    return pruned

# Example
original = """Please note that it is important to mention that the document 
contains multiple sections. Furthermore, additionally, it has various topics."""

optimized = prune_redundant_content(original)
print(f"Original: {len(original)} tokens")
print(f"Optimized: {len(optimized)} tokens")
```

### 2. Use Efficient Prompt Structures
Structure prompts to maximize information density.

```python
# INEFFICIENT - verbose prompt
inefficient_prompt = """
I would like you to please help me by analyzing the following text. 
Please provide me with a summary of the main points. 
The text is as follows: {text}
"""

# EFFICIENT - concise prompt
efficient_prompt = """Summarize the main points: {text}"""

# Even more efficient with examples
few_shot_efficient = """Text: {text1}
Summary: {summary1}

Text: {text2}
Summary: {summary2}

Text: {text}
Summary:"""
```

### 3. Chunk and Summarize Large Documents
Process large documents in chunks with progressive summarization.

```python
def chunk_text(text, max_chunk_size=2000):
    """Split text into chunks of roughly equal token count."""
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0
    
    for word in words:
        current_chunk.append(word)
        current_length += 1
        
        if current_length >= max_chunk_size:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_length = 0
    
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    return chunks

def progressive_summarize(text):
    """Summarize large document progressively."""
    # Split into chunks
    chunks = chunk_text(text, max_chunk_size=2000)
    
    # Summarize each chunk
    chunk_summaries = []
    for chunk in chunks:
        summary = client.chat.completions.create(
            model="gpt-4",
            messages=[{
                "role": "user", 
                "content": f"Summarize in 1-2 sentences: {chunk}"
            }]
        )
        chunk_summaries.append(summary.choices[0].message.content)
    
    # Combine chunk summaries
    combined = " ".join(chunk_summaries)
    
    # Final summary
    final_summary = client.chat.completions.create(
        model="gpt-4",
        messages=[{
            "role": "user", 
            "content": f"Create a cohesive summary: {combined}"
        }]
    )
    
    return final_summary.choices[0].message.content
```

### 4. Use System Messages Effectively
Move static context to system messages.

```python
# INEFFICIENT - repeating instructions in every message
messages_inefficient = [
    {
        "role": "user",
        "content": "You are a helpful assistant that provides concise answers. 
                    Please answer this question: What is machine learning?"
    }
]

# EFFICIENT - use system message
messages_efficient = [
    {
        "role": "system",
        "content": "You are a helpful assistant. Provide concise answers in 2-3 sentences."
    },
    {
        "role": "user",
        "content": "What is machine learning?"
    }
]
```

### 5. Use Smaller Models When Appropriate
Choose the right model for the task.

```python
def choose_model(task_complexity, token_count):
    """Choose the most cost-effective model."""
    if token_count < 500 and task_complexity == "simple":
        return "gpt-3.5-turbo"
    elif token_count < 2000 and task_complexity in ["simple", "medium"]:
        return "gpt-3.5-turbo"
    else:
        return "gpt-4"

# Example usage
text = "Your text here..."
token_count = len(text.split()) * 1.3  # Rough estimate
model = choose_model("medium", token_count)

response = client.chat.completions.create(
    model=model,
    messages=[{"role": "user", "content": text}]
)
```

### 6. Implement Token Counting and Budgeting
Track and limit token usage.

```python
import tiktoken

def count_tokens(text, model="gpt-4"):
    """Count tokens in text."""
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

class TokenBudget:
    def __init__(self, max_tokens=100000):
        self.max_tokens = max_tokens
        self.used_tokens = 0
        self.encoding = tiktoken.encoding_for_model("gpt-4")
    
    def can_process(self, text):
        """Check if we can process this text within budget."""
        tokens = count_tokens(text)
        return (self.used_tokens + tokens) <= self.max_tokens
    
    def process(self, text, function):
        """Process text if within budget."""
        if not self.can_process(text):
            raise Exception("Token budget exceeded!")
        
        tokens = count_tokens(text)
        self.used_tokens += tokens
        
        return function(text)
    
    def get_usage(self):
        """Get current token usage."""
        return {
            "used": self.used_tokens,
            "remaining": self.max_tokens - self.used_tokens,
            "percentage": (self.used_tokens / self.max_tokens) * 100
        }

# Usage
budget = TokenBudget(max_tokens=50000)

def make_llm_call(text):
    return client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": text}]
    )

try:
    result = budget.process("Your text here", make_llm_call)
    print(budget.get_usage())
except Exception as e:
    print(f"Error: {e}")
```

## Constraints
- **Quality vs. Cost**: Aggressive optimization may impact output quality
- **Context Loss**: Removing too much content may lose important information
- **Model Limitations**: Different models have different capabilities
- **Token Estimation**: Token counts are estimates, not exact
- **Budget Planning**: Always include buffer for unexpected token usage

## Expected Output
Reduced API costs (30-70% savings) while maintaining acceptable output quality through intelligent token optimization strategies.

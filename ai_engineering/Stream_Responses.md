# Skill: Stream Responses

## Purpose
To deliver LLM responses in real-time chunks, improving user experience by providing immediate feedback and reducing perceived latency.

## When to Use
- When building chat interfaces
- When processing long responses
- When users need immediate feedback
- When implementing real-time AI interactions

## Procedure

### 1. Basic Streaming Setup
Implement basic streaming with OpenAI API.

```python
from openai import OpenAI
import sys

client = OpenAI()

def stream_response(prompt, model="gpt-4"):
    """Stream a basic response from the LLM."""
    print("Assistant: ", end="", flush=True)
    
    stream = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        stream=True
    )
    
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            print(content, end="", flush=True)
            yield content
    
    print()  # New line after completion

# Usage
for chunk in stream_response("Explain quantum computing in simple terms"):
    pass  # Process chunks if needed
```

### 2. Streaming with Buffering
Implement buffering for more controlled output.

```python
def buffered_stream(prompt, buffer_size=10, delay=0.1):
    """Stream with buffering to prevent choppy output."""
    import time
    
    buffer = []
    stream = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        stream=True
    )
    
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            buffer.append(content)
            
            if len(buffer) >= buffer_size:
                print("".join(buffer), end="", flush=True)
                buffer = []
                time.sleep(delay)
    
    # Print remaining buffer
    if buffer:
        print("".join(buffer), end="", flush=True)
    print()

# Usage
buffered_stream("Write a short story about a robot learning to paint")
```

### 3. Async Streaming
Implement asynchronous streaming for better performance.

```python
import asyncio
from openai import AsyncOpenAI

async_client = AsyncOpenAI()

async def async_stream(prompt):
    """Stream responses asynchronously."""
    stream = await async_client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        stream=True
    )
    
    full_response = ""
    async for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            print(content, end="", flush=True)
            full_response += content
    
    print()
    return full_response

# Usage
async def main():
    response = await async_stream("What are the benefits of async programming?")
    
asyncio.run(main())
```

### 4. Multi-User Streaming
Handle streaming for multiple concurrent users.

```python
class StreamingManager:
    def __init__(self):
        self.active_streams = {}
    
    async def stream_to_user(self, user_id, prompt):
        """Stream response to a specific user."""
        self.active_streams[user_id] = True
        
        try:
            stream = await async_client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                stream=True
            )
            
            async for chunk in stream:
                if not self.active_streams.get(user_id, False):
                    print(f"Stream cancelled for user {user_id}")
                    break
                
                if chunk.choices[0].delta.content is not None:
                    # In real implementation, send to user via WebSocket
                    content = chunk.choices[0].delta.content
                    print(f"User {user_id}: {content}", end="", flush=True)
            
            print()
        finally:
            self.active_streams.pop(user_id, None)
    
    def cancel_stream(self, user_id):
        """Cancel stream for a specific user."""
        self.active_streams[user_id] = False

# Usage
manager = StreamingManager()

async def handle_multiple_users():
    tasks = [
        manager.stream_to_user(1, "Tell me a joke"),
        manager.stream_to_user(2, "Explain machine learning")
    ]
    await asyncio.gather(*tasks)

asyncio.run(handle_multiple_users())
```

### 5. Process Streaming Output
Process chunks during streaming.

```python
class StreamProcessor:
    def __init__(self):
        self.collected_chunks = []
        self.processed_chunks = []
    
    def process_chunk(self, chunk):
        """Process individual chunks during streaming."""
        # Example: filter or transform chunks
        processed = chunk.replace("**", "").replace("__", "")
        self.processed_chunks.append(processed)
        return processed
    
    def stream_with_processing(self, prompt):
        """Stream and process chunks in real-time."""
        stream = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            stream=True
        )
        
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                self.collected_chunks.append(content)
                
                processed = self.process_chunk(content)
                print(processed, end="", flush=True)
        
        print()
        return "".join(self.processed_chunks)

# Usage
processor = StreamProcessor()
result = processor.stream_with_processing("Write markdown formatted text with bold and italics")
```

### 6. Web Integration with Streaming
Integrate streaming with web frameworks.

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import json

app = FastAPI()

def generate_stream(prompt):
    """Generator for FastAPI streaming response."""
    stream = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        stream=True
    )
    
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            # Format as SSE (Server-Sent Events)
            data = json.dumps({"content": content})
            yield f"data: {data}\n\n"
    
    yield "data: [DONE]\n\n"

@app.post("/chat")
async def chat_endpoint(prompt: str):
    """Endpoint for streaming chat responses."""
    return StreamingResponse(
        generate_stream(prompt),
        media_type="text/event-stream"
    )

# For client-side JavaScript:
"""
const response = await fetch('/chat', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({prompt: 'Hello'})
});

const reader = response.body.getReader();
const decoder = new TextDecoder();

while (true) {
    const {done, value} = await reader.read();
    if (done) break;
    
    const chunk = decoder.decode(value);
    // Process chunk and update UI
}
"""
```

### 7. Streaming with Metadata
Include metadata with streaming responses.

```python
def stream_with_metadata(prompt):
    """Stream response with additional metadata."""
    stream = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        stream=True
    )
    
    total_tokens = 0
    start_time = time.time()
    
    for i, chunk in enumerate(stream):
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            total_tokens += len(content.split())
            
            metadata = {
                "chunk": i,
                "tokens": total_tokens,
                "elapsed": time.time() - start_time
            }
            
            yield {
                "content": content,
                "metadata": metadata
            }
    
    # Final metadata
    final_metadata = {
        "total_chunks": i + 1,
        "estimated_tokens": total_tokens,
        "total_time": time.time() - start_time
    }
    
    yield {
        "content": "",
        "metadata": final_metadata,
        "complete": True
    }

# Usage
for response in stream_with_metadata("Write a 500-word essay on AI"):
    if response.get("complete"):
        print(f"\nCompleted in {response['metadata']['total_time']:.2f}s")
    else:
        print(response["content"], end="", flush=True)
```

## Constraints
- **Token Counting**: Streaming makes exact token counting difficult
- **Error Handling**: Handle connection failures mid-stream gracefully
- **Buffer Size**: Balance between real-time feedback and choppy output
- **Memory Usage**: Be careful with memory for very long responses
- **Cancellation**: Implement proper cancellation for user interruptions
- **Format Maintenance**: Streaming may break markdown formatting temporarily

## Expected Output
Real-time streaming responses that provide immediate user feedback, with proper error handling and integration capabilities for various applications.

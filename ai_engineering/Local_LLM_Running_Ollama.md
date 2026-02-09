# Skill: Local LLM Running (Ollama)

## Purpose
To run Large Language Models locally using Ollama, ensuring data privacy, zero API costs, and offline capability while providing a standard REST API for applications.

## When to Use
- When data privacy is paramount (medical, legal, personal data).
- For development and testing without incurring API costs.
- When you need to experiment with open-source models (Llama 3, Mistral, etc.).

## Procedure

### 1. Installation & Model Setup
Install Ollama and pull the desired model.

```bash
# Install (macOS/Linux)
curl -fsSL https://ollama.com/install.sh | sh

# Pull a model
ollama pull llama3:8b
```

### 2. Basic Usage (CLI)
Interact with the model directly in your terminal.

```bash
ollama run llama3:8b "Why is the sky blue?"
```

### 3. Programmatic Integration (Node.js)
Use the Ollama REST API or official library to integrate into your app.

```bash
npm install ollama
```

```typescript
import ollama from 'ollama';

async function chat() {
  const response = await ollama.chat({
    model: 'llama3:8b',
    messages: [{ role: 'user', content: 'Explain quantum physics to a 5-year old' }],
    stream: true,
  });

  for await (const part of response) {
    process.stdout.write(part.message.content);
  }
}
```

### 4. Customizing Models (Modelfile)
Create a specialized version of a model with custom system prompts.

1. Create a file named `Modelfile`:
```dockerfile
FROM llama3:8b

# Set parameters
PARAMETER temperature 0.1
PARAMETER top_p 0.9

# Set system message
SYSTEM """
You are a senior TypeScript developer. 
You provide concise, high-performance code snippets.
Always use ESM syntax.
"""
```

2. Create the model:
```bash
ollama create ts-expert -f Modelfile
```

### 5. Running as a Service (Docker)
Run Ollama in a container for consistent deployment.

```bash
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

## Constraints
- **VRAM Requirements**: 
  - 7B/8B models: ~8GB RAM/VRAM.
  - 13B models: ~16GB RAM/VRAM.
  - 70B models: ~48GB+ RAM/VRAM.
- **Latency**: Local models are significantly slower than GPT-4o unless running on a high-end GPU (RTX 3090/4090 or Apple M2/M3 Max).
- **Quantization**: Most Ollama models are 4-bit quantized (Q4_K_M) by default, which slightly reduces reasoning capability but saves memory.

## Expected Output
A locally running LLM service accessible via a REST API on `localhost:11434`.

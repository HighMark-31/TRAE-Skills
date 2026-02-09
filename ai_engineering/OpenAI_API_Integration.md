# Skill: OpenAI API Integration

## Purpose
To correctly integrate OpenAI's models (GPT-4o, GPT-3.5) into Node.js/TypeScript applications, handling authentication, type-safety, streaming, and robust error management.

## When to Use
- When building applications that rely on OpenAI's completion or chat API.
- When you need a production-ready wrapper around the official SDK.

## Procedure

### 1. Installation & Setup
Install the official library and type definitions.

```bash
npm install openai zod
```

### 2. Robust Client Implementation
Create a service class that handles initialization and configuration.

```typescript
// lib/openai-client.ts
import OpenAI from 'openai';

export class OpenAIClient {
  private client: OpenAI;

  constructor() {
    if (!process.env.OPENAI_API_KEY) {
      throw new Error("Missing OPENAI_API_KEY environment variable");
    }
    this.client = new OpenAI({
      apiKey: process.env.OPENAI_API_KEY,
      maxRetries: 3, // Built-in retry logic
      timeout: 30000, // 30s timeout
    });
  }

  public getClient() {
    return this.client;
  }
}
```

### 3. Chat Completion with Error Handling
Implement a method for standard chat completions with try/catch blocks for specific API errors.

```typescript
// lib/ai-service.ts
import { OpenAIClient } from './openai-client';
import OpenAI from 'openai';

export class AIService {
  private openai: OpenAI;

  constructor() {
    this.openai = new OpenAIClient().getClient();
  }

  async generateResponse(systemPrompt: string, userMessage: string): Promise<string> {
    try {
      const response = await this.openai.chat.completions.create({
        model: "gpt-4o",
        messages: [
          { role: "system", content: systemPrompt },
          { role: "user", content: userMessage },
        ],
        temperature: 0.7,
      });

      return response.choices[0]?.message?.content || "";
    } catch (error) {
      if (error instanceof OpenAI.APIError) {
        console.error(`OpenAI Error: ${error.status} - ${error.code}`);
        // Handle specific codes: 429 (Rate Limit), 400 (Bad Request), 401 (Auth)
        if (error.status === 429) {
          throw new Error("Rate limit exceeded. Please try again later.");
        }
      }
      throw new Error("Failed to generate AI response");
    }
  }
}
```

### 4. Streaming Response Implementation
Handle real-time output for better UX.

```typescript
// lib/stream-service.ts
import { OpenAIClient } from './openai-client';

export async function* streamCompletion(prompt: string) {
  const openai = new OpenAIClient().getClient();
  
  const stream = await openai.chat.completions.create({
    model: "gpt-4o",
    messages: [{ role: "user", content: prompt }],
    stream: true,
  });

  for await (const chunk of stream) {
    const content = chunk.choices[0]?.delta?.content || "";
    if (content) {
      yield content;
    }
  }
}

// Usage:
// for await (const token of streamCompletion("Hello")) {
//   process.stdout.write(token);
// }
```

### 5. Structured Outputs (JSON)
Enforce JSON output for programmatic use.

```typescript
async function extractData(text: string) {
  const openai = new OpenAIClient().getClient();
  const response = await openai.chat.completions.create({
    model: "gpt-4o",
    messages: [
      { role: "system", content: "You are a data extractor. Output valid JSON." },
      { role: "user", content: `Extract names from: ${text}` }
    ],
    response_format: { type: "json_object" },
  });
  
  return JSON.parse(response.choices[0].message.content!);
}
```

## Constraints
- **Costs**: GPT-4 is expensive. Cache responses where possible (e.g., using Redis) for identical inputs.
- **Security**: Never expose the API key on the client-side (browser). Always proxy requests through your backend.
- **Timeouts**: LLM requests can be slow. Ensure your HTTP server (e.g., Nginx, Vercel) has appropriate timeout settings (often > 10s).

## Expected Output
A secure, reusable service module that reliably communicates with OpenAI, handles rate limits, and provides both streaming and blocking interfaces.

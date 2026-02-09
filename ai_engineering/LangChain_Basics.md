# Skill: LangChain Basics

## Purpose
To utilize the LangChain framework to build complex LLM applications by chaining together components (Models, Prompts, Parsers) into composable workflows.

## When to Use
- When building complex chains (e.g., Retrieval -> Augmentation -> Generation).
- When you need to swap LLM providers easily (e.g., OpenAI to Anthropic).
- When integrating structured output parsing.

## Procedure

### 1. Installation
Install core LangChain packages and the OpenAI integration.

```bash
npm install @langchain/core @langchain/openai zod
```

### 2. Basic Chain Construction (LCEL)
Use LangChain Expression Language (LCEL) for declarative chain definitions.

```typescript
import { ChatOpenAI } from "@langchain/openai";
import { ChatPromptTemplate } from "@langchain/core/prompts";
import { StringOutputParser } from "@langchain/core/output_parsers";

// 1. Initialize Model
const model = new ChatOpenAI({
  modelName: "gpt-4o",
  temperature: 0,
  apiKey: process.env.OPENAI_API_KEY
});

// 2. Define Prompt
const prompt = ChatPromptTemplate.fromMessages([
  ["system", "You are a technical documentation expert."],
  ["user", "Explain {topic} in one sentence."]
]);

// 3. Create Chain
// Input -> Prompt -> Model -> String Output
const chain = prompt.pipe(model).pipe(new StringOutputParser());

// Usage
async function runChain() {
  const result = await chain.invoke({ topic: "Dependency Injection" });
  console.log(result);
}
```

### 3. Structured Output Parsing
Use `StructuredOutputParser` with Zod to guarantee type-safe responses.

```typescript
import { z } from "zod";
import { StructuredOutputParser } from "@langchain/core/output_parsers";

// Define Schema
const schema = z.object({
  sentiment: z.enum(["positive", "negative", "neutral"]),
  keywords: z.array(z.string()).describe("List of up to 5 keywords"),
  summary: z.string().describe("Brief summary of the text")
});

const parser = StructuredOutputParser.fromZodSchema(schema);

const analysisChain = ChatPromptTemplate.fromTemplate(
  "Analyze the following text.\n{format_instructions}\n\nText: {text}"
).pipe(model).pipe(parser);

async function analyzeText(text: string) {
  return await analysisChain.invoke({
    text,
    format_instructions: parser.getFormatInstructions()
  });
}
```

### 4. Memory Integration (RunnableWithMessageHistory)
Manage conversation history for chatbots.

```typescript
import { RunnableWithMessageHistory } from "@langchain/core/runnables";
import { InMemoryChatMessageHistory } from "@langchain/core/chat_history";

const messageHistory = new InMemoryChatMessageHistory();

const chatChain = new RunnableWithMessageHistory({
  runnable: prompt.pipe(model),
  getMessageHistory: async (sessionId) => messageHistory,
  inputMessagesKey: "input",
  historyMessagesKey: "history",
});
```

## Constraints
- **Abstraction Cost**: LangChain adds a layer of abstraction. For very simple calls, the native SDK might be cleaner.
- **Debugging**: LCEL chains can be harder to debug than imperative code. Use `LangSmith` for tracing if available.
- **Version Compatibility**: LangChain evolves fast. Lock versions in `package.json`.

## Expected Output
A composable pipeline that reliably transforms inputs into structured outputs, leveraging the power of chained LLM operations.

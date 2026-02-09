# Skill: AI Agent Design Patterns

## Purpose
To structure autonomous AI systems that can reason, plan, and execute tools to solve complex, multi-step problems using patterns like ReAct and Multi-Agent orchestration.

## When to Use
- When the task requires multiple distinct steps (e.g., "Find the price of BTC and email me the summary").
- When the LLM needs to interact with the outside world (APIs, Databases, Web Search).
- When the workflow is non-linear and depends on intermediate results.

## Procedure

### 1. Tool Definition (Zod-based)
Define the tools your agent can use with clear descriptions.

```typescript
import { z } from "zod";
import { tool } from "@langchain/core/tools";

const searchTool = tool(
  async ({ query }) => {
    // Implement search logic here
    return `Results for ${query}...`;
  },
  {
    name: "web_search",
    description: "Search the web for current events or technical info.",
    schema: z.object({
      query: z.string(),
    }),
  }
);
```

### 2. The ReAct Agent Pattern
Implement the Reasoning + Acting loop.

```typescript
import { ChatOpenAI } from "@langchain/openai";
import { createReactAgent } from "@langchain/langgraph/prebuilt";
import { MemorySaver } from "@langchain/langgraph";

const model = new ChatOpenAI({ modelName: "gpt-4o" });
const tools = [searchTool];
const checkpointer = new MemorySaver();

const app = createReactAgent({
  llm: model,
  tools,
  checkpointSaver: checkpointer,
});

// Usage
const result = await app.invoke(
  { messages: [{ role: "user", content: "What is the current price of Ethereum?" }] },
  { configurable: { thread_id: "user_1" } }
);
```

### 3. Multi-Agent Orchestration (Hand-off)
Structure specialized agents that pass tasks to each other.

```typescript
// Conceptual LangGraph Flow:
// 1. Router Agent -> Decides if it's a "Coding" or "Writing" task.
// 2. Coder Agent -> Generates code.
// 3. Reviewer Agent -> Reviews code. If errors, sends back to Coder.
// 4. Final Output.
```

### 4. Guardrails & Safety
Implement safety checks for tool execution.

```typescript
const safeExecute = (action: string) => {
  const forbidden = ["rm -rf", "delete", "drop table"];
  if (forbidden.some(word => action.includes(word))) {
    throw new Error("Safety violation: forbidden command.");
  }
};
```

### 5. State Management
Maintain the conversation and tool execution state.

```typescript
// Use LangGraph state to keep track of:
// - messages
// - tool_outputs
// - current_step
```

## Constraints
- **Infinite Loops**: Always set a `maxIterations` or recursion limit.
- **Context Bloat**: Agents generate a lot of tokens. Prune history or use summarization for long tasks.
- **Tool Descriptions**: The agent's performance is 90% dependent on how well you describe the tools. Be extremely precise.

## Expected Output
A robust agentic system capable of autonomous problem solving by effectively utilizing provided tools.

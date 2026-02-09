# Skill: Prompt Engineering Basics

## Purpose
To apply systematic techniques for crafting inputs (prompts) to Large Language Models (LLMs) to ensure accurate, consistent, and high-quality outputs. This skill focuses on structured prompt management and engineering patterns.

## When to Use
- When interacting with LLMs for any task (generation, summarization, extraction).
- When model outputs are inconsistent, hallucinatory, or vague.
- When you need to standardize input/output formats for an application.

## Procedure

### 1. Structured Prompt Management (TypeScript)
Avoid hardcoding strings. Use a template system.

```typescript
// prompt-manager.ts
type PromptVariables = Record<string, string>;

interface PromptTemplate {
  system: (vars: PromptVariables) => string;
  user: (vars: PromptVariables) => string;
}

export const summarizationPrompt: PromptTemplate = {
  system: ({ context }) => 
    `You are an expert technical writer. Your task is to summarize the following context into a concise executive summary.
    
    Context: ${context}
    
    Constraints:
    - Use bullet points.
    - Max 200 words.
    - Maintain a professional tone.`,
  
  user: ({ text }) => `Text to summarize:\n${text}`
};
```

### 2. The CO-STAR Framework Implementation
Implement the CO-STAR framework programmatically to ensure all context is provided.

```typescript
// co-star-prompt.ts
interface CoStarParams {
  context: string;
  objective: string;
  style: string;
  tone: string;
  audience: string;
  responseFormat: string;
}

export const buildCoStarSystemMessage = (params: CoStarParams): string => {
  return `
  # CONTEXT
  ${params.context}

  # OBJECTIVE
  ${params.objective}

  # STYLE
  ${params.style}

  # TONE
  ${params.tone}

  # AUDIENCE
  ${params.audience}

  # RESPONSE FORMAT
  ${params.responseFormat}
  `;
};
```

### 3. Chain-of-Thought (CoT) & Few-Shot Prompting
Enhance reasoning by forcing step-by-step logic or providing examples.

```typescript
// reasoning-prompt.ts
const fewShotExamples = `
Input: "The server is down."
Classification: Critical
Reasoning: Impact on availability is immediate.

Input: "The button color is slightly off."
Classification: Low
Reasoning: Purely cosmetic issue.
`;

export const classificationPrompt = (input: string) => `
Classify the severity of the following issue (Critical, High, Medium, Low).
First, explain your reasoning step-by-step, then provide the final classification.

Examples:
${fewShotExamples}

Input: "${input}"
Output:
`;
```

### 4. Handling Output Formats (JSON Mode)
Always enforce structure when programmatic consumption is needed.

```typescript
// Ensure your API call sets { response_format: { type: "json_object" } }
export const jsonExtractionPrompt = (text: string) => `
Extract the key entities from the text below.
You must respond with valid JSON only.

Schema:
{
  "names": string[],
  "dates": string[],
  "sentiment": "positive" | "negative" | "neutral"
}

Text: "${text}"
`;
```

## Constraints
- **Context Window**: Monitor token count. Truncate inputs if they exceed limits (e.g., using `tiktoken`).
- **Injection Attacks**: Treat user input as untrusted. Delimit user input (e.g., with `"""` or `###`) to prevent prompt injection.
- **Determinism**: Set `temperature: 0` for classification/extraction tasks; higher for creative tasks.

## Expected Output
A set of typed, reusable prompt templates that produce consistent, parsed outputs from the LLM.

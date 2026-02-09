# Skill: AI Model Evaluation

## Purpose
To systematically assess the performance, accuracy, and safety of LLM outputs using quantitative metrics and "LLM-as-a-Judge" patterns, ensuring production readiness.

## When to Use
- Before deploying any LLM application to production.
- When comparing different models (e.g., GPT-4o vs. Claude 3.5 Sonnet) or prompt versions.
- To detect regressions after updating prompts or RAG knowledge bases.

## Procedure

### 1. Define the Evaluation Dataset (Golden Set)
Create a `tests.json` file containing inputs and expected outputs.

```json
[
  {
    "input": "What is the return policy?",
    "expected": "You can return items within 30 days.",
    "context": "Our policy allows returns for 30 days from purchase date."
  }
]
```

### 2. Implementation with Promptfoo (CLI)
Promptfoo is a popular tool for running batch evaluations.

```bash
# Install
npm install -g promptfoo

# Initialize
promptfoo init
```

Configure `promptfooconfig.yaml`:
```yaml
prompts:
  - "Answer this question using the context: {{context}}. Question: {{input}}"

providers:
  - openai:gpt-4o

tests:
  - vars:
      input: "What is the return policy?"
      context: "30-day return policy applies."
    assert:
      - type: icontains
        value: "30 days"
      - type: llm-rubric
        value: "Does not mention unrelated topics"
```

### 3. RAG Evaluation (Ragas/DeepEval)
For RAG systems, evaluate the three-way relationship: Question, Context, and Answer.

```typescript
import { rce } from "deepeval"; // Conceptual example

async function evaluateRag(query: string, retrievalContext: string, output: string) {
  // 1. Faithfulness: Is the answer grounded in the context?
  // 2. Answer Relevance: Does it answer the query?
  // 3. Context Precision: Was the retrieved context relevant?
}
```

### 4. Custom LLM-as-a-Judge Script
Use a stronger model to grade your target model.

```typescript
async function gradeOutput(question: string, answer: string, reference: string) {
  const graderPrompt = `
    You are an impartial judge. Grade the student's answer based on the reference.
    Question: ${question}
    Reference: ${reference}
    Student Answer: ${answer}
    
    Provide a score from 1-10 and a brief explanation.
    Output JSON: { "score": number, "explanation": string }
  `;
  
  // Call GPT-4 with JSON mode enabled
}
```

### 5. Continuous Integration (CI)
Integrate evaluation into your GitHub Actions to prevent regressions.

```yaml
# .github/workflows/ai-eval.yml
jobs:
  evaluate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npx promptfoo eval
```

## Constraints
- **Bias**: LLM judges tend to prefer longer answers or answers from the same provider. Use diverse judges (OpenAI + Anthropic).
- **Cost**: Running evaluations on 1000s of rows can be expensive. Use `gpt-4o-mini` for simpler checks.
- **Reference Accuracy**: A "Golden Set" is only as good as the human-verified reference answers.

## Expected Output
A detailed report (HTML/JSON) showing pass/fail status, accuracy percentages, and regression analysis.

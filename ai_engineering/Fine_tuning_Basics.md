# Skill: Fine-tuning Basics

## Purpose
To adapt a pre-trained LLM to a specific task, tone, or domain by training it on a specialized dataset, ensuring rigid adherence to format or style.

## When to Use
- When "Prompt Engineering" fails to produce the desired format consistently.
- When you need to mimic a very specific brand voice or writing style.
- To reduce latency and costs by using a smaller model (e.g., GPT-4o-mini) that performs like a larger one on a specific task.

## Procedure

### 1. Data Preparation (JSONL)
Create a dataset in the specific format required by the provider (OpenAI example).

```json
// training_data.jsonl
{"messages": [{"role": "system", "content": "You are a code reviewer."}, {"role": "user", "content": "Review this: const x = 1;"}, {"role": "assistant", "content": "LGTM. Consider using 'let' if reassigning."}]}
{"messages": [{"role": "system", "content": "You are a code reviewer."}, {"role": "user", "content": "Review this: alert('hi');"}, {"role": "assistant", "content": "Avoid 'alert' in production code."}]}
```

### 2. Validation Script (Python)
Always validate your JSONL before uploading to avoid costly training failures.

```python
import json

def validate_data(file_path):
    with open(file_path, 'r') as f:
        for line in f:
            try:
                data = json.loads(line)
                if "messages" not in data:
                    print("Missing 'messages' key")
            except Exception as e:
                print(f"Error parsing line: {e}")

validate_data("training_data.jsonl")
```

### 3. Starting the Fine-tuning Job (OpenAI CLI)
Upload the file and start the training process.

```bash
# Install CLI
pip install openai

# Set Key
export OPENAI_API_KEY="your-key"

# Upload file
openai files create -f training_data.jsonl -p fine-tune

# Start training
openai fine_tuning.jobs.create -t "file-id-from-upload" -m "gpt-4o-mini-2024-07-18"
```

### 4. Monitoring & Evaluation
Check the status and loss metrics.

```bash
# List jobs
openai fine_tuning.jobs.list

# Retrieve status
openai fine_tuning.jobs.retrieve -i "ft-job-id"
```

### 5. Using the Fine-tuned Model
Once completed, use the new model ID in your application.

```typescript
const completion = await openai.chat.completions.create({
  model: "ft:gpt-4o-mini:your-org:custom-name:id",
  messages: [{ role: "user", content: "Review this: console.log(1);" }],
});
```

## Constraints
- **Overfitting**: Don't train for too many epochs; the model will lose its general intelligence.
- **Facts vs Style**: **Never** fine-tune to teach new facts. Use RAG for facts. Use fine-tuning for **how** the model speaks.
- **Minimum Data**: You need at least 50-100 high-quality examples to see any meaningful improvement.

## Expected Output
A specialized model ID that delivers high-performance results on a specific, narrow task.

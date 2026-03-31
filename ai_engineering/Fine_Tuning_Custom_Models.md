# Skill: Fine-Tuning Custom Models

## Purpose
To adapt pre-trained LLMs to specific domains, tasks, or styles by training on custom datasets for improved performance on specialized use cases.

## When to Use
- When you need domain-specific knowledge (legal, medical, technical)
- When you want a specific writing style or tone
- When you have a large dataset of example inputs/outputs
- When you need consistent formatting or structure in outputs

## Procedure

### 1. Prepare Your Dataset
Create properly formatted training data.

```python
import json

# Training data format for OpenAI fine-tuning
training_data = [
    {
        "messages": [
            {"role": "system", "content": "You are a legal assistant specializing in contract review."},
            {"role": "user", "content": "Review this clause: 'The company may terminate at any time.'"},
            {"role": "assistant", "content": "This clause is one-sided. Consider adding: 'either party may terminate with 30 days notice.'"}
        ]
    },
    {
        "messages": [
            {"role": "system", "content": "You are a legal assistant specializing in contract review."},
            {"role": "user", "content": "Is this confidentiality clause standard?"},
            {"role": "assistant", "content": "The clause appears standard. It includes mutual confidentiality obligations and defines exceptions appropriately."}
        ]
    }
]

# Save to JSONL file
with open('training_data.jsonl', 'w') as f:
    for entry in training_data:
        f.write(json.dumps(entry) + '\n')
```

### 2. Validate Your Data
Ensure data quality before training.

```python
import json
from collections import defaultdict

def validate_finetuning_data(file_path):
    """Validate fine-tuning dataset."""
    errors = []
    stats = defaultdict(int)
    
    with open(file_path, 'r') as f:
        for line_num, line in enumerate(f, 1):
            try:
                entry = json.loads(line)
                stats['total_entries'] += 1
                
                # Check required fields
                if 'messages' not in entry:
                    errors.append(f"Line {line_num}: Missing 'messages' field")
                    continue
                
                messages = entry['messages']
                stats['total_messages'] += len(messages)
                
                # Validate message structure
                for msg in messages:
                    if 'role' not in msg or 'content' not in msg:
                        errors.append(f"Line {line_num}: Invalid message structure")
                    
                    if msg['role'] not in ['system', 'user', 'assistant']:
                        errors.append(f"Line {line_num}: Invalid role: {msg['role']}")
                    
                    stats[f"role_{msg['role']}"] += 1
                
            except json.JSONDecodeError:
                errors.append(f"Line {line_num}: Invalid JSON")
    
    return {
        'errors': errors,
        'stats': dict(stats)
    }

# Usage
validation_result = validate_finetuning_data('training_data.jsonl')
print(f"Validation complete: {validation_result['stats']['total_entries']} entries")
if validation_result['errors']:
    print(f"Errors found: {len(validation_result['errors'])}")
    for error in validation_result['errors'][:10]:  # Show first 10 errors
        print(f"  - {error}")
```

### 3. Upload and Prepare Training
Upload data to OpenAI and start fine-tuning.

```python
from openai import OpenAI

client = OpenAI()

# Upload training file
with open('training_data.jsonl', 'rb') as f:
    upload_response = client.files.create(
        file=f,
        purpose='fine-tune'
    )

training_file_id = upload_response.id
print(f"File uploaded: {training_file_id}")

# Create fine-tuning job
fine_tune_job = client.fine_tuning.jobs.create(
    training_file=training_file_id,
    model="gpt-3.5-turbo",
    hyperparameters={
        "n_epochs": 3,
        "batch_size": 4,
        "learning_rate_multiplier": 0.1
    }
)

job_id = fine_tune_job.id
print(f"Fine-tuning job started: {job_id}")
```

### 4. Monitor Training Progress
Track the fine-tuning process.

```python
def check_finetuning_status(job_id):
    """Check the status of a fine-tuning job."""
    job = client.fine_tuning.jobs.retrieve(job_id)
    
    status = {
        'status': job.status,
        'created_at': job.created_at,
        'finished_at': job.finished_at,
        'model': job.fine_tuned_model,
        'error': job.error
    }
    
    if job.result_files:
        # Retrieve training metrics
        result_file = client.files.retrieve(job.result_files[0])
        print(f"Results file: {result_file.id}")
    
    return status

# Usage
import time

while True:
    status = check_finetuning_status(job_id)
    print(f"Status: {status['status']}")
    
    if status['status'] in ['succeeded', 'failed', 'cancelled']:
        break
    
    time.sleep(60)  # Check every minute
```

### 5. Use the Fine-Tuned Model
Deploy and use your custom model.

```python
def use_finetuned_model(model_id, prompt):
    """Use the fine-tuned model for inference."""
    response = client.chat.completions.create(
        model=model_id,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# After training completes
fine_tuned_model = status['model']

# Test the model
test_prompt = "Review this contract clause: 'Employee shall not compete for 2 years after termination.'"
result = use_finetuned_model(fine_tuned_model, test_prompt)
print(result)
```

### 6. Evaluate Model Performance
Assess the quality of your fine-tuned model.

```python
def evaluate_model(model_id, test_data):
    """Evaluate fine-tuned model on test set."""
    results = []
    
    for test_case in test_data:
        # Get model response
        response = use_finetuned_model(model_id, test_case['input'])
        
        # Compare with expected output
        results.append({
            'input': test_case['input'],
            'expected': test_case['expected'],
            'actual': response,
            'match': test_case['expected'].lower() in response.lower()
        })
    
    # Calculate metrics
    accuracy = sum(r['match'] for r in results) / len(results)
    
    return {
        'accuracy': accuracy,
        'results': results
    }

# Test dataset
test_data = [
    {
        'input': 'Is this termination clause fair?',
        'expected': 'fair'  # or 'unfair'
    }
    # ... more test cases
]

evaluation = evaluate_model(fine_tuned_model, test_data)
print(f"Accuracy: {evaluation['accuracy']:.2%}")
```

## Constraints
- **Minimum Data**: Need at least 10-100 examples for meaningful fine-tuning
- **Data Quality**: Garbage in, garbage out - ensure high-quality training data
- **Cost**: Fine-tuning can be expensive, especially with large datasets
- **Overfitting**: Monitor for overfitting to training data
- **Hallucination**: Fine-tuned models may still hallucinate facts
- **Maintenance**: Models may need periodic retraining as data evolves

## Expected Output
A specialized model that performs better on your specific domain tasks compared to base models, with consistent formatting and domain-specific knowledge.

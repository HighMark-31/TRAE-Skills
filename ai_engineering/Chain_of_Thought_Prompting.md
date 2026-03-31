# Skill: Chain of Thought Prompting

## Purpose
To improve LLM reasoning performance by encouraging models to show their work and think through problems step-by-step before arriving at an answer.

## When to Use
- When solving complex math or logic problems
- When reasoning through multi-step questions
- When you need to verify the model's thinking process
- When working with problems requiring inference

## Procedure

### 1. Basic Chain of Thought
Structure your prompt to encourage step-by-step reasoning.

```python
from openai import OpenAI

client = OpenAI()

prompt = """
Question: If a store sells apples for $2 each and oranges for $3 each, 
and you buy 5 apples and 3 oranges, how much do you spend?

Let's think step by step:
1. Calculate the cost of apples: 5 apples × $2 = $10
2. Calculate the cost of oranges: 3 oranges × $3 = $9
3. Add both amounts: $10 + $9 = $19

Answer: $19

Question: A train travels 120 miles in 2 hours. If it maintains the same speed, 
how far will it travel in 5 hours?

Let's think step by step:
"""

response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}]
)
print(response.choices[0].message.content)
```

### 2. Zero-Shot Chain of Thought
Simply add "Let's think step by step" to your prompt.

```python
def zero_shot_cot(question):
    prompt = f"""Question: {question}

Let's think step by step:"""
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Example
question = "If 3 workers can build a wall in 4 days, how many days will 6 workers need?"
print(zero_shot_cot(question))
```

### 3. Few-Shot Chain of Thought
Provide examples of the reasoning process.

```python
few_shot_prompt = """
Q: Roger has 5 tennis balls. He buys 2 more cans of 3 tennis balls each. 
How many tennis balls does he have now?
A: Roger started with 5 balls. 2 cans of 3 tennis balls each is 6 tennis balls. 
5 + 6 = 11. The answer is 11.

Q: A restaurant had 23 apples. If they used 20 to make lunch and bought 6 more, 
how many apples do they have?
A: They had 23 apples and used 20, so 23 - 20 = 3. Then they bought 6 more, 
so 3 + 6 = 9. The answer is 9.

Q: If a car travels 60 miles per hour for 3 hours, how far does it travel?
A:"""

response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": few_shot_prompt}]
)
print(response.choices[0].message.content)
```

### 4. Self-Consistency with Chain of Thought
Generate multiple reasoning paths and take the majority answer.

```python
import numpy as np

def self_consistent_cot(question, num_samples=5):
    responses = []
    for _ in range(num_samples):
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": f"Question: {question}\nLet's think step by step:"}],
            temperature=0.7  # Add randomness for diverse paths
        )
        responses.append(response.choices[0].message.content)
    
    # Parse final answers from responses
    answers = [r.split("Answer:")[-1].strip() if "Answer:" in r else r for r in responses]
    
    # Return most common answer
    from collections import Counter
    most_common = Counter(answers).most_common(1)[0][0]
    return most_common

# Example
question = "A bat and ball cost $1.10 in total. The bat costs $1.00 more than the ball. How much does the ball cost?"
answer = self_consistent_cot(question)
print(f"Final answer: {answer}")
```

### 5. Structured Chain of Thought
Use specific reasoning templates for different problem types.

```python
math_template = """
Solve this math problem systematically:

1. Identify the given information
2. Identify what needs to be found
3. Determine the appropriate formula or approach
4. Execute the calculation
5. Verify the answer

Question: {question}

Answer:"""

coding_template = """
Debug this code step by step:

1. Understand what the code should do
2. Trace through the execution line by line
3. Identify where the behavior differs from expectations
4. Propose and test fixes

Code: {code}

Issue: {issue}

Fix:"""

def structured_cot(template, **kwargs):
    prompt = template.format(**kwargs)
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
```

## Constraints
- **Token Usage**: Chain of thought increases token consumption significantly
- **Latency**: More tokens = longer response times
- **Model Selection**: Works best with larger models (GPT-4, Claude)
- **Temperature**: Use lower temperature (0-0.3) for more consistent reasoning
- **Verification**: Always verify the reasoning steps, especially for critical applications

## Expected Output
Improved reasoning performance on complex problems that require multi-step thinking, with transparent thought processes that can be verified and debugged.

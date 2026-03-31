# Skill: Structured Output Parsing

## Purpose
To force LLMs to output data in specific, parseable formats like JSON, enabling reliable integration with applications and automated workflows.

## When to Use
- When building APIs that need structured responses
- When extracting data from unstructured text
- When generating code, configuration files, or data formats
- When requiring consistent output formatting for downstream processing

## Procedure

### 1. Basic JSON Output
Request JSON format in your prompt.

```python
from openai import OpenAI
import json

client = OpenAI()

def get_json_response(prompt, schema_description):
    """Get structured JSON response from LLM."""
    full_prompt = f"""
    {prompt}
    
    Provide your response as a JSON object following this structure:
    {schema_description}
    
    Return only the JSON, no additional text.
    """
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": full_prompt}],
        temperature=0  # Lower temperature for more consistent structure
    )
    
    # Parse JSON response
    try:
        return json.loads(response.choices[0].message.content)
    except json.JSONDecodeError:
        # Fallback: ask model to fix the JSON
        return fix_json_parse(response.choices[0].message.content)

# Example usage
person_info = get_json_response(
    "Extract information from: 'John Doe is a 35-year-old software engineer from New York.'",
    """
    {
        "name": "string",
        "age": "number",
        "occupation": "string",
        "location": "string"
    }
    """
)
print(person_info)
```

### 2. Pydantic Models for Validation
Use Pydantic for robust schema validation.

```python
from pydantic import BaseModel, Field
from typing import List, Optional

class Person(BaseModel):
    name: str = Field(description="Full name of the person")
    age: int = Field(description="Age in years", ge=0, le=150)
    occupation: str = Field(description="Job title or occupation")
    location: Optional[str] = Field(default=None, description="City or location")

class ProductReview(BaseModel):
    product_name: str
    rating: int = Field(ge=1, le=5)
    review_text: str
    pros: List[str]
    cons: List[str]
    would_recommend: bool

def extract_structured_data(text, model_class):
    """Extract structured data using Pydantic model."""
    schema = model_class.model_json_schema()
    
    prompt = f"""
    Extract information from the following text and return it as JSON:
    
    Text: {text}
    
    Return JSON matching this schema:
    {json.dumps(schema, indent=2)}
    
    Return only the JSON, no additional text.
    """
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    
    try:
        data = json.loads(response.choices[0].message.content)
        return model_class(**data)
    except Exception as e:
        print(f"Error parsing response: {e}")
        return None

# Example usage
review_text = """
I bought the Acme Widget Pro last month. Overall I'd give it 4 stars.
The build quality is excellent and battery life is amazing.
However, the price is quite high and the app interface is confusing.
Despite these issues, I would recommend it to others.
"""

review = extract_structured_data(review_text, ProductReview)
if review:
    print(f"Product: {review.product_name}")
    print(f"Rating: {review.rating}/5")
    print(f"Pros: {', '.join(review.pros)}")
```

### 3. Few-Shot JSON Examples
Provide examples to improve JSON formatting.

```python
def extract_with_few_shots(text):
    """Extract structured data with few-shot examples."""
    prompt = """
    Example 1:
    Input: "Sarah Connor, 28, works as a data analyst in Boston."
    Output: {"name": "Sarah Connor", "age": 28, "occupation": "data analyst", "location": "Boston"}
    
    Example 2:
    Input: "Mike Ross is a 32-year-old lawyer from New York."
    Output: {"name": "Mike Ross", "age": 32, "occupation": "lawyer", "location": "New York"}
    
    Example 3:
    Input: "Emily Chen, 25, graphic designer, San Francisco"
    Output: {"name": "Emily Chen", "age": 25, "occupation": "graphic designer", "location": "San Francisco"}
    
    Now extract from this input:
    Input: "{text}"
    Output:"""
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    
    return json.loads(response.choices[0].message.content)

# Usage
result = extract_with_few_shots("James Wilson, 42, architect, Chicago")
print(result)
```

### 4. Structured Output with Function Calling
Use function calling for guaranteed structured output.

```python
def structured_output_with_functions(text):
    """Use function calling for structured output."""
    function_def = {
        "name": "extract_person_info",
        "description": "Extract person information from text",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"},
                "occupation": {"type": "string"},
                "location": {"type": "string"}
            },
            "required": ["name", "age", "occupation"]
        }
    }
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{
            "role": "user",
            "content": f"Extract person information from: {text}"
        }],
        functions=[function_def],
        function_call={"name": "extract_person_info"}
    )
    
    function_call = response.choices[0].message.function_call
    return json.loads(function_call.arguments)

# Example
person = structured_output_with_functions(
    "Dr. Lisa Anderson, 38, cardiologist at Mayo Clinic, Rochester"
)
print(person)
```

### 5. Complex Nested Structures
Handle complex nested JSON structures.

```python
class Company(BaseModel):
    name: str
    founded_year: int
    headquarters: str
    employees: List[str]
    departments: dict

def extract_company_info(text):
    """Extract complex nested company information."""
    prompt = f"""
    Extract company information from the following text and return it as JSON.
    Include all employees mentioned and their departments.
    
    Text: {text}
    
    Return JSON matching this structure:
    {json.dumps(Company.model_json_schema(), indent=2)}
    
    Return only valid JSON.
    """
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    
    try:
        data = json.loads(response.choices[0].message.content)
        return Company(**data)
    except Exception as e:
        print(f"Error: {e}")
        return None

# Example
company_text = """
TechCorp Inc. was founded in 2010 and is headquartered in Austin, Texas.
The company has three main departments: Engineering, Sales, and Marketing.
Key employees include:
- John Smith (CEO, Engineering department)
- Sarah Johnson (VP of Sales)
- Michael Chen (CTO, Engineering)
- Emily Davis (Marketing Director)
"""

company = extract_company_info(company_text)
if company:
    print(f"Company: {company.name}")
    print(f"Departments: {company.departments.keys()}")
```

### 6. Error Recovery and Retry Logic
Implement robust error handling for JSON parsing.

```python
def extract_with_retry(text, model_class, max_retries=3):
    """Extract structured data with retry logic."""
    schema = model_class.model_json_schema()
    
    for attempt in range(max_retries):
        prompt = f"""
        Extract information as JSON following this schema:
        {json.dumps(schema, indent=2)}
        
        Text: {text}
        
        {'Only return the JSON object, no other text.' if attempt == 0 else 'Your previous response was not valid JSON. Please ensure you return ONLY a valid JSON object, nothing else.'}
        """
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        
        try:
            data = json.loads(response.choices[0].message.content)
            return model_class(**data)
        except Exception as e:
            if attempt == max_retries - 1:
                print(f"Failed after {max_retries} attempts: {e}")
                return None
            print(f"Attempt {attempt + 1} failed, retrying...")
```

## Constraints
- **Model Consistency**: Not all models follow instructions perfectly - use function calling when possible
- **Temperature**: Use low temperature (0-0.3) for more consistent formatting
- **Complexity**: Very complex structures may require multiple extraction steps
- **Validation**: Always validate parsed data before using it
- **Error Handling**: Implement robust error handling for malformed responses
- **Token Limits**: Large schemas consume tokens - keep them as minimal as possible

## Expected Output
Reliable structured data extraction from unstructured text, with properly validated and typed results that can be directly used in applications.

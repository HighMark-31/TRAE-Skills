# Skill: Function Calling

## Purpose
To enable LLMs to interact with external tools, APIs, and databases by defining structured function specifications that models can intelligently invoke.

## When to Use
- When building AI assistants that need to perform actions
- When integrating LLMs with existing APIs
- When requiring structured data extraction
- When implementing multi-step workflows with external systems

## Procedure

### 1. Define Function Schemas
Create structured function definitions with clear descriptions.

```python
from openai import OpenAI

client = OpenAI()

# Define available functions
functions = [
    {
        "name": "get_weather",
        "description": "Get the current weather for a specific location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA"
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "description": "The temperature unit"
                }
            },
            "required": ["location"]
        }
    },
    {
        "name": "search_database",
        "description": "Search a database for specific records",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query"
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of results to return"
                }
            },
            "required": ["query"]
        }
    }
]
```

### 2. Implement the Functions
Create actual implementations of your defined functions.

```python
import requests

def get_weather(location, unit="celsius"):
    """Get weather data for a location."""
    # Example using a weather API
    api_url = f"https://api.weatherapi.com/v1/current.json"
    params = {
        "key": "your-api-key",
        "q": location,
        "aqi": "no"
    }
    
    try:
        response = requests.get(api_url, params=params)
        data = response.json()
        
        temp = data['current']['temp_c'] if unit == "celsius" else data['current']['temp_f']
        condition = data['current']['condition']['text']
        
        return {
            "location": location,
            "temperature": temp,
            "unit": unit,
            "condition": condition
        }
    except Exception as e:
        return {"error": str(e)}

def search_database(query, limit=10):
    """Search database for records."""
    # Example database query
    # In production, use your actual database connection
    results = [
        {"id": 1, "title": f"Result for {query}", "content": "..."},
        {"id": 2, "title": f"Another result for {query}", "content": "..."}
    ]
    return results[:limit]

# Map function names to implementations
function_map = {
    "get_weather": get_weather,
    "search_database": search_database
}
```

### 3. Handle Function Calls
Process LLM responses that request function calls.

```python
def execute_function_call(function_call):
    """Execute a function call from the LLM."""
    function_name = function_call.name
    function_args = json.loads(function_call.arguments)
    
    print(f"Calling function: {function_name}")
    print(f"Arguments: {function_args}")
    
    if function_name in function_map:
        function_to_call = function_map[function_name]
        return function_to_call(**function_args)
    else:
        return f"Error: Function {function_name} not found"
```

### 4. Complete Conversation Flow
Implement the full interaction loop.

```python
def chat_with_functions(user_message, messages_history=None):
    """Handle conversation with function calling."""
    if messages_history is None:
        messages_history = []
    
    # Add user message to history
    messages_history.append({"role": "user", "content": user_message})
    
    # Make API call with functions
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages_history,
        functions=functions,
        function_call="auto"  # Let model decide whether to call functions
    )
    
    response_message = response.choices[0].message
    
    # Check if model wants to call a function
    if response_message.function_call:
        print(f"Model wants to call: {response_message.function_call.name}")
        
        # Execute function call
        function_response = execute_function_call(response_message.function_call)
        
        # Add function response to conversation
        messages_history.append(response_message)  # Assistant message with function call
        messages_history.append({
            "role": "function",
            "name": response_message.function_call.name,
            "content": json.dumps(function_response)
        })
        
        # Get final response from model
        second_response = client.chat.completions.create(
            model="gpt-4",
            messages=messages_history
        )
        
        return second_response.choices[0].message.content
    else:
        return response_message.content

# Usage
messages = []
while True:
    user_input = input("You: ")
    if user_input.lower() in ['quit', 'exit']:
        break
    
    response = chat_with_functions(user_input, messages)
    print(f"Assistant: {response}")
    messages.append({"role": "assistant", "content": response})
```

### 5. Advanced: Parallel Function Calls
Handle multiple function calls in a single request.

```python
def handle_parallel_function_calls(response_message, messages_history):
    """Handle multiple function calls from the model."""
    # Some models can request multiple function calls at once
    if hasattr(response_message, 'function_calls'):
        function_calls = response_message.function_calls
    else:
        # Single function call (convert to list for uniform handling)
        if response_message.function_call:
            function_calls = [response_message.function_call]
        else:
            return messages_history
    
    # Add assistant message with function calls
    messages_history.append(response_message)
    
    # Execute all function calls
    for function_call in function_calls:
        function_response = execute_function_call(function_call)
        
        # Add each function response
        messages_history.append({
            "role": "function",
            "name": function_call.name,
            "content": json.dumps(function_response)
        })
    
    return messages_history
```

### 6. Error Handling and Validation
Add robust error handling for function calls.

```python
def safe_execute_function_call(function_call):
    """Execute function call with error handling."""
    function_name = function_call.name
    
    try:
        function_args = json.loads(function_call.arguments)
    except json.JSONDecodeError as e:
        return {
            "error": f"Invalid JSON in arguments: {str(e)}",
            "arguments": function_call.arguments
        }
    
    # Validate function exists
    if function_name not in function_map:
        return {
            "error": f"Unknown function: {function_name}",
            "available_functions": list(function_map.keys())
        }
    
    # Validate required parameters
    function_schema = next((f for f in functions if f["name"] == function_name), None)
    if function_schema:
        required_params = function_schema["parameters"].get("required", [])
        missing_params = [p for p in required_params if p not in function_args]
        
        if missing_params:
            return {
                "error": f"Missing required parameters: {', '.join(missing_params)}",
                "provided": list(function_args.keys())
            }
    
    # Execute function
    try:
        function_to_call = function_map[function_name]
        return function_to_call(**function_args)
    except Exception as e:
        return {
            "error": f"Function execution failed: {str(e)}",
            "function": function_name,
            "arguments": function_args
        }
```

## Constraints
- **Function Descriptions**: Clear, detailed descriptions are crucial for model performance
- **Parameter Validation**: Always validate function arguments before execution
- **Error Handling**: Gracefully handle function failures and API errors
- **Security**: Validate and sanitize all inputs, especially for database operations
- **Rate Limiting**: Implement rate limits for external API calls
- **Token Limits**: Function calls consume tokens - consider size of function schemas and responses

## Expected Output
An intelligent AI assistant capable of understanding user intent and automatically executing appropriate functions to fulfill requests, with proper error handling and response formatting.

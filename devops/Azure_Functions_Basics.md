# Skill: Azure Functions Basics

## Purpose
To use serverless on Azure.

## When to Use
- Bindings and triggers.
- When the specific requirement for Azure Functions Basics arises in the project.

## Procedure

### 1. Project Initialization
Create a new Azure Functions project using the CLI.

```bash
# Install tools
npm install -g azure-functions-core-tools@4

# Initialize project (Node.js/TypeScript)
func init MyFunctionProj --typescript
cd MyFunctionProj

# Create a specific function (HTTP Trigger)
func new --name MyHttpTrigger --template "HTTP trigger" --authlevel "anonymous"
```

### 2. Defining Triggers and Bindings
Edit `function.json` (or use decorators in v4+) to define how the function is invoked.

```typescript
// v4 Node.js model (index.ts)
import { app, HttpRequest, HttpResponseInit, InvocationContext } from "@azure/functions";

export async function MyHttpTrigger(request: HttpRequest, context: InvocationContext): HttpResponseInit {
    context.log(`Http function processed request for url "${request.url}"`);

    const name = request.query.get('name') || await request.text() || 'world';

    return { body: `Hello, ${name}!` };
};

app.http('MyHttpTrigger', {
    methods: ['GET', 'POST'],
    authLevel: 'anonymous',
    handler: MyHttpTrigger
});
```

### 3. Local Testing
Run the function locally before deploying.

```bash
npm start
# Function will be available at http://localhost:7071/api/MyHttpTrigger
```

### 4. Deployment
Deploy to Azure using the CLI or GitHub Actions.

```bash
# Via CLI
func azure functionapp publish <FunctionAppName>
```

## Constraints
- **Cold Starts**: Be aware of latency for the first request after inactivity on "Consumption" plans.
- **Statelessness**: Functions must be stateless. Use Azure Durable Functions if you need state/orchestration.
- **Execution Limit**: Consumption plan functions have a default timeout of 5 minutes (max 10).

## Expected Output
A serverless function deployed to Azure that responds to triggers (HTTP, Timer, Queue) without managing underlying server infrastructure.

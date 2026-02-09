# Skill: Serverless Framework Setup

## Purpose
To deploy serverless apps easily.

## When to Use
- serverless.yml configuration.
- When the specific requirement for Serverless Framework Setup arises in the project.

## Procedure

### 1. Installation and Configuration
Install the Serverless CLI and configure your cloud provider credentials.

```bash
npm install -g serverless

# Configure AWS credentials
serverless config credentials --provider aws --key <YOUR_KEY> --secret <YOUR_SECRET>
```

### 2. Creating a Service
Initialize a new project from a template.

```bash
serverless create --template aws-nodejs-typescript --path my-service
cd my-service
npm install
```

### 3. Configuring `serverless.yml`
Define your infrastructure and functions in the configuration file.

```yaml
service: my-backend

provider:
  name: aws
  runtime: nodejs18.x
  region: us-east-1
  stage: ${opt:stage, 'dev'}
  environment:
    DATABASE_URL: ${env:DATABASE_URL}

functions:
  createUser:
    handler: handler.createUser
    events:
      - http:
          path: users
          method: post
          cors: true

plugins:
  - serverless-offline # For local development
  - serverless-esbuild # For fast bundling
```

### 4. Deployment
Deploy your service to the cloud.

```bash
# Deploy to the default stage (dev)
serverless deploy

# Deploy to production
serverless deploy --stage prod
```

## Constraints
- **Function Size**: Keep function bundles small (use `esbuild` or `webpack`) to minimize cold start times.
- **Permissions**: Use the principle of least privilege for IAM roles assigned to functions.
- **VPC Latency**: Be careful when placing Lambda functions inside a VPC, as it can increase cold start times (though improved in recent years).

## Expected Output
A set of cloud resources (Lambda, API Gateway, IAM roles) deployed and managed via the Serverless Framework.

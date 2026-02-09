# Skill: Docker Containerization (Node.js)

## Purpose
To package a Node.js application and its dependencies into a lightweight, portable container image that runs consistently across any environment.

## When to Use
- When preparing an application for production deployment.
- When ensuring development environment consistency.
- When isolating microservices in a cluster (Kubernetes/ECS).

## Procedure

### 1. Multi-Stage Dockerfile (TypeScript/Build)
Use multi-stage builds to keep the final production image as small as possible.

```dockerfile
# Stage 1: Build
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Production
FROM node:20-alpine
WORKDIR /app
ENV NODE_ENV=production

# Install only production dependencies
COPY package*.json ./
RUN npm ci --only=production

# Copy built assets from builder stage
COPY --from=builder /app/dist ./dist

# Security: Run as non-root user
USER node

EXPOSE 3000
CMD ["node", "dist/index.js"]
```

### 2. .dockerignore Configuration
Prevent unnecessary files from bloating the build context.

```text
node_modules
npm-debug.log
dist
.git
.env
Dockerfile
.dockerignore
```

### 3. Docker Compose for Development
Simplify local development with linked services.

```yaml
# docker-compose.yml
services:
  app:
    build: 
      context: .
      dockerfile: Dockerfile.dev
    ports:
      - "3000:3000"
    volumes:
      - .:/app
      - /app/node_modules
    environment:
      - DATABASE_URL=postgres://user:pass@db:5432/db
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      - POSTGRES_PASSWORD=pass
```

### 4. Building and Running
Commands for the CLI.

```bash
# Build the image
docker build -t my-app:v1 .

# Run the container
docker run -p 3000:3000 --env-file .env my-app:v1
```

## Constraints
- **Base Image**: Always use `alpine` or `slim` tags for smaller, more secure images.
- **Layer Caching**: Copy `package.json` and install dependencies **before** copying the rest of the source code to leverage Docker layer caching.
- **Security**: Never include `.env` files or hardcoded secrets in the image. Use environment variables at runtime.

## Expected Output
A production-ready `Dockerfile` that produces a minimal, secure image containing only the necessary runtime files.

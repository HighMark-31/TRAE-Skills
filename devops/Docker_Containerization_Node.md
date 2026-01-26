# Skill: Docker Containerization (Node.js)

## Purpose
To package a Node.js application and its dependencies into a lightweight, portable container image that runs consistently across any environment.

## When to Use
- When preparing an application for deployment.
- When ensuring development environment consistency (devcontainers).
- When isolating microservices.

## Procedure
1.  **Create Dockerfile**: Create a `Dockerfile` in the project root.
2.  **Select Base Image**: Use a specific, lightweight version (e.g., `node:20-alpine`).
3.  **Set Working Directory**: `WORKDIR /app`.
4.  **Install Dependencies**:
    - Copy `package.json` and `package-lock.json`.
    - Run `npm ci --only=production` (for prod images).
5.  **Copy Source Code**: Copy the rest of the application code (`COPY . .`).
6.  **Build (if needed)**: Run build scripts (e.g., TypeScript compilation).
7.  **Expose Port**: `EXPOSE <PORT>`.
8.  **Define Command**: `CMD ["node", "dist/index.js"]`.
9.  **Create .dockerignore**: Exclude `node_modules`, `.git`, `.env`, and logs.

## Constraints
- Do NOT run the container as root (use `USER node`).
- Minimize image layers by chaining commands where possible.
- Use multi-stage builds for TypeScript/compilation steps to keep the final image small.

## Expected Output
A `Dockerfile` and `.dockerignore` file that allows building a functional Docker image using `docker build`.

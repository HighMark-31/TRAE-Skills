# Skill: Nginx Reverse Proxy Setup

## Purpose
To sit in front of backend applications, handling SSL termination, load balancing, compression, and static file serving.

## When to Use
- Exposing a Node.js app to the internet.
- Hosting multiple domains on one server.
- Improving security and performance.

## Procedure
1.  **Install Nginx**: `apt-get install nginx`.
2.  **Configure Server Block**: Create `/etc/nginx/sites-available/myapp`.
3.  **Upstream**: Define the backend: `upstream backend { server localhost:3000; }`.
4.  **Proxy Pass**:
    - `location / { proxy_pass http://backend; proxy_set_header Host $host; ... }`.
5.  **Security Headers**: Add `X-Frame-Options`, `X-Content-Type-Options`, `HSTS`.
6.  **Enable**: Symlink to `sites-enabled` and test config: `nginx -t`.
7.  **Reload**: `systemctl reload nginx`.

## Constraints
- Always pass the real client IP (`X-Forwarded-For`) to the backend.
- Disable server tokens (`server_tokens off;`) to hide Nginx version.
- Tune worker processes for high loads.

## Expected Output
A configured Nginx server routing traffic to the application, handling HTTP/HTTPS correctly.

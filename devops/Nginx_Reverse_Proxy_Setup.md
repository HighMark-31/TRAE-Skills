# Skill: Nginx Reverse Proxy Setup

## Purpose
To sit in front of backend applications, handling SSL termination, load balancing, compression, and static file serving.

## When to Use
- Exposing a Node.js app to the internet.
- Hosting multiple domains on one server.
- Improving security and performance.

## Procedure

### 1. Basic Server Block Configuration
Create a configuration file in `/etc/nginx/sites-available/myapp.conf`.

```nginx
upstream myapp_upstream {
    server 127.0.0.1:3000;
    keepalive 64;
}

server {
    listen 80;
    server_name example.com www.example.com;

    # Redirect all HTTP traffic to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name example.com www.example.com;

    # SSL Configuration (assuming Certbot paths)
    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

    # Performance & Security
    client_max_body_size 20M;
    server_tokens off;

    location / {
        proxy_pass http://myapp_upstream;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Static Assets Caching
    location /static/ {
        alias /var/www/myapp/static/;
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }
}
```

### 2. Enabling the Configuration
Link the file to the enabled sites directory and test the configuration.

```bash
# Enable the site
ln -s /etc/nginx/sites-available/myapp.conf /etc/nginx/sites-enabled/

# Test configuration syntax
nginx -t

# Reload Nginx to apply changes
systemctl reload nginx
```

### 3. Adding Security Headers
Include common security headers in the `server` block or a separate snippet.

```nginx
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header X-Content-Type-Options "nosniff" always;
add_header Referrer-Policy "no-referrer-when-downgrade" always;
add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
```

## Constraints
- **IP Forwarding**: Always pass the real client IP (`X-Forwarded-For`) to ensure backend logs and rate limiting work correctly.
- **Header Limits**: Be careful with `proxy_buffer_size` if your app sends large headers (e.g., heavy JWTs).
- **Security**: Disable server tokens (`server_tokens off;`) to avoid leaking the Nginx version to attackers.
- **Permissions**: Ensure the `nginx` user has read access to static asset directories.

## Expected Output
A configured Nginx server routing traffic to the application, handling HTTP/HTTPS correctly.

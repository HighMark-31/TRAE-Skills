# Skill: SSL/TLS Certificate Management (Certbot)

## Purpose
To secure communication between clients and the server using HTTPS, obtaining free certificates from Let's Encrypt and automating renewal.

## When to Use
- Any public-facing web service.
- Compliance requirements (PCI-DSS).

## Procedure

### 1. Installation of Certbot and Nginx Plugin
Install the necessary packages for your OS (Ubuntu/Debian example).

```bash
sudo apt update
sudo apt install certbot python3-certbot-nginx
```

### 2. Obtaining and Installing the Certificate
Run Certbot to automatically fetch the certificate and configure Nginx.

```bash
# Request certificate for a single domain
sudo certbot --nginx -d example.com -d www.example.com

# Follow the prompts:
# 1. Enter email for renewal notifications
# 2. Agree to Terms of Service
# 3. Choose whether to redirect HTTP to HTTPS (Recommended: Yes)
```

### 3. Manual Certificate Generation (DNS Challenge)
If you are using a wildcard certificate or don't have port 80 open.

```bash
sudo certbot certonly --manual --preferred-challenges dns -d "*.example.com" -d "example.com"

# You will need to add a TXT record to your DNS provider as instructed
```

### 4. Verifying and Testing Auto-Renewal
Certbot usually adds a systemd timer or cron job automatically.

```bash
# Test the renewal process without making changes
sudo certbot renew --dry-run

# Check systemd timer status
systemctl status certbot.timer
```

### 5. Nginx Configuration Check
Ensure the generated configuration in `/etc/nginx/sites-available/` looks correct.

```nginx
server {
    listen 443 ssl; # managed by Certbot
    server_name example.com;

    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot
}
```

## Constraints
- **Domain Resolution**: The domain must point to the server's public IP before running Certbot.
- **Port 80**: Must be open and not used by another process (unless using the `--nginx` plugin which handles this).
- **Rate Limits**: Let's Encrypt has strict limits (e.g., 50 certificates per registered domain per week).
- **Security**: Protect the `/etc/letsencrypt/` directory; it contains your private keys.

## Expected Output
A secured website with a valid, auto-renewing SSL certificate.

# Skill: SSL/TLS Certificate Management (Certbot)

## Purpose
To secure communication between clients and the server using HTTPS, obtaining free certificates from Let's Encrypt and automating renewal.

## When to Use
- Any public-facing web service.
- Compliance requirements (PCI-DSS).

## Procedure
1.  **Install Certbot**: `apt-get install certbot python3-certbot-nginx`.
2.  **Obtain Cert**: Run `certbot --nginx -d example.com`.
3.  **Verification**: Certbot validates domain ownership (HTTP-01 challenge).
4.  **Configuration**: Certbot automatically modifies Nginx config to use the new certs and force HTTPS redirect.
5.  **Auto-Renewal**: Verify the cron job/timer is active: `systemctl list-timers | grep certbot`.
6.  **Test**: Visit `https://example.com` and check the padlock.

## Constraints
- Rate limits apply (5 duplicate certs per week).
- Port 80 must be open for the challenge to work.
- Backup the `/etc/letsencrypt` directory.

## Expected Output
A secured website with a valid, auto-renewing SSL certificate.

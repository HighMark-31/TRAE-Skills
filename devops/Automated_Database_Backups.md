# Skill: Automated Database Backups

## Purpose
To ensure data is preserved and recoverable in case of corruption, accidental deletion, or catastrophic failure.

## When to Use
- Always. For every production database.

## Procedure
1.  **Scripting**: Write a script (bash/python) to run `pg_dump` (Postgres) or `mysqldump`.
    - `pg_dump -h $HOST -U $USER $DB | gzip > backup.sql.gz`.
2.  **Upload**: Stream or upload the file to offsite storage (AWS S3, Google Cloud Storage).
    - `aws s3 cp backup.sql.gz s3://my-backups/$(date +%F)/`.
3.  **Scheduling**: Add to crontab: `0 2 * * * /path/to/backup.sh` (Runs at 2 AM).
4.  **Retention Policy**: Configure S3 Lifecycle Rules to delete backups older than X days.
5.  **Verification**: **Crucial**. Regularly attempt to restore a backup to a test DB to ensure it works.

## Constraints
- Encrypt backups at rest.
- Do not store backups on the same server as the database.
- Monitor the backup job (alert if it fails).

## Expected Output
A reliable, automated system that produces daily/hourly backups stored securely offsite.

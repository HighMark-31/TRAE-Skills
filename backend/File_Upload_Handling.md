# Skill: File Upload Handling (Multer/S3)

## Purpose
To securely accept file uploads from users, validate them, and store them in a durable object storage service (like AWS S3), keeping the application server stateless.

## When to Use
- User avatar uploads.
- Document attachments.
- Media processing pipelines.

## Procedure
1.  **Configure Middleware**: Use `multer` to handle `multipart/form-data`.
2.  **Validate File**:
    - Check file type (MIME type) against whitelist.
    - Check file size against limit.
3.  **Process Upload**:
    - Stream file directly to storage (S3) using `multer-s3` (avoid saving to local disk in production).
    - Generate a unique filename (UUID + extension) to prevent collisions.
4.  **Save Metadata**: Store the file URL/Key and metadata in the database linked to the resource.
5.  **Cleanup**: If validation fails during the process, ensure partial uploads are cleaned up.

## Constraints
- Do not store files in the database (BLOBs) unless very small.
- Do not store user files on the application server filesystem (ephemeral).
- Scan files for viruses if possible.

## Expected Output
An API endpoint that accepts a file, validates it, uploads it to cloud storage, and returns the file URL.

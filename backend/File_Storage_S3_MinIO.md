# Skill: File Storage (S3/MinIO)

## Purpose
To securely store, retrieve, and serve user-uploaded files (images, documents) using Object Storage, separating binary data from the database.

## When to Use
- Storing user avatars, post images, or PDFs.
- When local disk storage is not scalable (e.g., stateless containers).

## Procedure

### 1. Setup
- **AWS S3**: Create Bucket, create IAM User with `PutObject`/`GetObject` permissions.
- **MinIO**: Self-hosted S3-compatible alternative (great for dev/on-prem).

### 2. SDK Integration (AWS SDK v3)
```javascript
const { S3Client, PutObjectCommand } = require('@aws-sdk/client-s3');
const s3 = new S3Client({ region: 'us-east-1', credentials: { ... } });
```

### 3. Upload Strategy
**A. Presigned URLs (Recommended)**
Client uploads directly to S3. Server generates a temporary signature. Saves server bandwidth.
1.  Server:
    ```javascript
    const { getSignedUrl } = require('@aws-sdk/s3-request-presigner');
    const command = new PutObjectCommand({ Bucket: 'my-bucket', Key: 'file.jpg' });
    const url = await getSignedUrl(s3, command, { expiresIn: 3600 });
    // Send url to client
    ```
2.  Client: PUT binary data to that URL.

**B. Server-Side Upload**
Client -> Server -> S3. Easier to validate content, but heavy on server.

### 4. Security
- **Bucket Policy**: Block public access.
- **Serving Files**: Use CloudFront (CDN) with Signed URLs for private content, or public read access for public assets.

## Constraints
- **Filename Collisions**: Always generate unique keys (e.g., `uuid-filename.ext`).
- **Validation**: Validate mime-type and file size before generating presigned URLs.

## Expected Output
Scalable, durable file storage system with secure access controls and offloaded bandwidth usage.

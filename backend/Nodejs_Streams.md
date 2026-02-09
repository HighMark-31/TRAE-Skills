# Skill: Node.js Streams

## Purpose
To handle data efficiently in Node.js by processing it piece-by-piece (chunks) rather than loading everything into memory at once.

## When to Use
- Reading/Writing large files (GBs in size).
- Processing HTTP requests/responses (e.g., video streaming, file uploads).
- Transformative pipelines (compression, encryption).

## Procedure

### 1. Readable Streams
Read data from a source.
```javascript
const fs = require('fs');
const readable = fs.createReadStream('big-file.txt', { encoding: 'utf8' });

readable.on('data', (chunk) => {
  console.log(`Received ${chunk.length} bytes`);
});
```

### 2. Writable Streams
Write data to a destination.
```javascript
const writable = fs.createWriteStream('output.txt');
writable.write('Some data\n');
```

### 3. Piping (The Power of Streams)
Connect readable to writable. Handles backpressure automatically (prevents memory overflow if reading faster than writing).
```javascript
// Copy file
fs.createReadStream('input.txt').pipe(fs.createWriteStream('output.txt'));
```

### 4. Transform Streams
Modify data as it passes through.
```javascript
const { Transform } = require('stream');
const gzip = require('zlib').createGzip();

fs.createReadStream('input.txt')
  .pipe(gzip) // Compress
  .pipe(fs.createWriteStream('input.txt.gz'));
```

### 5. Pipeline API (Modern/Safe)
Use `stream.pipeline` to handle errors correctly (automatic cleanup).
```javascript
const { pipeline } = require('stream/promises');

await pipeline(
  fs.createReadStream('input.txt'),
  gzip,
  fs.createWriteStream('output.gz')
);
```

## Constraints
- **Error Handling**: `pipe()` does not forward errors automatically. Use `pipeline` or attach error listeners to all streams.
- **Complexity**: Writing custom Transform streams requires understanding the internal buffering mechanism.

## Expected Output
Low memory footprint applications capable of processing datasets significantly larger than available RAM.

# Skill: Background Jobs (BullMQ)

## Purpose
To offload time-consuming tasks (email sending, image processing, report generation) from the main HTTP request-response cycle using Redis-based queues.

## When to Use
- When an API request takes longer than a few seconds.
- To handle rate-limited 3rd party API calls.
- To retry failed operations automatically.

## Procedure

### 1. Setup
Requires a running Redis instance.
```bash
npm install bullmq ioredis
```

### 2. Producer (Adding Jobs)
Add jobs to a queue.
```javascript
const { Queue } = require('bullmq');
const emailQueue = new Queue('email-queue', { connection: redisConnection });

async function sendWelcomeEmail(user) {
  await emailQueue.add('welcome-email', {
    email: user.email,
    name: user.name
  }, {
    attempts: 3, // Retry 3 times on failure
    backoff: { type: 'exponential', delay: 1000 }
  });
}
```

### 3. Consumer (Processing Jobs)
Worker processes jobs from the queue. Run this in a separate process or service.
```javascript
const { Worker } = require('bullmq');

const worker = new Worker('email-queue', async job => {
  console.log(`Sending email to ${job.data.email}`);
  await sendEmailService(job.data);
}, { connection: redisConnection });

worker.on('completed', job => {
  console.log(`Job ${job.id} completed`);
});

worker.on('failed', (job, err) => {
  console.log(`Job ${job.id} failed: ${err.message}`);
});
```

## Constraints
- **Redis Dependency**: The queue relies entirely on Redis. If Redis goes down, queues are inaccessible (though data persists if configured).
- **Concurrency**: Configure `concurrency` option in Worker to process multiple jobs in parallel based on CPU resources.

## Expected Output
Improved API response times (immediate 202 Accepted) and reliable background task execution with retry mechanisms.

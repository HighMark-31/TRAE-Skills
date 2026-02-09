# Skill: Web Workers

## Purpose
To run JavaScript in background threads, preventing heavy computations from blocking the UI (Main Thread).

## When to Use
- Image processing/filtering.
- Parsing large JSON/CSV files.
- Complex cryptographic calculations.
- Syntax highlighting in editors.

## Procedure

### 1. Create Worker File
`worker.js`:
```javascript
self.onmessage = (e) => {
  const result = heavyComputation(e.data);
  self.postMessage(result);
};

function heavyComputation(num) {
  // Simulate CPU work
  return num * 2;
}
```

### 2. Main Thread Integration
```javascript
const worker = new Worker('worker.js');

worker.postMessage(100);

worker.onmessage = (e) => {
  console.log('Result from worker:', e.data);
};

worker.onerror = (err) => {
  console.error('Worker error:', err);
};
```

### 3. Using with React/Bundlers
Vite/Webpack support importing workers.
```javascript
import MyWorker from './worker?worker'; // Vite syntax
const worker = new MyWorker();
```

## Constraints
- **No DOM Access**: Workers cannot access `window`, `document`, or update the UI directly. They must communicate back to the main thread.
- **Serialization**: Data passed between threads is cloned (structured clone algorithm). Avoid passing massive objects repeatedly; use `Transferable Objects` (ArrayBuffer) for zero-copy transfer.

## Expected Output
A responsive UI that remains interactive even during intensive data processing tasks.

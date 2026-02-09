# Skill: Vector Database Setup

## Purpose
To provision and configure a vector database (Vector DB) for storing high-dimensional embeddings, enabling semantic search and RAG applications.

## When to Use
- Implementing RAG (Retrieval-Augmented Generation).
- Building recommendation systems based on similarity.
- Implementing semantic search (search by meaning, not just keywords).

## Procedure

### 1. Choice of Database (Selection)
- **Pinecone**: Best for managed, serverless, and fast scaling.
- **pgvector**: Best for existing PostgreSQL users who want to keep data in one place.
- **Chroma**: Best for local development and simple prototyping.

### 2. Implementation: Pinecone (Managed)
Install the client and initialize the index.

```bash
npm install @pinecone-database/pinecone
```

```typescript
import { Pinecone } from '@pinecone-database/pinecone';

const pc = new Pinecone({ apiKey: process.env.PINECONE_API_KEY! });

async function setupIndex() {
  await pc.createIndex({
    name: 'my-index',
    dimension: 1536, // Must match embedding model (e.g., text-embedding-3-small)
    metric: 'cosine',
    spec: { 
      serverless: { 
        cloud: 'aws', 
        region: 'us-east-1' 
      }
    }
  });
}
```

### 3. Implementation: pgvector (PostgreSQL)
Enable the extension and create a table with a vector column.

```sql
-- 1. Enable extension
CREATE EXTENSION IF NOT EXISTS vector;

-- 2. Create table
CREATE TABLE documents (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  content text,
  metadata jsonb,
  embedding vector(1536) -- Match your model's dimensions
);

-- 3. Create index for fast search (HNSW is recommended)
CREATE INDEX ON documents USING hnsw (embedding vector_cosine_ops);
```

### 4. Data Insertion (Upsert)
Always batch your insertions for efficiency.

```typescript
// Pinecone example
const index = pc.index('my-index');

await index.upsert([
  {
    id: 'doc1',
    values: [0.1, 0.2, ...], // The embedding vector
    metadata: { text: 'The actual content...', category: 'legal' }
  }
]);
```

### 5. Querying (Semantic Search)
Perform a similarity search using a query vector.

```typescript
const queryResponse = await index.query({
  vector: [0.1, 0.2, ...], // Vector of the user query
  topK: 5,
  includeMetadata: true,
});
```

## Constraints
- **Dimension Matching**: The dimension of the index MUST exactly match the output dimension of your embedding model.
- **Metric Selection**: Use `cosine` for text; `euclidean` or `dotproduct` for other specific use cases.
- **Batch Limits**: Most vector DBs have limits on payload size per upsert (e.g., 2MB or 100 vectors).

## Expected Output
A fully configured vector index ready for high-speed similarity searches and data retrieval.

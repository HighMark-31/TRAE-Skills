# Skill: RAG System Architecture

## Purpose
To design and implement a Retrieval-Augmented Generation (RAG) system that grounds LLM responses in specific, external data sources, reducing hallucinations and enabling knowledge on private data.

## When to Use
- When the LLM needs to answer questions about proprietary documents (PDFs, internal wikis).
- When the knowledge base is too large to fit in the context window.
- When data changes frequently and retraining is not feasible.

## Procedure

### 1. Ingestion & Embedding (The ETL Pipeline)
Process documents into vectors.

```typescript
import { RecursiveCharacterTextSplitter } from "langchain/text_splitter";
import { OpenAIEmbeddings } from "@langchain/openai";
import { MemoryVectorStore } from "langchain/vectorstores/memory";

// 1. Text Splitting
const splitter = new RecursiveCharacterTextSplitter({
  chunkSize: 1000,
  chunkOverlap: 200, // Crucial for context continuity
});

// 2. Embedding Model
const embeddings = new OpenAIEmbeddings({
  modelName: "text-embedding-3-small", // Efficient & cheap
});

// 3. Vector Store Initialization
// In production, use Pinecone, Weaviate, or pgvector
const vectorStore = new MemoryVectorStore(embeddings);

export async function ingestDocument(text: string) {
  const docs = await splitter.createDocuments([text]);
  await vectorStore.addDocuments(docs);
  return vectorStore;
}
```

### 2. Retrieval Implementation
Create a retriever that fetches relevant context.

```typescript
// Create a retriever from the store
const retriever = vectorStore.asRetriever({
  k: 3, // Top 3 results
  searchType: "similarity", // or "mmr" for diversity
});
```

### 3. The RAG Chain (Generation)
Combine retrieval with generation.

```typescript
import { ChatOpenAI } from "@langchain/openai";
import { ChatPromptTemplate } from "@langchain/core/prompts";
import { createStuffDocumentsChain } from "langchain/chains/combine_documents";
import { createRetrievalChain } from "langchain/chains/retrieval";

const model = new ChatOpenAI({ modelName: "gpt-4o" });

const prompt = ChatPromptTemplate.fromTemplate(`
Answer the user's question based ONLY on the following context:

<context>
{context}
</context>

Question: {input}
`);

// 1. Create the document combining chain
const combineDocsChain = await createStuffDocumentsChain({
  llm: model,
  prompt,
});

// 2. Create the full retrieval chain
const ragChain = await createRetrievalChain({
  retriever,
  combineDocsChain,
});

// Usage
export async function askQuestion(question: string) {
  const response = await ragChain.invoke({
    input: question,
  });
  return response.answer;
}
```

### 4. Advanced: Hybrid Search
For production, combine keyword search (BM25) with semantic search (Vectors) for better accuracy.

```typescript
// Conceptual example for Supabase/Postgres
// supabase.rpc('hybrid_search', { query_text: ..., match_threshold: ... })
```

## Constraints
- **Chunk Quality**: If chunks are too small, context is lost. If too large, noise increases.
- **Latency**: Embedding + Vector Search + Generation = High Latency. Use caching and streaming.
- **Relevance**: "Garbage In, Garbage Out". Ensure the retrieved context is actually relevant before passing to LLM.

## Expected Output
A functional RAG pipeline where a user asks a question, the system retrieves relevant docs, and the LLM answers accurately citing the sources.

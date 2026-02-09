# Skill: Elasticsearch Integration

## Purpose
To implement full-text search, autocomplete, and complex filtering capabilities that standard SQL databases cannot handle efficiently.

## When to Use
- Search bars (e-commerce products, user finder).
- Log analysis.
- Fuzzy matching (handling typos).

## Procedure

### 1. Connection
```javascript
const { Client } = require('@elastic/elasticsearch');
const client = new Client({ node: 'http://localhost:9200' });
```

### 2. Indexing Data (Sync)
Keep Elasticsearch in sync with the primary DB.
- **On Save**: When User is updated in SQL, update Elasticsearch.
```javascript
await client.index({
  index: 'users',
  id: user.id,
  document: {
    name: user.name,
    email: user.email,
    bio: user.bio
  }
});
```

### 3. Searching
Perform a multi-match fuzzy search.
```javascript
const result = await client.search({
  index: 'users',
  query: {
    multi_match: {
      query: 'jonh doe', // typo intended
      fields: ['name', 'bio'],
      fuzziness: 'AUTO'
    }
  }
});
const hits = result.hits.hits.map(h => h._source);
```

### 4. Mappings
Define types explicitly for better performance.
```javascript
await client.indices.create({
  index: 'users',
  mappings: {
    properties: {
      name: { type: 'text' }, // Full-text search
      email: { type: 'keyword' }, // Exact match only
      created_at: { type: 'date' }
    }
  }
});
```

## Constraints
- **Sync Latency**: Data might not be immediately available for search (near real-time).
- **Cost**: Elasticsearch is resource-heavy (RAM/CPU).
- **Reindexing**: Changing mappings often requires reindexing all data.

## Expected Output
Fast, relevant search results with capabilities like highlighting, facets, and fuzzy matching.

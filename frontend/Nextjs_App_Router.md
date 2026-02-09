# Skill: Next.js App Router

## Purpose
To build modern, full-stack React applications using the Next.js App Router (introduced in v13), leveraging React Server Components (RSC) for better performance.

## When to Use
- Building a new Next.js application.
- When you need Server Components, Layouts, or Streaming.
- Migrating from `pages/` directory (gradually).

## Procedure

### 1. Directory Structure
Files in `app/` are routes.
- `app/page.tsx` -> `/`
- `app/blog/[slug]/page.tsx` -> `/blog/abc`
- `app/layout.tsx` -> Wraps all pages (Root Layout).

### 2. Server Components (Default)
By default, components are Server Components. They run on the server, can be async, and can access DB directly.
```tsx
// app/users/page.tsx
async function getUsers() {
  const res = await fetch('https://api.example.com/users');
  return res.json();
}

export default async function Page() {
  const users = await getUsers();
  return <ul>{users.map(u => <li key={u.id}>{u.name}</li>)}</ul>;
}
```

### 3. Client Components
Use `'use client'` directive at the top to use hooks (`useState`, `useEffect`).
```tsx
'use client';
import { useState } from 'react';

export default function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(count + 1)}>{count}</button>;
}
```

### 4. Data Fetching
- **Static (Default)**: `fetch('...', { cache: 'force-cache' })`.
- **Dynamic**: `fetch('...', { cache: 'no-store' })`.
- **Revalidation**: `fetch('...', { next: { revalidate: 3600 } })`.

## Constraints
- **Context**: You cannot use React Context directly in Server Components. Wrap the provider in a Client Component.
- **Node APIs**: Server components have access to Node APIs (fs, db), but Client components do not.

## Expected Output
A high-performance application with reduced JavaScript sent to the client and simplified data fetching logic.

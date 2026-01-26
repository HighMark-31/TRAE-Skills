# SSR vs CSR Decision Matrix

## Concepts
- **CSR (Client-Side Rendering)**: Browser downloads JS bundle and renders UI (e.g., CRA).
- **SSR (Server-Side Rendering)**: Server renders HTML and sends to browser (e.g., Next.js).
- **SSG (Static Site Generation)**: HTML generated at build time.

## Decision Factors
- **SEO**: SSR/SSG is better for crawlers.
- **Initial Load**: SSR is faster (First Contentful Paint).
- **Interactivity**: CSR can be faster after initial load.
- **Cost**: SSR requires running a Node server (computational cost).

## Verdict
- **Public Marketing Site/Blog**: SSG.
- **Dashboard/SaaS App**: CSR is often sufficient.
- **E-commerce/Social Network**: SSR for SEO and performance.

# Skill: Web Vitals Optimization

## Purpose
To measure and improve Core Web Vitals (LCP, INP, CLS) for better user experience and SEO rankings.

## When to Use
- When users complain about slowness.
- Preparing for a production launch.
- Continuous monitoring.

## Procedure

### 1. Measurement
- **Lighthouse**: Lab data. Run in Chrome DevTools.
- **Web Vitals Extension**: Real-time checking.
- **Code**:
  ```javascript
  import { onLCP, onINP, onCLS } from 'web-vitals';
  onLCP(console.log);
  ```

### 2. Optimizing LCP (Largest Contentful Paint)
Goal: < 2.5s.
- **Images**: Use WebP/AVIF. Explicit `width`/`height`.
- **Preload**: `<link rel="preload" as="image" href="hero.jpg">`.
- **Server**: Improve TTFB (Time to First Byte) via caching/CDN.

### 3. Optimizing INP (Interaction to Next Paint)
Goal: < 200ms. Replaces FID.
- **Main Thread**: Break up long tasks using `setTimeout` or `requestIdleCallback`.
- **React**: Use `useTransition` for non-urgent updates.
- **Events**: Avoid heavy logic in event handlers.

### 4. Optimizing CLS (Cumulative Layout Shift)
Goal: < 0.1.
- **Space**: Always reserve space for images/ads/embeds (CSS `aspect-ratio`).
- **Fonts**: Use `font-display: swap` to avoid FOIT (Flash of Invisible Text).

## Constraints
- **Third-Party Scripts**: Analytics/Ads often hurt performance. Defer them (`<script defer>`) or load via Web Workers (Partytown).
- **Network**: Test on "Fast 3G" in DevTools, not just Wi-Fi.

## Expected Output
A faster, more stable website that passes Google's Core Web Vitals assessment.

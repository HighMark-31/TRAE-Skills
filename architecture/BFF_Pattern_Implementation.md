# BFF Pattern Implementation (Backend for Frontend)

## Overview
A BFF is a dedicated backend service for a specific frontend (e.g., Web BFF, Mobile BFF).

## Problem
Different frontends have different data needs. A "one-size-fits-all" API might over-fetch for mobile or under-fetch for desktop.

## Solution
- The BFF calls downstream microservices and aggregates/formats data specifically for its frontend.
- Handles authentication, caching, and protocol translation (e.g., gRPC to JSON).

## When to use
- You have multiple client types (Web, iOS, Android) with significantly different UI requirements.

# Skill: Pagination Implementation

## Purpose
To limit the amount of data returned in a single API response, improving performance and user experience when dealing with large lists.

## When to Use
- Listing users, products, or orders.
- Any endpoint returning an array that could grow indefinitely.

## Procedure
1.  **Choose Strategy**:
    - **Offset-based** (`skip/limit`): Simple, good for page numbers. Slow on large offsets.
    - **Cursor-based** (`after_id`): Faster, good for infinite scroll. No random page access.
2.  **Parse Query Params**: Extract `page`, `limit`, or `cursor` from request. Set defaults (e.g., limit=20).
3.  **Query Database**:
    - Apply `limit` + 1 (to check if there's a next page).
    - Apply sort order (crucial for cursor).
4.  **Format Response**:
    - Return `data` array.
    - Return `meta` object: `{ total, page, hasNextPage, nextCursor }`.
5.  **Validation**: Cap the maximum `limit` to prevent users requesting 10,000 rows.

## Constraints
- Ensure the sort column is indexed.
- For cursor pagination, the sort column must be unique (or use a tiebreaker like ID).

## Expected Output
A reusable service function or helper that wraps DB queries and returns a standardized paginated response structure.

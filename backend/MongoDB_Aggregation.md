# Skill: MongoDB Aggregation Framework

## Purpose
To perform complex data processing, transformation, and analysis directly within MongoDB using pipelines.

## When to Use
- When simple `find()` queries are insufficient.
- For grouping, summing, or averaging data (analytics).
- For joining collections (`$lookup`).

## Procedure

### 1. Structure
An aggregation pipeline is an array of stages. Documents pass through stages in order.
```javascript
db.collection.aggregate([
  { $stage1: { ... } },
  { $stage2: { ... } }
])
```

### 2. Common Stages

#### A. Filtering (`$match`)
Always place this first to reduce dataset size early.
```javascript
{ $match: { status: "completed" } }
```

#### B. Grouping (`$group`)
Calculate metrics.
```javascript
{
  $group: {
    _id: "$customerId", // Group by customer
    totalSpent: { $sum: "$amount" },
    averageOrder: { $avg: "$amount" }
  }
}
```

#### C. Joining (`$lookup`)
Left outer join with another collection.
```javascript
{
  $lookup: {
    from: "users",
    localField: "userId",
    foreignField: "_id",
    as: "userDetails"
  }
}
```

#### D. Projections (`$project`)
Shape the output.
```javascript
{
  $project: {
    name: 1,
    totalSpent: 1,
    _id: 0
  }
}
```

### 3. Optimization
- Ensure the first `$match` stage hits an index.
- Use `$limit` and `$skip` for pagination.

## Constraints
- **Memory Limit**: Each stage has a 100MB RAM limit. Use `{ allowDiskUse: true }` for large operations, though it is slower.
- **Complexity**: Debugging long pipelines is difficult; build them stage by stage.

## Expected Output
Transformed and aggregated data returned efficiently without pulling all raw documents into the application layer.

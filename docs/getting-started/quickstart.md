# Quick Start

This guide will help you get started with Mongo Aggro in just a few minutes.

## Basic Concepts

Mongo Aggro provides three main components:

1. **Pipeline** - A container for aggregation stages that can be passed directly to MongoDB
2. **Stages** - Individual operations like `$match`, `$group`, `$sort`, etc.
3. **Accumulators** - Functions used in `$group` stage like `$sum`, `$avg`, `$max`, etc.

## Your First Pipeline

```python
from mongo_aggro import Pipeline, Match, Group, Sort, Limit, Sum

# Create a simple pipeline
pipeline = Pipeline([
    Match(query={"status": "active"}),
    Group(
        id="$category",
        accumulators={"count": {"$sum": 1}}
    ),
    Sort(fields={"count": -1}),
    Limit(count=5),
])

# View the pipeline as a list
print(pipeline.to_list())
```

Output:
```python
[
    {"$match": {"status": "active"}},
    {"$group": {"_id": "$category", "count": {"$sum": 1}}},
    {"$sort": {"count": -1}},
    {"$limit": 5}
]
```

## Using with PyMongo

```python
from pymongo import MongoClient
from mongo_aggro import Pipeline, Match, Group, Sort

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["mydb"]
collection = db["orders"]

# Build the pipeline
pipeline = Pipeline([
    Match(query={"year": 2024}),
    Group(
        id="$product",
        accumulators={"total_sales": {"$sum": "$amount"}}
    ),
    Sort(fields={"total_sales": -1}),
])

# Execute - Pipeline is directly iterable!
results = list(collection.aggregate(pipeline))

for doc in results:
    print(f"{doc['_id']}: ${doc['total_sales']}")
```

## Using Accumulators

Mongo Aggro provides typed accumulator classes for cleaner code:

```python
from mongo_aggro import (
    Pipeline, Match, Group, Sort,
    Sum, Avg, Max, Min, Count_,
    merge_accumulators
)

pipeline = Pipeline([
    Match(query={"status": "completed"}),
    Group(
        id="$category",
        accumulators=merge_accumulators(
            Sum(name="total_revenue", field="amount"),
            Avg(name="avg_order", field="amount"),
            Max(name="max_order", field="amount"),
            Min(name="min_order", field="amount"),
            Count_(name="order_count"),
        )
    ),
    Sort(fields={"total_revenue": -1}),
])
```

## Method Chaining

You can also build pipelines using method chaining:

```python
from mongo_aggro import Pipeline, Match, Group, Sort, Limit

pipeline = (
    Pipeline()
    .add_stage(Match(query={"active": True}))
    .add_stage(Group(id="$type", accumulators={"count": {"$sum": 1}}))
    .add_stage(Sort(fields={"count": -1}))
    .add_stage(Limit(count=10))
)
```

## Next Steps

- Learn about all available [Stages](../guide/stages.md)
- Explore [Accumulators](../guide/accumulators.md) for grouping operations
- See [Examples](../examples/basic.md) for common use cases

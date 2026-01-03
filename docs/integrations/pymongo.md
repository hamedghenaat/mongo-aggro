# PyMongo Integration

[PyMongo](https://pymongo.readthedocs.io/) is the official MongoDB driver
for Python. Mongo Aggro works directly with PyMongo's collection.aggregate()
method.

## Installation

```bash
pip install mongo-aggro pymongo
```

## Basic Usage

```python
from pymongo import MongoClient
from mongo_aggro import (
    Pipeline, Match, Group, Sort, Sum, ASCENDING, DESCENDING
)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['mydb']
orders = db['orders']

# Build aggregation pipeline
pipeline = Pipeline([
    Match(query={"status": "completed"}),
    Group(
        id="$category",
        total_amount=Sum(name="total_amount", field="amount").to_expr(),
        order_count={"$sum": 1}
    ),
    Sort(fields={"total_amount": DESCENDING})
])

# Execute directly - Pipeline is iterable!
results = list(orders.aggregate(pipeline))
```

## Direct Iteration

One of Mongo Aggro's key features is that Pipeline implements `__iter__`,
so you can pass it directly to PyMongo without calling `to_list()`:

```python
# Both work identically - but direct passing is preferred
results = orders.aggregate(pipeline)           # Direct - recommended!
results = orders.aggregate(pipeline.to_list()) # Explicit conversion

# Iterate over results
for doc in orders.aggregate(pipeline):
    print(doc)
```

## Sort Direction Constants

Use `ASCENDING` (1) and `DESCENDING` (-1) for better code readability:

```python
from mongo_aggro import (
    Pipeline, Sort, ASCENDING, DESCENDING
)

# Using constants
pipeline = Pipeline([
    Sort(fields={
        "created_at": DESCENDING,
        "name": ASCENDING
    })
])
```

## Async with Motor

Motor is the async driver for MongoDB built on PyMongo. Mongo Aggro works
the same way:

```python
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from mongo_aggro import Pipeline, Match, Group, Sort, DESCENDING

async def get_category_stats():
    client = AsyncIOMotorClient('mongodb://localhost:27017/')
    db = client['mydb']
    orders = db['orders']

    pipeline = Pipeline([
        Match(query={"status": "completed"}),
        Group(
            id="$category",
            total={"$sum": "$amount"},
            count={"$sum": 1}
        ),
        Sort(fields={"total": DESCENDING})
    ])

    # Works directly with Motor - no to_list() needed!
    cursor = orders.aggregate(pipeline)
    results = await cursor.to_list(length=None)

    return results

# Run
results = asyncio.run(get_category_stats())
```

## Complex Aggregations

### Lookup (Join)

```python
from mongo_aggro import Pipeline, Match, Lookup, Unwind, Project

pipeline = Pipeline([
    Match(query={"status": "active"}),
    Lookup(
        from_collection="customers",
        local_field="customer_id",
        foreign_field="_id",
        as_field="customer"
    ),
    Unwind(path="customer"),
    Project(fields={
        "_id": 0,
        "order_id": "$_id",
        "amount": 1,
        "customer_name": "$customer.name",
        "customer_email": "$customer.email"
    })
])

# Pass pipeline directly
results = list(orders.aggregate(pipeline))
```

### Faceted Search

```python
from mongo_aggro import (
    Pipeline, Match, Facet, Group, Sort, Limit, DESCENDING
)

pipeline = Pipeline([
    Match(query={"year": 2024}),
    Facet(pipelines={
        "by_category": [
            Group(id="$category", count={"$sum": 1}),
            Sort(fields={"count": DESCENDING}),
            Limit(count=5)
        ],
        "by_region": [
            Group(id="$region", total={"$sum": "$amount"}),
            Sort(fields={"total": DESCENDING}),
            Limit(count=5)
        ],
        "total_stats": [
            Group(
                id=None,
                total_orders={"$sum": 1},
                total_amount={"$sum": "$amount"},
                avg_amount={"$avg": "$amount"}
            )
        ]
    })
])

# Pass pipeline directly
results = list(orders.aggregate(pipeline))
# results[0] contains: by_category, by_region, total_stats
```

### Window Functions

```python
from mongo_aggro import Pipeline, Match, SetWindowFields, Sort, ASCENDING

pipeline = Pipeline([
    Match(query={"year": 2024}),
    SetWindowFields(
        partition_by="$region",
        sort_by={"date": ASCENDING},
        output={
            "running_total": {
                "$sum": "$amount",
                "window": {"documents": ["unbounded", "current"]}
            },
            "moving_avg": {
                "$avg": "$amount",
                "window": {"documents": [-2, 2]}
            }
        }
    ),
    Sort(fields={"region": ASCENDING, "date": ASCENDING})
])

# Pass pipeline directly
results = list(orders.aggregate(pipeline))
```

## Aggregation Options

PyMongo's aggregate() accepts various options:

```python
# With options - pipeline passed directly
cursor = orders.aggregate(
    pipeline,
    allowDiskUse=True,      # For large datasets
    batchSize=1000,         # Cursor batch size
    maxTimeMS=30000,        # Timeout
    comment="category_report"  # For profiling
)

results = list(cursor)
```

## Building Dynamic Pipelines

```python
from mongo_aggro import DESCENDING

def build_sales_pipeline(
    start_date=None,
    end_date=None,
    categories=None,
    group_by="category"
):
    pipeline = Pipeline()

    # Dynamic match conditions
    match_query = {"status": "completed"}

    if start_date:
        match_query["date"] = {"$gte": start_date}
    if end_date:
        match_query.setdefault("date", {})["$lt"] = end_date
    if categories:
        match_query["category"] = {"$in": categories}

    pipeline.add_stage(Match(query=match_query))

    # Dynamic grouping
    pipeline.add_stage(Group(
        id=f"${group_by}",
        total={"$sum": "$amount"},
        count={"$sum": 1},
        avg={"$avg": "$amount"}
    ))

    pipeline.add_stage(Sort(fields={"total": DESCENDING}))

    return pipeline


# Usage
pipeline = build_sales_pipeline(
    start_date=datetime(2024, 1, 1),
    categories=["electronics", "clothing"],
    group_by="region"
)

# Pass pipeline directly
results = list(orders.aggregate(pipeline))
```

## Mixing Typed and Raw Stages

```python
pipeline = Pipeline([
    Match(query={"type": "sale"}),
    Group(id="$product_id", total={"$sum": "$quantity"})
])

# Add raw stages for complex operations
pipeline.extend_raw([
    {
        "$lookup": {
            "from": "products",
            "let": {"pid": "$_id"},
            "pipeline": [
                {"$match": {"$expr": {"$eq": ["$_id", "$$pid"]}}},
                {"$project": {"name": 1, "category": 1}}
            ],
            "as": "product"
        }
    },
    {"$unwind": "$product"},
    {
        "$project": {
            "_id": 0,
            "product_name": "$product.name",
            "category": "$product.category",
            "total_sold": "$total"
        }
    }
])

# Pass pipeline directly
results = list(sales.aggregate(pipeline))
```

## Error Handling

```python
from pymongo.errors import OperationFailure

pipeline = Pipeline([
    Match(query={"status": "active"}),
    Group(id="$category", total={"$sum": "$amount"})
])

try:
    results = list(orders.aggregate(
        pipeline,
        maxTimeMS=5000  # 5 second timeout
    ))
except OperationFailure as e:
    if e.code == 50:  # ExceededTimeLimit
        print("Query timed out")
    else:
        raise
```

## Explain Plans

Analyze aggregation performance:

```python
# Get explain output - need to_list() for explain
explain = orders.aggregate(
    pipeline.to_list(),
    explain=True
)

print(explain)

# Or use database command
explain = db.command(
    'aggregate',
    'orders',
    pipeline=pipeline.to_list(),
    explain=True
)
```

## Pagination Helper

```python
from mongo_aggro import DESCENDING

def paginate_aggregate(
    collection,
    pipeline: Pipeline,
    page: int = 1,
    page_size: int = 20,
    sort: dict = None
):
    """Paginate aggregation results."""
    skip = (page - 1) * page_size

    # Get pipeline as list for manipulation
    stages = pipeline.to_list()

    # Count total
    count_stages = stages + [{"$count": "total"}]
    count_result = list(collection.aggregate(count_stages))
    total = count_result[0]["total"] if count_result else 0

    # Get page data
    data_stages = stages.copy()
    if sort:
        data_stages.append({"$sort": sort})
    data_stages.extend([
        {"$skip": skip},
        {"$limit": page_size}
    ])

    data = list(collection.aggregate(data_stages))

    return {
        "data": data,
        "total": total,
        "page": page,
        "page_size": page_size,
        "pages": (total + page_size - 1) // page_size
    }


# Usage
result = paginate_aggregate(
    orders,
    Pipeline([
        Match(query={"status": "completed"}),
        Group(id="$category", total={"$sum": "$amount"})
    ]),
    page=2,
    page_size=10,
    sort={"total": DESCENDING}
)
```

## Tips for PyMongo Integration

1. **Pass Pipeline directly** - It implements `__iter__` for direct use
2. **Use sort constants** - `ASCENDING` and `DESCENDING` for readability
3. **Use `allowDiskUse=True`** - For large aggregations
4. **Set `maxTimeMS`** - Prevent runaway queries
5. **Use indexes** - Ensure `$match` stages can use indexes
6. **Profile with `explain`** - Analyze query performance
7. **Batch processing** - Use cursor iteration for large results

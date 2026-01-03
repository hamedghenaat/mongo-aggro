# Advanced Examples

This page demonstrates advanced aggregation patterns using Mongo Aggro.

## Joins with Lookup

### Simple Join

```python
from mongo_aggro import Pipeline, Match, Lookup, Unwind, Project

pipeline = Pipeline([
    Match(query={"status": "active"}),
    Lookup(
        from_collection="customers",
        local_field="customerId",
        foreign_field="_id",
        as_field="customer"
    ),
    Unwind(path="customer"),
    Project(fields={
        "orderId": "$_id",
        "total": 1,
        "customerName": "$customer.name",
        "customerEmail": "$customer.email",
    }),
])
```

### Lookup with Pipeline

```python
from mongo_aggro import Pipeline, Match, Lookup, Project, Unwind, Group

pipeline = Pipeline([
    Lookup(
        from_collection="orders",
        let={"userId": "$_id"},
        pipeline=Pipeline([
            Match(query={
                "$expr": {"$eq": ["$customerId", "$$userId"]},
                "status": "completed",
            }),
            Group(
                id=None,
                accumulators={
                    "totalSpent": {"$sum": "$amount"},
                    "orderCount": {"$sum": 1},
                }
            ),
        ]),
        as_field="orderStats"
    ),
    Unwind(path="orderStats", preserve_null_and_empty=True),
    Project(fields={
        "name": 1,
        "email": 1,
        "totalSpent": {"$ifNull": ["$orderStats.totalSpent", 0]},
        "orderCount": {"$ifNull": ["$orderStats.orderCount", 0]},
    }),
])
```

### Multiple Lookups

```python
from mongo_aggro import Pipeline, Lookup, Unwind, Project

pipeline = Pipeline([
    Lookup(
        from_collection="users",
        local_field="userId",
        foreign_field="_id",
        as_field="user"
    ),
    Lookup(
        from_collection="products",
        local_field="productId",
        foreign_field="_id",
        as_field="product"
    ),
    Unwind(path="user"),
    Unwind(path="product"),
    Project(fields={
        "userName": "$user.name",
        "productName": "$product.name",
        "quantity": 1,
        "total": 1,
    }),
])
```

## Faceted Search

### Multi-Facet Aggregation

```python
from mongo_aggro import (
    Pipeline, Match, Facet, Group, Sort, Limit, Count, Sum, DESCENDING
)

pipeline = Pipeline([
    Match(query={"status": "active"}),
    Facet(pipelines={
        "byCategory": Pipeline([
            Group(id="$category", accumulators={"count": {"$sum": 1}}),
            Sort(fields={"count": DESCENDING}),
        ]),
        "byPriceRange": Pipeline([
            Group(
                id={
                    "$switch": {
                        "branches": [
                            {"case": {"$lt": ["$price", 50]}, "then": "budget"},
                            {"case": {"$lt": ["$price", 200]}, "then": "mid"},
                        ],
                        "default": "premium"
                    }
                },
                accumulators={"count": {"$sum": 1}}
            ),
        ]),
        "topRated": Pipeline([
            Match(query={"rating": {"$gte": 4.5}}),
            Sort(fields={"rating": DESCENDING}),
            Limit(count=5),
        ]),
        "stats": Pipeline([
            Group(
                id=None,
                accumulators={
                    "avgPrice": {"$avg": "$price"},
                    "totalProducts": {"$sum": 1},
                }
            ),
        ]),
    }),
])
```

## Window Functions

### Running Totals

```python
from mongo_aggro import Pipeline, Sort, SetWindowFields, ASCENDING

pipeline = Pipeline([
    Sort(fields={"date": ASCENDING}),
    SetWindowFields(
        sort_by={"date": ASCENDING},
        output={
            "runningTotal": {
                "$sum": "$amount",
                "window": {"documents": ["unbounded", "current"]}
            }
        }
    ),
])
```

### Moving Average

```python
from mongo_aggro import Pipeline, SetWindowFields, ASCENDING

pipeline = Pipeline([
    SetWindowFields(
        partition_by="$productId",
        sort_by={"date": ASCENDING},
        output={
            "movingAvg": {
                "$avg": "$price",
                "window": {"documents": [-6, 0]}  # 7-day moving average
            }
        }
    ),
])
```

## Recursive Lookups

### Hierarchical Data with GraphLookup

```python
from mongo_aggro import Pipeline, Match, GraphLookup, Project

# Find all descendants in an org chart
pipeline = Pipeline([
    Match(query={"name": "CEO"}),
    GraphLookup(
        from_collection="employees",
        start_with="$_id",
        connect_from_field="_id",
        connect_to_field="managerId",
        as_field="subordinates",
        max_depth=10,
        depth_field="level"
    ),
    Project(fields={
        "name": 1,
        "subordinates.name": 1,
        "subordinates.level": 1,
    }),
])
```

## Data Bucketing

### Histogram with Bucket

```python
from mongo_aggro import Pipeline, Bucket

pipeline = Pipeline([
    Bucket(
        group_by="$price",
        boundaries=[0, 25, 50, 100, 250, 500, 1000],
        default="Luxury",
        output={
            "count": {"$sum": 1},
            "avgPrice": {"$avg": "$price"},
            "products": {"$push": "$name"},
        }
    ),
])
```

### Auto Bucketing

```python
from mongo_aggro import Pipeline, BucketAuto

pipeline = Pipeline([
    BucketAuto(
        group_by="$age",
        buckets=5,
        output={
            "count": {"$sum": 1},
            "avgIncome": {"$avg": "$income"},
        }
    ),
])
```

## Union Operations

### Combining Collections

```python
from mongo_aggro import Pipeline, Match, UnionWith, Sort, Project, DESCENDING

pipeline = Pipeline([
    Match(query={"type": "order"}),
    Project(fields={
        "date": 1,
        "amount": 1,
        "source": {"$literal": "orders"},
    }),
    UnionWith(
        collection="refunds",
        pipeline=Pipeline([
            Project(fields={
                "date": 1,
                "amount": {"$multiply": ["$amount", -1]},
                "source": {"$literal": "refunds"},
            }),
        ])
    ),
    Sort(fields={"date": DESCENDING}),
])
```

## Geospatial Queries

### Find Nearby Locations

```python
from mongo_aggro import Pipeline, GeoNear, Limit, Project

pipeline = Pipeline([
    GeoNear(
        near={"type": "Point", "coordinates": [-73.99, 40.73]},
        distance_field="distance",
        max_distance=5000,  # 5km
        spherical=True,
        query={"status": "open"},
    ),
    Limit(count=10),
    Project(fields={
        "name": 1,
        "address": 1,
        "distanceKm": {"$divide": ["$distance", 1000]},
    }),
])
```

## Text Search with Aggregation

### Full-Text Search with Scoring

```python
from mongo_aggro import Pipeline, Match, AddFields, Sort, DESCENDING

pipeline = Pipeline([
    Match(query={"$text": {"$search": "coffee shop"}}),
    AddFields(fields={"score": {"$meta": "textScore"}}),
    Sort(fields={"score": DESCENDING}),
])
```

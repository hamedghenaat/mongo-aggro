# Basic Examples

This page shows basic examples of common aggregation patterns using Mongo Aggro.

## Filtering and Sorting

### Get Active Users Sorted by Date

```python
from mongo_aggro import Pipeline, Match, Sort, Limit

pipeline = Pipeline([
    Match(query={"status": "active"}),
    Sort(fields={"createdAt": -1}),
    Limit(count=100),
])

results = collection.aggregate(pipeline)
```

### Filter with Multiple Conditions

```python
from mongo_aggro import Pipeline, Match, Project

pipeline = Pipeline([
    Match(query={
        "status": "active",
        "age": {"$gte": 18, "$lte": 65},
        "country": {"$in": ["US", "UK", "CA"]},
    }),
    Project(fields={
        "_id": 0,
        "name": 1,
        "email": 1,
        "country": 1,
    }),
])
```

## Grouping and Aggregation

### Count by Category

```python
from mongo_aggro import Pipeline, Group, Sort

pipeline = Pipeline([
    Group(id="$category", accumulators={"count": {"$sum": 1}}),
    Sort(fields={"count": -1}),
])
```

### Sales Summary by Product

```python
from mongo_aggro import (
    Pipeline, Match, Group, Sort,
    Sum, Avg, merge_accumulators
)

pipeline = Pipeline([
    Match(query={"status": "completed"}),
    Group(
        id="$productId",
        accumulators=merge_accumulators(
            Sum(name="totalSales", field="amount"),
            Sum(name="quantity", field="qty"),
            Avg(name="avgPrice", field="price"),
        )
    ),
    Sort(fields={"totalSales": -1}),
])
```

### Group by Multiple Fields

```python
from mongo_aggro import Pipeline, Group, Sort, Sum

pipeline = Pipeline([
    Group(
        id={"year": "$year", "month": "$month"},
        accumulators={"total": {"$sum": "$amount"}}
    ),
    Sort(fields={"_id.year": -1, "_id.month": -1}),
])
```

## Working with Arrays

### Unwind and Count

```python
from mongo_aggro import Pipeline, Unwind, Group, Sort

pipeline = Pipeline([
    Unwind(path="tags"),
    Group(id="$tags", accumulators={"count": {"$sum": 1}}),
    Sort(fields={"count": -1}),
])
```

### Flatten Nested Arrays

```python
from mongo_aggro import Pipeline, Match, Unwind, Project

pipeline = Pipeline([
    Match(query={"status": "active"}),
    Unwind(path="items"),
    Project(fields={
        "orderId": "$_id",
        "itemName": "$items.name",
        "itemPrice": "$items.price",
    }),
])
```

## Pagination

### Basic Pagination

```python
from mongo_aggro import Pipeline, Match, Sort, Skip, Limit

page = 2
page_size = 20

pipeline = Pipeline([
    Match(query={"status": "active"}),
    Sort(fields={"createdAt": -1}),
    Skip(count=(page - 1) * page_size),
    Limit(count=page_size),
])
```

### Pagination with Total Count

```python
from mongo_aggro import Pipeline, Match, Facet, Sort, Skip, Limit, Count

page = 2
page_size = 20

pipeline = Pipeline([
    Match(query={"status": "active"}),
    Facet(pipelines={
        "data": Pipeline([
            Sort(fields={"createdAt": -1}),
            Skip(count=(page - 1) * page_size),
            Limit(count=page_size),
        ]),
        "total": Pipeline([
            Count(field="count"),
        ]),
    }),
])
```

## Field Transformation

### Rename Fields

```python
from mongo_aggro import Pipeline, Project

pipeline = Pipeline([
    Project(fields={
        "_id": 0,
        "userId": "$_id",
        "fullName": "$name",
        "emailAddress": "$email",
    }),
])
```

### Computed Fields

```python
from mongo_aggro import Pipeline, AddFields, Project

pipeline = Pipeline([
    AddFields(fields={
        "totalPrice": {"$multiply": ["$price", "$quantity"]},
        "discountedPrice": {
            "$subtract": [
                {"$multiply": ["$price", "$quantity"]},
                "$discount"
            ]
        },
    }),
    Project(fields={
        "name": 1,
        "totalPrice": 1,
        "discountedPrice": 1,
    }),
])
```

## Conditional Logic

### Using $cond

```python
from mongo_aggro import Pipeline, AddFields

pipeline = Pipeline([
    AddFields(fields={
        "status": {
            "$cond": {
                "if": {"$gte": ["$score", 70]},
                "then": "pass",
                "else": "fail"
            }
        }
    }),
])
```

### Using $switch

```python
from mongo_aggro import Pipeline, AddFields

pipeline = Pipeline([
    AddFields(fields={
        "grade": {
            "$switch": {
                "branches": [
                    {"case": {"$gte": ["$score", 90]}, "then": "A"},
                    {"case": {"$gte": ["$score", 80]}, "then": "B"},
                    {"case": {"$gte": ["$score", 70]}, "then": "C"},
                    {"case": {"$gte": ["$score", 60]}, "then": "D"},
                ],
                "default": "F"
            }
        }
    }),
])
```

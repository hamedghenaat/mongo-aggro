# Beanie Integration

[Beanie](https://beanie-odm.dev/) is an async MongoDB ODM built on top of
Pydantic and Motor. Mongo Aggro integrates naturally with Beanie since both
use Pydantic for data modeling.

## Installation

```bash
pip install mongo-aggro beanie
```

## Basic Usage

The Pipeline class implements `__iter__`, so you can pass it directly to
Beanie's aggregate method without calling `to_list()`:

```python
from beanie import Document, init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from mongo_aggro import (
    Pipeline, Match, Group, Sort, Sum, ASCENDING, DESCENDING
)

# Define your Beanie document
class Order(Document):
    customer_id: str
    status: str
    amount: float
    category: str

    class Settings:
        name = "orders"


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

# Execute with Beanie - pass pipeline directly!
async def get_category_totals():
    results = await Order.aggregate(pipeline).to_list()
    return results
```

## Using Sort Direction Constants

Mongo Aggro provides `ASCENDING` (1) and `DESCENDING` (-1) constants:

```python
from mongo_aggro import (
    Pipeline, Sort, ASCENDING, DESCENDING
)

# Using constants for better readability
pipeline = Pipeline([
    Sort(fields={
        "created_at": DESCENDING,
        "name": ASCENDING
    })
])

# Use with with_sort method
aggregation_input = pipeline.with_sort({
    "total": DESCENDING,
    "name": ASCENDING
})
```

## Pagination Pattern

Mongo Aggro provides the `with_sort()` method specifically designed for
pagination utilities common in Beanie applications.

### Basic Pagination Setup

```python
from typing import Any
from pydantic import BaseModel, Field

# Type definitions (these match common pagination patterns)
SortSpec = dict[str, int]
AggregationInput = tuple[list[dict[str, Any]], SortSpec]


class PaginatedResponse[T](BaseModel):
    data: list[T] = Field(default_factory=list)
    count: int = Field(0, ge=0)


class PaginationQuery(BaseModel):
    offset: int = Field(0, ge=0)
    limit: int = Field(15, ge=0)

    @property
    def skip(self) -> int:
        return self.limit * self.offset

    async def paginate_and_cast(
        self,
        query,
        projection_model: type,
        aggregation_input: AggregationInput | None = None,
    ) -> PaginatedResponse:
        # Your pagination implementation
        ...
```

### Using with Pagination

```python
from mongo_aggro import (
    Pipeline, Match, Group, Sort, Project, DESCENDING, Sum
)
from pydantic import BaseModel


# Output model for aggregation results
class SalesReportOut(BaseModel):
    category: str
    total_sales: float
    order_count: int


# Query model with pagination
class ReportQuery(PaginationQuery):
    start_date: datetime
    end_date: datetime


async def get_sales_report(
    q: ReportQuery,
    category: str | None = None,
) -> PaginatedResponse[SalesReportOut]:
    # Build the aggregation pipeline
    match_query = {
        "order_date": {"$gte": q.start_date, "$lte": q.end_date},
        "status": "completed"
    }
    if category:
        match_query["category"] = category

    pipeline = Pipeline([
        Match(query=match_query),
        Group(
            id="$category",
            total_sales=Sum(name="total_sales", field="amount").to_expr(),
            order_count={"$sum": 1}
        ),
        Project(fields={
            "_id": 0,
            "category": "$_id",
            "total_sales": 1,
            "order_count": 1
        })
    ])

    # Use with_sort() for pagination
    return await q.paginate_and_cast(
        query=Order.find(),
        projection_model=SalesReportOut,
        aggregation_input=pipeline.with_sort({"total_sales": DESCENDING})
    )
```

## Extending with Raw Stages

For complex operations not covered by typed classes, use `extend_raw()`:

```python
from mongo_aggro import Pipeline, Match, DESCENDING

pipeline = Pipeline([
    Match(query={"status": "active"}),
])

# Add complex raw stages
pipeline.extend_raw([
    {
        "$lookup": {
            "from": "targets",
            "let": {"item_id": "$item_id"},
            "pipeline": [
                {"$match": {"$expr": {"$eq": ["$ItemId", "$$item_id"]}}}
            ],
            "as": "target"
        }
    },
    {"$unwind": {"path": "$target", "preserveNullAndEmptyArrays": True}},
    {
        "$project": {
            "_id": 0,
            "item_id": 1,
            "name": 1,
            "target_value": {"$ifNull": ["$target.value", 0]},
        }
    }
])

# Execute - pipeline is directly iterable
results = await SomeDocument.aggregate(pipeline).to_list()
```

## Combining with Beanie Operators

You can mix Beanie's operators with Mongo Aggro stages:

```python
from beanie.operators import In, And, Or
from mongo_aggro import Pipeline, Match, Group, Project, Sum

# Use Beanie for the initial query
query = Order.find(
    Order.status == "completed",
    Or(
        And(Order.year == 2024, In(Order.month, [1, 2, 3])),
        And(Order.year == 2023, In(Order.month, [10, 11, 12]))
    )
)

# Use Mongo Aggro for aggregation stages
pipeline = Pipeline([
    Group(
        id={"product_id": "$product_id", "label": "$label"},
        value=Sum(name="value", field="data").to_expr(),
    ),
    Project(fields={
        "product_id": "$_id.product_id",
        "label": "$_id.label",
        "value": 1,
        "_id": 0
    })
])

# Execute - pass pipeline directly
results = await query.aggregate(
    pipeline,
    projection_model=ProductChartData
).to_list()
```

## Complex Lookup with Sub-Pipeline

```python
from mongo_aggro import Pipeline, Match, ASCENDING, DESCENDING

pipeline = Pipeline([
    Match(query={"product_id": product_id}),
])

# Add lookup with sub-pipeline
pipeline.extend_raw([
    {
        "$lookup": {
            "from": "reviews",
            "let": {"product_id": "$_id"},
            "pipeline": [
                {
                    "$match": {
                        "$expr": {"$eq": ["$product_id", "$$product_id"]},
                    }
                },
                {
                    "$project": {
                        "_id": 0,
                        "rating": 1,
                        "comment": 1,
                        "created_at": 1,
                    }
                },
            ],
            "as": "reviews",
        }
    },
    {
        "$addFields": {
            "avg_rating": {"$avg": "$reviews.rating"},
            "review_count": {"$size": "$reviews"},
        }
    },
])

# Execute with pagination
return await q.paginate_and_cast(
    query=Product.find(),
    projection_model=ProductWithReviews,
    aggregation_input=pipeline.with_sort({
        "avg_rating": DESCENDING,
        "review_count": DESCENDING,
    }),
)
```

## Tips for Beanie Integration

1. **Pass Pipeline directly** - It implements `__iter__` for direct use
2. **Use sort constants** - `ASCENDING` and `DESCENDING` for readability
3. **Use `with_sort()` for pagination** - Integrates with pagination utilities
4. **Use `extend_raw()` for complex stages** - When typed classes don't cover
   your use case
5. **Mix Beanie operators with Mongo Aggro** - Use Beanie for queries,
   Mongo Aggro for aggregation
6. **Type your output models** - Use `projection_model` for type-safe results

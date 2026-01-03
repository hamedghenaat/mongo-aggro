# MongoEngine Integration

[MongoEngine](http://mongoengine.org/) is a Document-Object Mapper for
working with MongoDB from Python. While it's synchronous, Mongo Aggro
works seamlessly with its aggregation framework.

## Installation

```bash
pip install mongo-aggro mongoengine
```

## Basic Usage

The Pipeline class implements `__iter__`, so you can pass it directly to
MongoEngine's aggregate method:

```python
from mongoengine import Document, StringField, FloatField, connect
from mongo_aggro import (
    Pipeline, Match, Group, Sort, Sum, ASCENDING, DESCENDING
)

# Connect to MongoDB
connect('mydb')


# Define your MongoEngine document
class Order(Document):
    customer_id = StringField(required=True)
    status = StringField(required=True)
    amount = FloatField(required=True)
    category = StringField()

    meta = {'collection': 'orders'}


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

# Execute with MongoEngine - pass pipeline directly!
def get_category_totals():
    results = list(Order.objects.aggregate(pipeline))
    return results
```

## Using Sort Direction Constants

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
```

## Using the Aggregation Framework

MongoEngine provides direct access to the aggregation framework through
the `aggregate()` method on QuerySets:

```python
from mongo_aggro import Pipeline, Match, Group, Unwind, Lookup, DESCENDING

# Complex aggregation with joins
pipeline = Pipeline([
    Match(query={"status": "active"}),
    Lookup(
        from_collection="customers",
        local_field="customer_id",
        foreign_field="_id",
        as_field="customer"
    ),
    Unwind(path="customer"),
    Group(
        id="$customer.region",
        total={"$sum": "$amount"},
        count={"$sum": 1}
    )
])

# Execute - pass pipeline directly
results = Order.objects.aggregate(pipeline)
for doc in results:
    print(f"Region: {doc['_id']}, Total: {doc['total']}")
```

## Combining with MongoEngine Queries

You can use MongoEngine's query syntax to filter before aggregation:

```python
from datetime import datetime
from mongoengine import DateTimeField
from mongo_aggro import DESCENDING

class Sale(Document):
    product_id = StringField()
    amount = FloatField()
    date = DateTimeField()
    region = StringField()

    meta = {'collection': 'sales'}


def get_monthly_sales(year: int, month: int, region: str = None):
    # Start with a filtered queryset
    queryset = Sale.objects(
        date__gte=datetime(year, month, 1),
        date__lt=datetime(year, month + 1, 1) if month < 12
            else datetime(year + 1, 1, 1)
    )

    if region:
        queryset = queryset.filter(region=region)

    # Build aggregation
    pipeline = Pipeline([
        Group(
            id={"product": "$product_id", "day": {"$dayOfMonth": "$date"}},
            daily_total={"$sum": "$amount"},
            count={"$sum": 1}
        ),
        Group(
            id="$_id.product",
            daily_sales={"$push": {
                "day": "$_id.day",
                "total": "$daily_total",
                "count": "$count"
            }},
            monthly_total={"$sum": "$daily_total"}
        ),
        Sort(fields={"monthly_total": DESCENDING})
    ])

    # Pass pipeline directly
    return list(queryset.aggregate(pipeline))
```

## Working with Embedded Documents

MongoEngine supports embedded documents, and Mongo Aggro can work with them:

```python
from mongoengine import EmbeddedDocument, EmbeddedDocumentField, ListField
from mongo_aggro import DESCENDING

class Address(EmbeddedDocument):
    city = StringField()
    country = StringField()

class Customer(Document):
    name = StringField()
    addresses = ListField(EmbeddedDocumentField(Address))

    meta = {'collection': 'customers'}


# Aggregate by city
pipeline = Pipeline([
    Unwind(path="addresses"),
    Group(
        id="$addresses.city",
        customer_count={"$sum": 1}
    ),
    Sort(fields={"customer_count": DESCENDING})
])

# Pass pipeline directly
city_stats = list(Customer.objects.aggregate(pipeline))
```

## Pagination Pattern

For paginated aggregation results:

```python
from typing import TypeVar, Generic
from pydantic import BaseModel
from mongo_aggro import DESCENDING

T = TypeVar('T')


class PaginatedResult(BaseModel, Generic[T]):
    data: list[T]
    total: int
    page: int
    page_size: int


def paginate_aggregation(
    model_class,
    pipeline: Pipeline,
    page: int = 1,
    page_size: int = 20,
    sort_field: str = "_id",
    sort_order: int = DESCENDING
):
    # Add pagination stages
    skip = (page - 1) * page_size

    # Clone pipeline and add count facet
    count_pipeline = pipeline.to_list() + [{"$count": "total"}]
    data_pipeline = pipeline.to_list() + [
        {"$sort": {sort_field: sort_order}},
        {"$skip": skip},
        {"$limit": page_size}
    ]

    # Get total count
    count_result = list(model_class.objects.aggregate(count_pipeline))
    total = count_result[0]['total'] if count_result else 0

    # Get paginated data
    data = list(model_class.objects.aggregate(data_pipeline))

    return {
        'data': data,
        'total': total,
        'page': page,
        'page_size': page_size
    }


# Usage
pipeline = Pipeline([
    Match(query={"status": "completed"}),
    Group(
        id="$category",
        total={"$sum": "$amount"}
    )
])

result = paginate_aggregation(
    Order,
    pipeline,
    page=1,
    page_size=10,
    sort_field="total",
    sort_order=DESCENDING
)
```

## Using Raw Stages

For complex aggregations not covered by typed stages:

```python
pipeline = Pipeline([
    Match(query={"type": "sale"})
])

# Add complex raw stages
pipeline.extend_raw([
    {
        "$graphLookup": {
            "from": "categories",
            "startWith": "$category_id",
            "connectFromField": "parent_id",
            "connectToField": "_id",
            "as": "category_hierarchy",
            "maxDepth": 5
        }
    },
    {
        "$addFields": {
            "root_category": {
                "$arrayElemAt": ["$category_hierarchy", -1]
            }
        }
    }
])

# Pass pipeline directly
results = Order.objects.aggregate(pipeline)
```

## Django Integration

MongoEngine works with Django through `django-mongoengine`:

```python
# settings.py
MONGODB_DATABASES = {
    'default': {
        'name': 'mydb',
        'host': 'localhost',
        'port': 27017,
    }
}

# views.py
from django.http import JsonResponse
from mongo_aggro import Pipeline, Match, Group, Sort, DESCENDING

from .models import Order


def category_report(request):
    pipeline = Pipeline([
        Match(query={"status": "completed"}),
        Group(
            id="$category",
            total={"$sum": "$amount"},
            count={"$sum": 1}
        ),
        Sort(fields={"total": DESCENDING})
    ])

    # Pass pipeline directly
    results = list(Order.objects.aggregate(pipeline))

    return JsonResponse({
        'categories': [
            {
                'name': r['_id'],
                'total': r['total'],
                'count': r['count']
            }
            for r in results
        ]
    })
```

## Tips for MongoEngine Integration

1. **Pass Pipeline directly** - It implements `__iter__` for direct use
2. **Use sort constants** - `ASCENDING` and `DESCENDING` for readability
3. **Chain with queryset filters** - Filter before aggregation for efficiency
4. **Use `extend_raw()` for unsupported stages** - GraphLookup, $facet, etc.
5. **Handle ObjectId conversions** - MongoEngine uses ObjectId, convert
   as needed
6. **Consider indexing** - Ensure indexes support your aggregation queries

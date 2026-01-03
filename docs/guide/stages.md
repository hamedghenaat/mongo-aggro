# Stages

Mongo Aggro provides classes for all major MongoDB aggregation stages. Each stage is a Pydantic model that serializes to the correct MongoDB format.

## Document Stages

### Match

Filters documents based on query conditions.

```python
from mongo_aggro import Match

# Simple match
Match(query={"status": "active"})
# {"$match": {"status": "active"}}

# With operators
Match(query={"age": {"$gte": 18}, "status": {"$in": ["active", "pending"]}})
```

### Project

Reshapes documents by including, excluding, or computing fields.

```python
from mongo_aggro import Project

Project(fields={
    "_id": 0,
    "name": 1,
    "fullName": {"$concat": ["$firstName", " ", "$lastName"]},
})
# {"$project": {"_id": 0, "name": 1, "fullName": {"$concat": ["$firstName", " ", "$lastName"]}}}
```

### AddFields / Set

Adds new fields to documents.

```python
from mongo_aggro import AddFields, Set

AddFields(fields={"totalPrice": {"$multiply": ["$price", "$quantity"]}})
# {"$addFields": {"totalPrice": {"$multiply": ["$price", "$quantity"]}}}

# Set is an alias for AddFields
Set(fields={"computed": {"$sum": "$values"}})
# {"$set": {"computed": {"$sum": "$values"}}}
```

### Unset

Removes fields from documents.

```python
from mongo_aggro import Unset

Unset(fields=["password", "internalId"])
# {"$unset": ["password", "internalId"]}

# Single field
Unset(fields="tempField")
# {"$unset": "tempField"}
```

### ReplaceRoot / ReplaceWith

Replaces the document with a specified embedded document.

```python
from mongo_aggro import ReplaceRoot, ReplaceWith

ReplaceRoot(new_root="$embedded")
# {"$replaceRoot": {"newRoot": "$embedded"}}

ReplaceWith(replacement={"$mergeObjects": ["$defaults", "$doc"]})
# {"$replaceWith": {"$mergeObjects": ["$defaults", "$doc"]}}
```

## Grouping Stages

### Group

Groups documents by an expression and applies accumulators.

```python
from mongo_aggro import Group, Sum, Avg, merge_accumulators

# Simple group
Group(id="$category", accumulators={"count": {"$sum": 1}})

# With typed accumulators
Group(
    id="$category",
    accumulators=merge_accumulators(
        Sum(name="total", field="amount"),
        Avg(name="average", field="amount"),
    )
)

# Compound _id
Group(
    id={"year": "$year", "month": "$month"},
    accumulators={"count": {"$sum": 1}}
)
```

### SortByCount

Groups by a field and counts occurrences, then sorts by count descending.

```python
from mongo_aggro import SortByCount

SortByCount(expression="$category")
# {"$sortByCount": "$category"}
```

### Bucket

Categorizes documents into buckets based on boundaries.

```python
from mongo_aggro import Bucket

Bucket(
    group_by="$price",
    boundaries=[0, 100, 500, 1000],
    default="Other",
    output={"count": {"$sum": 1}}
)
```

### BucketAuto

Automatically determines bucket boundaries.

```python
from mongo_aggro import BucketAuto

BucketAuto(
    group_by="$price",
    buckets=5,
    granularity="R5"  # Optional: R5, R10, R20, R40, R80, 1-2-5, E6, E12, E24, E48, E96, E192, POWERSOF2
)
```

## Array Stages

### Unwind

Deconstructs an array field into multiple documents.

```python
from mongo_aggro import Unwind

# Simple unwind
Unwind(path="items")
# {"$unwind": "$items"}

# With options
Unwind(
    path="items",
    include_array_index="itemIndex",
    preserve_null_and_empty=True
)
# {"$unwind": {"path": "$items", "includeArrayIndex": "itemIndex", "preserveNullAndEmptyArrays": true}}
```

## Join Stages

### Lookup

Performs a left outer join with another collection.

```python
from mongo_aggro import Lookup, Pipeline, Match

# Simple lookup
Lookup(
    from_collection="orders",
    local_field="customerId",
    foreign_field="customerId",
    as_field="customerOrders"
)

# Lookup with pipeline
Lookup(
    from_collection="orders",
    let={"cust_id": "$customerId"},
    pipeline=Pipeline([
        Match(query={"$expr": {"$eq": ["$customerId", "$$cust_id"]}}),
    ]),
    as_field="matchingOrders"
)
```

### GraphLookup

Performs recursive search on a collection.

```python
from mongo_aggro import GraphLookup

GraphLookup(
    from_collection="employees",
    start_with="$reportsTo",
    connect_from_field="reportsTo",
    connect_to_field="name",
    as_field="reportingHierarchy",
    max_depth=5,
    depth_field="level"
)
```

## Sorting and Pagination

### Sort

Sorts documents by specified fields.

```python
from mongo_aggro import Sort

Sort(fields={"createdAt": -1, "name": 1})
# {"$sort": {"createdAt": -1, "name": 1}}
```

### Limit

Limits the number of documents.

```python
from mongo_aggro import Limit

Limit(count=10)
# {"$limit": 10}
```

### Skip

Skips a number of documents.

```python
from mongo_aggro import Skip

Skip(count=20)
# {"$skip": 20}
```

### Sample

Randomly selects documents.

```python
from mongo_aggro import Sample

Sample(size=5)
# {"$sample": {"size": 5}}
```

## Multi-Pipeline Stages

### Facet

Processes multiple pipelines in a single stage.

```python
from mongo_aggro import Facet, Pipeline, Match, Count, Group

Facet(pipelines={
    "totalCount": Pipeline([Count(field="total")]),
    "byCategory": Pipeline([
        Group(id="$category", accumulators={"count": {"$sum": 1}})
    ]),
})
```

### UnionWith

Combines results from multiple collections.

```python
from mongo_aggro import UnionWith, Pipeline, Match

UnionWith(collection="archive")
# {"$unionWith": "archive"}

# With pipeline
UnionWith(
    collection="archive",
    pipeline=Pipeline([Match(query={"year": 2024})])
)
```

## Output Stages

### Out

Writes results to a collection (replaces if exists).

```python
from mongo_aggro import Out

Out(collection="results")
# {"$out": "results"}

Out(db="otherDb", collection="results")
# {"$out": {"db": "otherDb", "coll": "results"}}
```

### Merge

Merges results into a collection with upsert options.

```python
from mongo_aggro import Merge

Merge(
    into="monthly_totals",
    on="_id",
    when_matched="merge",
    when_not_matched="insert"
)
```

## Other Stages

### Count

Counts documents and outputs as a field.

```python
from mongo_aggro import Count

Count(field="totalDocuments")
# {"$count": "totalDocuments"}
```

### Redact

Restricts content based on document fields.

```python
from mongo_aggro import Redact

Redact(expression={
    "$cond": {
        "if": {"$eq": ["$level", "public"]},
        "then": "$$DESCEND",
        "else": "$$PRUNE"
    }
})
```

### GeoNear

Returns documents sorted by distance from a geospatial point.

```python
from mongo_aggro import GeoNear

GeoNear(
    near={"type": "Point", "coordinates": [-73.99, 40.73]},
    distance_field="distance",
    max_distance=5000,
    spherical=True
)
```

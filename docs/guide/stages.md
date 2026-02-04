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

## Statistics Stages

### CollStats

Returns collection statistics.

```python
from mongo_aggro import CollStats

# Latency statistics with histograms
CollStats(lat_stats={"histograms": True})
# {"$collStats": {"latencyStats": {"histograms": True}}}

# Storage and count statistics
CollStats(storage_stats={}, count={})
# {"$collStats": {"storageStats": {}, "count": {}}}
```

### IndexStats

Returns index usage statistics.

```python
from mongo_aggro import IndexStats

IndexStats()
# {"$indexStats": {}}
```

### PlanCacheStats

Returns query plan cache information.

```python
from mongo_aggro import PlanCacheStats

PlanCacheStats()
# {"$planCacheStats": {}}
```

## Session Stages

### ListSessions

Lists sessions in system.sessions collection.

```python
from mongo_aggro import ListSessions

# All sessions for current user
ListSessions()
# {"$listSessions": {}}

# Sessions for all users (requires privileges)
ListSessions(all_users=True)
# {"$listSessions": {"allUsers": True}}

# Sessions for specific users
ListSessions(users=[{"user": "admin", "db": "admin"}])
# {"$listSessions": {"users": [{"user": "admin", "db": "admin"}]}}
```

### ListLocalSessions

Lists sessions on current mongos/mongod (db.aggregate only).

```python
from mongo_aggro import ListLocalSessions

ListLocalSessions(all_users=True)
# {"$listLocalSessions": {"allUsers": True}}
```

### ListSampledQueries

Lists sampled queries for query analysis.

```python
from mongo_aggro import ListSampledQueries

# All sampled queries
ListSampledQueries()
# {"$listSampledQueries": {}}

# Queries for specific namespace
ListSampledQueries(namespace="mydb.users")
# {"$listSampledQueries": {"namespace": "mydb.users"}}
```

## Change Stream Stages

### ChangeStream

Opens a change stream cursor (must be first stage).

```python
from mongo_aggro import ChangeStream

# Basic change stream
ChangeStream()
# {"$changeStream": {}}

# With full document on update
ChangeStream(full_document="updateLookup")
# {"$changeStream": {"fullDocument": "updateLookup"}}

# With pre-image and expanded events
ChangeStream(
    full_document="whenAvailable",
    full_document_before_change="required",
    show_expanded_events=True
)
```

### ChangeStreamSplitLargeEvent

Splits large change events (>16MB) into fragments.

```python
from mongo_aggro import ChangeStreamSplitLargeEvent

ChangeStreamSplitLargeEvent()
# {"$changeStreamSplitLargeEvent": {}}
```

## Admin Stages

### CurrentOp

Returns current operations (db.aggregate only).

```python
from mongo_aggro import CurrentOp

# All operations
CurrentOp()
# {"$currentOp": {}}

# Include idle connections and all users
CurrentOp(all_users=True, idle_connections=True)
# {"$currentOp": {"allUsers": True, "idleConnections": True}}
```

### ListClusterCatalog

Lists collections in a sharded cluster.

```python
from mongo_aggro import ListClusterCatalog

ListClusterCatalog()
# {"$listClusterCatalog": {}}
```

### ListSearchIndexes

Lists Atlas Search indexes on a collection.

```python
from mongo_aggro import ListSearchIndexes

# All search indexes
ListSearchIndexes()
# {"$listSearchIndexes": {}}

# Specific index by name
ListSearchIndexes(name="my_search_index")
# {"$listSearchIndexes": {"name": "my_search_index"}}
```

## Atlas Search Stages

### Search

Performs full-text search on Atlas Search indexes.

```python
from mongo_aggro import Search

# Text search
Search(index="default", text={"query": "coffee shop", "path": "description"})
# {"$search": {"index": "default", "text": {...}}}

# Compound search with must/should
Search(
    index="default",
    compound={
        "must": [{"text": {"query": "coffee", "path": "title"}}],
        "should": [{"text": {"query": "organic", "path": "tags"}}]
    }
)

# Autocomplete
Search(index="autocomplete", autocomplete={"query": "cof", "path": "name"})
```

### SearchMeta

Returns Atlas Search metadata (counts, facets).

```python
from mongo_aggro import SearchMeta

# Total count
SearchMeta(index="default", count={"type": "total"})
# {"$searchMeta": {"index": "default", "count": {"type": "total"}}}

# Facet results
SearchMeta(index="default", facet={
    "operator": {"text": {"query": "coffee", "path": "description"}},
    "facets": {"categories": {"type": "string", "path": "category"}}
})
```

### VectorSearch

Performs vector similarity search (MongoDB 7.0.2+, Atlas only).

```python
from mongo_aggro import VectorSearch

VectorSearch(
    index="vector_index",
    path="embedding",
    query_vector=[0.1, 0.2, 0.3, 0.4, 0.5],
    num_candidates=100,
    limit=10
)
# {"$vectorSearch": {...}}

# With pre-filter
VectorSearch(
    index="vector_index",
    path="embedding",
    query_vector=[0.1, 0.2, 0.3],
    num_candidates=50,
    limit=5,
    filter={"category": "electronics"}
)
```

## Advanced Stages

### QuerySettings

Returns query settings (MongoDB 8.0+).

```python
from mongo_aggro import QuerySettings

QuerySettings()
# {"$querySettings": {}}
```

### RankFusion

Combines ranked results from multiple pipelines using Reciprocal Rank Fusion.

```python
from mongo_aggro import RankFusion

RankFusion(
    input={
        "text_search": [
            {"$search": {"text": {"query": "coffee", "path": "title"}}}
        ],
        "vector_search": [
            {"$vectorSearch": {"index": "vectors", "path": "embedding"}}
        ]
    },
    combination={"weights": {"text_search": 0.6, "vector_search": 0.4}}
)
```

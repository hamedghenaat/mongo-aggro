# Mongo Aggro

A Python package for building MongoDB aggregation pipelines with Pydantic.

[![PyPI](https://img.shields.io/pypi/v/mongo-aggro)](https://pypi.org/project/mongo-aggro/)
[![Python](https://img.shields.io/pypi/pyversions/mongo-aggro)](https://pypi.org/project/mongo-aggro/)
[![License](https://img.shields.io/pypi/l/mongo-aggro)](https://github.com/hamedghenaat/mongo-aggro/blob/main/LICENSE)

## Features

- **Type-safe** - Pydantic models with full type hints
- **Zero-conversion** - Pass `Pipeline` directly to `collection.aggregate()`
- **Python operators** - Use `F("age") > 18` instead of `{"$gt": ["$age", 18]}`
- **149 expression operators** - Arithmetic, string, date, array, and more
- **46 aggregation stages** - All major MongoDB stages supported
- **31 query predicates** - Comparison, logical, geospatial, bitwise
- **17 accumulators** - Sum, Avg, Min, Max, Push, TopN, etc.

## Installation

```bash
uv add mongo-aggro
# or
pip install mongo-aggro
```

## Quick Start

```python
from mongo_aggro import Pipeline, Match, Group, Sort, F, Expr

# Traditional approach
pipeline = Pipeline([
    Match(query={"status": "active"}),
    Group(id="$category", accumulators={"total": {"$sum": "$amount"}}),
    Sort(fields={"total": -1})
])

# Python operator syntax
pipeline = Pipeline([
    Match(query=Expr(expression=(F("status") == "active")).model_dump()),
    Group(id="$category", accumulators={"total": {"$sum": "$amount"}}),
])

# Pass directly to MongoDB
results = collection.aggregate(pipeline)
```

## Expression Operators with Python Syntax

```python
from mongo_aggro import F, Expr, Match

# Comparison operators
F("age") > 18        # {"$gt": ["$age", 18]}
F("status") == "active"  # {"$eq": ["$status", "active"]}

# Logical operators (use & | ~ instead of and or not)
(F("age") >= 18) & (F("status") == "active")
(F("type") == "premium") | (F("balance") > 1000)

# Use in Match stage
Match(query=Expr(expression=(
    (F("status") == "active") & (F("age") > 18)
)).model_dump())
```

## Stages

| Category | Stages |
|----------|--------|
| **Core** | Match, Project, Group, Sort, Limit, Skip, Unwind, AddFields, Set, Unset |
| **Join** | Lookup, GraphLookup, UnionWith |
| **Aggregation** | Bucket, BucketAuto, Facet, SortByCount, Count |
| **Output** | Out, Merge |
| **Window** | SetWindowFields, Densify, Fill |
| **Geospatial** | GeoNear |
| **Search** | Search, SearchMeta, VectorSearch, RankFusion |
| **Change Stream** | ChangeStream, ChangeStreamSplitLargeEvent |
| **Admin** | CollStats, IndexStats, CurrentOp, ListSessions |

## Expression Operators

| Category | Examples |
|----------|----------|
| **Comparison** | Eq, Ne, Gt, Gte, Lt, Lte, Cmp |
| **Logical** | And, Or, Not |
| **Arithmetic** | Add, Subtract, Multiply, Divide, Mod, Abs, Ceil, Floor |
| **String** | Concat, Split, ToLower, ToUpper, Trim, RegexMatch |
| **Array** | ArraySize, Filter, Map, Reduce, Slice, InArray |
| **Date** | DateAdd, DateDiff, DateToString, Year, Month, Day |
| **Type** | ToDate, ToString, ToInt, Convert, Type |
| **Conditional** | Cond, IfNull, Switch |
| **Set** | SetUnion, SetIntersection, SetDifference |
| **Window** | Rank, DenseRank, Shift, ExpMovingAvg |

## Query Predicates

```python
from mongo_aggro import Match, In, Regex, Exists, GeoWithin

Match(query={
    "status": In(values=["active", "pending"]).model_dump(),
    "email": Regex(pattern="@company\\.com$").model_dump(),
    "profile": Exists(exists=True).model_dump(),
})
```

## Accumulators

```python
from mongo_aggro import Group, Sum, Avg, Max, Push, merge_accumulators

Group(
    id="$category",
    accumulators=merge_accumulators(
        Sum(name="total", field="amount"),
        Avg(name="average", field="price"),
        Max(name="highest", field="price"),
    )
)
```

## Documentation

- [User Guide](https://hamedghenaat.github.io/mongo-aggro/guide/)
- [API Reference](https://hamedghenaat.github.io/mongo-aggro/api/)
- [Examples](https://hamedghenaat.github.io/mongo-aggro/examples/)

## License

MIT

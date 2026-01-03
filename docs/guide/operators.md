# Operators

Mongo Aggro provides query operator classes for building complex filter conditions in `Match` stages and other contexts.

## Logical Operators

### And

Combines multiple conditions with AND logic.

```python
from mongo_aggro import And, Match

Match(query=And(conditions=[
    {"status": "active"},
    {"age": {"$gte": 18}},
    {"verified": True},
]).model_dump())
# {"$match": {"$and": [{"status": "active"}, {"age": {"$gte": 18}}, {"verified": true}]}}
```

### Or

Combines conditions with OR logic.

```python
from mongo_aggro import Or, Match

Match(query=Or(conditions=[
    {"status": "active"},
    {"status": "pending"},
]).model_dump())
# {"$match": {"$or": [{"status": "active"}, {"status": "pending"}]}}
```

### Not

Negates a condition.

```python
from mongo_aggro import Not

Not(condition={"$regex": "^test"})
# {"$not": {"$regex": "^test"}}
```

### Nor

None of the conditions should match.

```python
from mongo_aggro import Nor

Nor(conditions=[
    {"status": "deleted"},
    {"status": "archived"},
])
# {"$nor": [{"status": "deleted"}, {"status": "archived"}]}
```

## Expression Operator

### Expr

Allows use of aggregation expressions in query context.

```python
from mongo_aggro import Expr, Match

# Compare two fields
Match(query=Expr(expression={"$eq": ["$field1", "$field2"]}).model_dump())

# Complex expression
Match(query=Expr(expression={
    "$and": [
        {"$gt": ["$quantity", "$minQuantity"]},
        {"$lt": ["$price", "$maxPrice"]},
    ]
}).model_dump())
```

## Comparison Operators

### Eq / Ne

Equal and not equal comparisons.

```python
from mongo_aggro import Eq, Ne

Eq(value=5)
# {"$eq": 5}

Ne(value="deleted")
# {"$ne": "deleted"}
```

### Gt / Gte / Lt / Lte

Greater than, greater than or equal, less than, less than or equal.

```python
from mongo_aggro import Gt, Gte, Lt, Lte

Gt(value=10)    # {"$gt": 10}
Gte(value=18)   # {"$gte": 18}
Lt(value=100)   # {"$lt": 100}
Lte(value=65)   # {"$lte": 65}
```

### In / Nin

Match values in or not in an array.

```python
from mongo_aggro import In, Nin

In(values=["active", "pending", "review"])
# {"$in": ["active", "pending", "review"]}

Nin(values=["deleted", "archived"])
# {"$nin": ["deleted", "archived"]}
```

## String Operators

### Regex

Pattern matching with regular expressions.

```python
from mongo_aggro import Regex

# Simple pattern
Regex(pattern="^test")
# {"$regex": "^test"}

# With options (i=case-insensitive, m=multiline)
Regex(pattern="hello", options="i")
# {"$regex": "hello", "$options": "i"}
```

## Field Operators

### Exists

Check if a field exists.

```python
from mongo_aggro import Exists

Exists(exists=True)   # {"$exists": true}
Exists(exists=False)  # {"$exists": false}
Exists()              # {"$exists": true} (default)
```

### Type

Match documents where field is of a specific BSON type.

```python
from mongo_aggro import Type

Type(bson_type="string")
# {"$type": "string"}

Type(bson_type=2)  # Numeric type code
# {"$type": 2}

Type(bson_type=["string", "int"])  # Multiple types
# {"$type": ["string", "int"]}
```

## Array Operators

### ElemMatch

Match documents where array contains element matching all conditions.

```python
from mongo_aggro import ElemMatch

ElemMatch(conditions={
    "quantity": {"$gt": 5},
    "price": {"$lt": 100},
})
# {"$elemMatch": {"quantity": {"$gt": 5}, "price": {"$lt": 100}}}
```

### Size

Match arrays of a specific size.

```python
from mongo_aggro import Size

Size(size=5)
# {"$size": 5}
```

### All

Match arrays containing all specified elements.

```python
from mongo_aggro import All

All(values=["red", "green", "blue"])
# {"$all": ["red", "green", "blue"]}
```

## Combining Operators in Match

Operators can be combined to build complex queries:

```python
from mongo_aggro import Match, And, Or, In, Gte, Lte, Exists, Regex

# Complex query combining multiple operators
pipeline = Pipeline([
    Match(query={
        "$and": [
            {"status": {"$in": ["active", "pending"]}},
            {"age": {"$gte": 18, "$lte": 65}},
            {"email": {"$exists": True, "$regex": "@company\\.com$"}},
            {"$or": [
                {"priority": "high"},
                {"amount": {"$gt": 1000}},
            ]},
        ]
    }),
])

# Or using operator classes
Match(query=And(conditions=[
    In(values=["active", "pending"]).model_dump(),  # for status field
    {"age": {**Gte(value=18).model_dump(), **Lte(value=65).model_dump()}},
    Or(conditions=[
        {"priority": "high"},
        {"amount": {"$gt": 1000}},
    ]).model_dump(),
]).model_dump())
```

## Using Operators with Fields

Operators are typically used as values for field conditions:

```python
from mongo_aggro import Match, Gte, In, Regex

# Direct dictionary usage (most common)
Match(query={
    "age": {"$gte": 18},
    "status": {"$in": ["active", "pending"]},
    "name": {"$regex": "^John", "$options": "i"},
})

# Using operator classes for reusability
age_filter = Gte(value=18).model_dump()
status_filter = In(values=["active", "pending"]).model_dump()
name_filter = Regex(pattern="^John", options="i").model_dump()

Match(query={
    "age": age_filter,
    "status": status_filter,
    "name": name_filter,
})
```

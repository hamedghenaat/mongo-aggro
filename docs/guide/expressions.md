# Expressions

Expression operators are used within aggregation stages like `$project`,
`$addFields`, and `$match` (via `$expr`) to compute values, transform data,
and perform comparisons.

## Quick Start

```python
from mongo_aggro import Match, Project, Expr
from mongo_aggro.expressions import F, AddExpr, ConcatExpr, CondExpr

# Use F() to reference fields
pipeline = Pipeline([
    # Match with expression comparison
    Match(query=Expr((F("status") == "active") & (F("age") > 18))),
    # Project with computed fields
    Project(fields={
        "name": 1,
        "total": AddExpr(values=[F("price"), F("tax")]),
        "greeting": ConcatExpr(strings=["Hello, ", F("name"), "!"]),
    })
])
```

## Field References

Use `F()` to create field references:

```python
from mongo_aggro.expressions import F

F("name")       # References "$name"
F("user.age")   # Nested field "$user.age"
F("$total")     # Already prefixed, stays "$total"
```

## Expression Categories

### Arithmetic Expressions

```python
from mongo_aggro.expressions import (
    AddExpr, SubtractExpr, MultiplyExpr, DivideExpr,
    AbsExpr, ModExpr, CeilExpr, FloorExpr, RoundExpr,
    SqrtExpr, PowExpr, ExpExpr, LnExpr, LogExpr
)

# Add values
AddExpr(values=[F("price"), F("tax"), 5])
# {"$add": ["$price", "$tax", 5]}

# Multiply
MultiplyExpr(values=[F("quantity"), F("price")])
# {"$multiply": ["$quantity", "$price"]}

# Power and sqrt
PowExpr(base=F("x"), exponent=2)
SqrtExpr(value=F("variance"))
```

### Comparison Expressions

Use Python operators with `F()`:

```python
from mongo_aggro.expressions import F

# Python operators → MongoDB expressions
F("status") == "active"   # {"$eq": ["$status", "active"]}
F("age") > 18             # {"$gt": ["$age", 18]}
F("score") >= 80          # {"$gte": ["$score", 80]}
F("price") < 100          # {"$lt": ["$price", 100]}
F("level") <= 5           # {"$lte": ["$level", 5]}
F("type") != "deleted"    # {"$ne": ["$type", "deleted"]}
```

Or use explicit classes:

```python
from mongo_aggro.expressions import EqExpr, GtExpr, LtExpr, CmpExpr

EqExpr(left=F("a"), right=F("b"))
CmpExpr(left=F("a"), right=F("b"))  # Returns -1, 0, or 1
```

### Logical Expressions

Use `&`, `|`, `~` operators (not `and`, `or`, `not`):

```python
from mongo_aggro.expressions import F

# AND - use &
expr = (F("status") == "active") & (F("age") > 18)
# {"$and": [{"$eq": ["$status", "active"]}, {"$gt": ["$age", 18]}]}

# OR - use |
expr = (F("type") == "A") | (F("type") == "B")
# {"$or": [{"$eq": ["$type", "A"]}, {"$eq": ["$type", "B"]}]}

# NOT - use ~
expr = ~(F("deleted") == True)
# {"$not": {"$eq": ["$deleted", true]}}
```

**Important:** Parentheses are required due to operator precedence.

### Conditional Expressions

```python
from mongo_aggro.expressions import CondExpr, IfNullExpr, SwitchExpr

# If-then-else
CondExpr(
    if_=F("score") > 80,
    then="passed",
    else_="failed"
)
# {"$cond": {"if": {"$gt": ["$score", 80]}, ...}}

# Null coalescing
IfNullExpr(expression=F("nickname"), replacement=F("name"))
# {"$ifNull": ["$nickname", "$name"]}

# Switch statement
SwitchExpr(
    branches=[
        SwitchBranch(case=F("grade") >= 90, then="A"),
        SwitchBranch(case=F("grade") >= 80, then="B"),
    ],
    default="C"
)
```

### String Expressions

```python
from mongo_aggro.expressions import (
    ConcatExpr, SplitExpr, ToLowerExpr, ToUpperExpr,
    TrimExpr, SubstrCPExpr, RegexMatchExpr
)

# Concatenate
ConcatExpr(strings=[F("first"), " ", F("last")])
# {"$concat": ["$first", " ", "$last"]}

# Split
SplitExpr(string=F("tags"), delimiter=",")
# {"$split": ["$tags", ","]}

# Case conversion
ToUpperExpr(value=F("code"))
ToLowerExpr(value=F("email"))

# Regex match
RegexMatchExpr(input=F("email"), regex=r"@gmail\.com$")
```

### Array Expressions

```python
from mongo_aggro.expressions import (
    ArraySizeExpr, SliceExpr, FilterExpr, MapExpr,
    ReduceExpr, ArrayElemAtExpr, ConcatArraysExpr
)

# Array size
ArraySizeExpr(array=F("items"))
# {"$size": "$items"}

# Slice
SliceExpr(array=F("items"), n=3)           # First 3
SliceExpr(array=F("items"), position=2, n=5)  # From index 2

# Filter
FilterExpr(input=F("items"), cond=F("$$this.active") == True)
# {"$filter": {"input": "$items", "cond": ...}}

# Map
MapExpr(
    input=F("items"),
    in_=F("$$this.price") * 1.1  # 10% markup
)
```

### Date Expressions

```python
from mongo_aggro.expressions import (
    DateAddExpr, DateDiffExpr, DateToStringExpr,
    YearExpr, MonthExpr, DayOfMonthExpr
)

# Add time
DateAddExpr(start_date=F("created"), unit="day", amount=30)
# {"$dateAdd": {"startDate": "$created", "unit": "day", "amount": 30}}

# Difference
DateDiffExpr(start_date=F("start"), end_date=F("end"), unit="hour")

# Format
DateToStringExpr(date=F("created"), format="%Y-%m-%d")
# {"$dateToString": {"date": "$created", "format": "%Y-%m-%d"}}

# Extract parts
YearExpr(date=F("created"))
MonthExpr(date=F("created"))
```

### Type Conversion

```python
from mongo_aggro.expressions import (
    ToStringExpr, ToIntExpr, ToDoubleExpr, ToBoolExpr,
    ToDateExpr, ConvertExpr, TypeExpr
)

# Simple conversions
ToStringExpr(value=F("count"))
ToIntExpr(value=F("price"))
ToDateExpr(value=F("timestamp"))

# With error handling
ConvertExpr(input=F("value"), to="int", on_error=0)
# {"$convert": {"input": "$value", "to": "int", "onError": 0}}

# Get type
TypeExpr(value=F("field"))
# {"$type": "$field"}
```

### Set Expressions

```python
from mongo_aggro.expressions import (
    SetUnionExpr, SetIntersectionExpr, SetDifferenceExpr,
    SetEqualsExpr, SetIsSubsetExpr
)

# Union
SetUnionExpr(arrays=[F("tags"), F("categories")])

# Intersection
SetIntersectionExpr(arrays=[F("requiredSkills"), F("userSkills")])

# Difference
SetDifferenceExpr(array1=F("all"), array2=F("completed"))
```

### Object Expressions

```python
from mongo_aggro.expressions import (
    MergeObjectsExpr, ObjectToArrayExpr, GetFieldExpr, SetFieldExpr
)

# Merge
MergeObjectsExpr(objects=[F("defaults"), F("overrides")])
# {"$mergeObjects": ["$defaults", "$overrides"]}

# Get field dynamically
GetFieldExpr(field=F("fieldName"), input=F("doc"))

# Object to array
ObjectToArrayExpr(object=F("metadata"))
# {"$objectToArray": "$metadata"}
```

### Window Expressions

For use in `$setWindowFields`:

```python
from mongo_aggro.expressions import (
    RankExpr, DenseRankExpr, ShiftExpr, ExpMovingAvgExpr
)

# Ranking
RankExpr()           # {"$rank": {}}
DenseRankExpr()      # {"$denseRank": {}}

# Shift values
ShiftExpr(output=F("value"), by=-1, default=0)  # Previous value

# Moving average
ExpMovingAvgExpr(input=F("price"), n=7)  # 7-day EMA
```

## Nesting Expressions

Expressions nest automatically - no manual `model_dump()` needed:

```python
from mongo_aggro.expressions import (
    F, CondExpr, AddExpr, MultiplyExpr, GtExpr
)

# Deeply nested expression
expr = CondExpr(
    if_=GtExpr(left=F("quantity"), right=10),
    then=MultiplyExpr(values=[F("price"), 0.9]),  # 10% discount
    else_=F("price")
)

# Serializes recursively
expr.model_dump()
# {
#   "$cond": {
#     "if": {"$gt": ["$quantity", 10]},
#     "then": {"$multiply": ["$price", 0.9]},
#     "else": "$price"
#   }
# }
```

## Using in Stages

```python
from mongo_aggro import Pipeline, Match, Project, Expr
from mongo_aggro.expressions import F, AddExpr, ConcatExpr

pipeline = Pipeline([
    Match(query=Expr((F("status") == "active") & (F("stock") > 0))),
    Project(fields={
        "name": 1,
        "total": AddExpr(values=[F("price"), F("shipping")]),
        "display": ConcatExpr(strings=[F("brand"), " - ", F("model")]),
    })
])

# Pass directly to MongoDB
results = collection.aggregate(pipeline)
```

## Available Expression Categories

| Category | Module | Count |
|----------|--------|-------|
| Arithmetic | `expressions.arithmetic` | 16 |
| Array | `expressions.array` | 17 |
| Bitwise | `expressions.bitwise` | 4 |
| Comparison | `expressions.comparison` | 7 |
| Conditional | `expressions.conditional` | 4 |
| Date | `expressions.date` | 22 |
| Encrypted | `expressions.encrypted` | 4 |
| Logical | `expressions.logical` | 3 |
| Object | `expressions.object` | 5 |
| Set | `expressions.set` | 7 |
| Size | `expressions.size` | 2 |
| String | `expressions.string` | 15 |
| Trigonometry | `expressions.trigonometry` | 15 |
| Type | `expressions.type` | 10 |
| Variable | `expressions.variable` | 3 |
| Window | `expressions.window` | 15 |

**Total: 149 expression operators**

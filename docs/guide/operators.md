# Operators

Mongo Aggro provides query operator classes for building complex filter
conditions in `Match` stages and other contexts.

## Expression Operators with Python Syntax

The most ergonomic way to build expressions is using Python's native
operators with the `F()` field helper:

```python
from mongo_aggro import F, Expr, Match, Pipeline

# Build expressions with Python operators
expr = (F("status") == "active") & (F("age") > 18)

# Use in Match stage
pipeline = Pipeline([
    Match(query=Expr(expression=expr).model_dump())
])
# Outputs: {"$match": {"$expr": {"$and": [
#     {"$eq": ["$status", "active"]},
#     {"$gt": ["$age", 18]}
# ]}}}
```

### Field Reference with F()

`F()` creates a field reference that supports operator overloading:

```python
from mongo_aggro import F

# Basic field reference
F("name")       # References "$name"
F("user.age")   # References "$user.age" (nested)
F("$total")     # Already prefixed, stays "$total"
```

### Comparison Operators

| Python | MongoDB | Example |
|--------|---------|---------|
| `==`   | `$eq`   | `F("status") == "active"` |
| `!=`   | `$ne`   | `F("status") != "deleted"` |
| `>`    | `$gt`   | `F("age") > 18` |
| `>=`   | `$gte`  | `F("score") >= 80` |
| `<`    | `$lt`   | `F("price") < 100` |
| `<=`   | `$lte`  | `F("level") <= 5` |

### Logical Operators

**Important:** Python's `and`, `or`, `not` keywords cannot be overloaded.
Use bitwise operators instead:

| Python | MongoDB | Example |
|--------|---------|---------|
| `&`    | `$and`  | `(F("a") == 1) & (F("b") == 2)` |
| `\|`   | `$or`   | `(F("a") == 1) \| (F("b") == 2)` |
| `~`    | `$not`  | `~(F("status") == "deleted")` |

**Note:** Parentheses are required due to operator precedence!

```python
from mongo_aggro import F, Expr

# Complex expression with AND, OR, NOT
expr = (
    (F("status") == "active")
    & (F("verified") == True)
    & (
        (F("score") >= 90)
        | (F("bonus") > 0)
    )
)

# Negation
not_deleted = ~(F("status") == "deleted")
```

### Chaining Flattens Automatically

Chained `&` or `|` operators are flattened into a single `$and` / `$or`:

```python
from mongo_aggro import F

# These chains create a single $and with 3 conditions
expr = (F("a") == 1) & (F("b") == 2) & (F("c") == 3)
# {"$and": [{"$eq": ["$a", 1]}, {"$eq": ["$b", 2]}, {"$eq": ["$c", 3]}]}
```

### Using with Expr in Match

```python
from mongo_aggro import F, Expr, Match, Pipeline

# Build the expression
filter_expr = (
    (F("status") == "active")
    & (F("age") >= 18)
    & ((F("role") == "admin") | (F("level") > 5))
)

# Use in pipeline
pipeline = Pipeline([
    Match(query=Expr(expression=filter_expr).model_dump())
])
```

---

## Arithmetic Expressions

Perform mathematical operations on field values.

### AddExpr - Addition

```python
from mongo_aggro import F, AddExpr, Project, Pipeline

# Add two fields
total = AddExpr(operands=[F("price"), F("tax")])

# Add multiple values
pipeline = Pipeline([
    Project(fields={
        "total": AddExpr(operands=[F("subtotal"), F("tax"), F("shipping")]).model_dump(),
        "adjusted": AddExpr(operands=[F("price"), 10]).model_dump(),
    })
])
```

### SubtractExpr - Subtraction

```python
from mongo_aggro import F, SubtractExpr

# Calculate profit margin
profit = SubtractExpr(left=F("revenue"), right=F("cost"))

# Subtract a constant
discounted = SubtractExpr(left=F("price"), right=5)
```

### MultiplyExpr - Multiplication

```python
from mongo_aggro import F, MultiplyExpr

# Calculate line total
line_total = MultiplyExpr(operands=[F("price"), F("quantity")])

# Apply discount percentage
discounted = MultiplyExpr(operands=[F("price"), 0.9])  # 10% off
```

### DivideExpr - Division

```python
from mongo_aggro import F, DivideExpr

# Calculate average
average = DivideExpr(dividend=F("total"), divisor=F("count"))

# Calculate percentage
percentage = DivideExpr(dividend=F("completed"), divisor=F("total"))
```

### Combining Arithmetic Expressions

```python
from mongo_aggro import F, AddExpr, MultiplyExpr, DivideExpr, Project, Pipeline

# Complex calculation: (price * quantity) + tax
pipeline = Pipeline([
    Project(fields={
        "final_price": AddExpr(operands=[
            MultiplyExpr(operands=[F("price"), F("qty")]),
            F("tax")
        ]).model_dump()
    })
])

# Nested: ((a + b) * c) / d
result = DivideExpr(
    dividend=MultiplyExpr(operands=[
        AddExpr(operands=[F("a"), F("b")]),
        F("c")
    ]),
    divisor=F("d")
)
```

---

## Conditional Expressions

Implement branching logic in aggregation pipelines.

### CondExpr - If/Then/Else

```python
from mongo_aggro import F, CondExpr, Project, Pipeline

# Simple conditional
pipeline = Pipeline([
    Project(fields={
        "category": CondExpr(
            if_=(F("qty") > 100),
            then="bulk",
            else_="retail"
        ).model_dump()
    })
])

# Nested conditionals for multiple conditions
tier = CondExpr(
    if_=(F("score") >= 90),
    then="gold",
    else_=CondExpr(
        if_=(F("score") >= 70),
        then="silver",
        else_="bronze"
    )
)
```

### IfNullExpr - Null Coalescing

```python
from mongo_aggro import F, IfNullExpr

# Provide default for null fields
name = IfNullExpr(input=F("nickname"), replacement=F("fullName"))

# Chain defaults
display = IfNullExpr(
    input=F("displayName"),
    replacement=IfNullExpr(input=F("username"), replacement="Anonymous")
)
```

### SwitchExpr - Multi-Branch Conditional

```python
from mongo_aggro import F, SwitchExpr, SwitchBranch, EqExpr, Project, Pipeline

# Map status codes to labels
pipeline = Pipeline([
    Project(fields={
        "status_label": SwitchExpr(
            branches=[
                SwitchBranch(case=EqExpr(left=F("status"), right="A"), then="Active"),
                SwitchBranch(case=EqExpr(left=F("status"), right="P"), then="Pending"),
                SwitchBranch(case=EqExpr(left=F("status"), right="D"), then="Deleted"),
            ],
            default="Unknown"
        ).model_dump()
    })
])

# Using comparison operators
grade = SwitchExpr(
    branches=[
        SwitchBranch(case=(F("score") >= 90), then="A"),
        SwitchBranch(case=(F("score") >= 80), then="B"),
        SwitchBranch(case=(F("score") >= 70), then="C"),
    ],
    default="F"
)
```

---

## String Expressions

Manipulate string values in documents.

### ConcatExpr - String Concatenation

```python
from mongo_aggro import F, ConcatExpr

# Combine first and last name
full_name = ConcatExpr(strings=[F("firstName"), " ", F("lastName")])

# Build formatted string
label = ConcatExpr(strings=["Order #", F("orderId"), " - ", F("status")])
```

### SplitExpr - Split String

```python
from mongo_aggro import F, SplitExpr

# Split email into parts
email_parts = SplitExpr(input=F("email"), delimiter="@")

# Split path
path_segments = SplitExpr(input=F("filePath"), delimiter="/")
```

### ToLowerExpr / ToUpperExpr - Case Conversion

```python
from mongo_aggro import F, ToLowerExpr, ToUpperExpr, Project, Pipeline

pipeline = Pipeline([
    Project(fields={
        "email_normalized": ToLowerExpr(input=F("email")).model_dump(),
        "code_upper": ToUpperExpr(input=F("countryCode")).model_dump(),
    })
])
```

---

## Array Expressions

Work with array fields in documents.

### ArraySizeExpr - Array Length

```python
from mongo_aggro import F, ArraySizeExpr

# Count items in array
item_count = ArraySizeExpr(array=F("items"))

# Use in conditions
has_items = (ArraySizeExpr(array=F("items")) > 0)
```

### SliceExpr - Array Subset

```python
from mongo_aggro import F, SliceExpr

# Get first 5 items
top_5 = SliceExpr(array=F("items"), n=5)

# Get items 3-5 (skip 2, take 3)
middle = SliceExpr(array=F("items"), position=2, n=3)

# Get last 3 items (negative n)
last_3 = SliceExpr(array=F("items"), n=-3)
```

### FilterExpr - Filter Array Elements

```python
from mongo_aggro import F, Field, FilterExpr, GteExpr, Project, Pipeline

# Filter items where price >= 100
pipeline = Pipeline([
    Project(fields={
        "expensive_items": FilterExpr(
            input=F("items"),
            as_="item",
            cond=GteExpr(left=Field("$$item.price"), right=100)
        ).model_dump()
    })
])

# Filter with multiple conditions
active_high_value = FilterExpr(
    input=F("orders"),
    as_="order",
    cond=(
        (Field("$$order.status") == "active")
        & (Field("$$order.total") > 1000)
    )
)
```

### MapExpr - Transform Array Elements

```python
from mongo_aggro import F, Field, MapExpr, MultiplyExpr, Project, Pipeline

# Apply 10% increase to all prices
pipeline = Pipeline([
    Project(fields={
        "increased_prices": MapExpr(
            input=F("prices"),
            as_="price",
            in_=MultiplyExpr(operands=[Field("$$price"), 1.1])
        ).model_dump()
    })
])

# Extract specific field from array of objects
names = MapExpr(
    input=F("users"),
    as_="user",
    in_=Field("$$user.name")
)
```

### ReduceExpr - Aggregate Array to Single Value

```python
from mongo_aggro import F, Field, ReduceExpr, AddExpr, Project, Pipeline

# Sum all quantities
pipeline = Pipeline([
    Project(fields={
        "total_qty": ReduceExpr(
            input=F("items"),
            initial_value=0,
            in_=AddExpr(operands=[Field("$$value"), Field("$$this.qty")])
        ).model_dump()
    })
])

# Concatenate strings with separator
joined = ReduceExpr(
    input=F("tags"),
    initial_value="",
    in_=CondExpr(
        if_=(Field("$$value") == ""),
        then=Field("$$this"),
        else_=ConcatExpr(strings=[Field("$$value"), ", ", Field("$$this")])
    )
)
```

---

## Real-World Examples

### E-commerce Order Processing

```python
from mongo_aggro import (
    F, Pipeline, Match, Project, Group,
    AddExpr, MultiplyExpr, CondExpr, FilterExpr, ReduceExpr,
    Field, Expr, Sum
)

# Calculate order totals with discounts
pipeline = Pipeline([
    # Filter active orders
    Match(query=Expr(expression=(
        (F("status") == "confirmed") & (F("items").model_dump() != [])
    )).model_dump()),

    # Calculate line totals and apply bulk discount
    Project(fields={
        "orderId": 1,
        "lineTotal": ReduceExpr(
            input=F("items"),
            initial_value=0,
            in_=AddExpr(operands=[
                Field("$$value"),
                MultiplyExpr(operands=[
                    Field("$$this.price"),
                    Field("$$this.qty")
                ])
            ])
        ).model_dump(),
        "itemCount": {"$size": "$items"},
    }),

    # Apply discount for large orders
    Project(fields={
        "orderId": 1,
        "lineTotal": 1,
        "discount": CondExpr(
            if_=(F("itemCount") > 10),
            then=MultiplyExpr(operands=[F("lineTotal"), 0.1]),
            else_=0
        ).model_dump(),
    }),
])
```

### User Analytics Dashboard

```python
from mongo_aggro import (
    F, Pipeline, Match, Project, AddFields,
    CondExpr, SwitchExpr, SwitchBranch, ArraySizeExpr,
    Expr
)

# Categorize users by activity
pipeline = Pipeline([
    AddFields(fields={
        "activityLevel": SwitchExpr(
            branches=[
                SwitchBranch(
                    case=(ArraySizeExpr(array=F("logins")) >= 100),
                    then="power_user"
                ),
                SwitchBranch(
                    case=(ArraySizeExpr(array=F("logins")) >= 20),
                    then="active"
                ),
                SwitchBranch(
                    case=(ArraySizeExpr(array=F("logins")) >= 1),
                    then="casual"
                ),
            ],
            default="inactive"
        ).model_dump(),
        "hasProfile": CondExpr(
            if_=(F("profile") != None),
            then=True,
            else_=False
        ).model_dump(),
    })
])
```

---

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

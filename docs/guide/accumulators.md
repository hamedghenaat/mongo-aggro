# Accumulators

Accumulators are used within the `$group` stage to compute values across
grouped documents. Mongo Aggro provides typed accumulator classes with
IDE autocomplete and validation.

## Using Accumulators

### With `merge_accumulators()` (Recommended)

Use typed accumulator classes for better IDE support and validation:

```python
from mongo_aggro import Group, Sum, Avg, Max, Min, merge_accumulators

Group(
    id="$category",
    accumulators=merge_accumulators(
        Sum(name="totalSales", field="amount"),
        Avg(name="avgSale", field="amount"),
        Max(name="maxSale", field="amount"),
        Min(name="minSale", field="amount"),
    )
)
```

### Raw Dictionary

For simple cases, raw dicts work too:

```python
Group(
    id="$category",
    accumulators={
        "totalSales": {"$sum": "$amount"},
        "avgSale": {"$avg": "$amount"},
    }
)
```

## Basic Accumulators

### Sum

Sums values or counts documents.

```python
from mongo_aggro import Sum

# Sum a field
Sum(name="total", field="amount")
# {"total": {"$sum": "$amount"}}

# Count documents
Sum(name="count", value=1)
# {"count": {"$sum": 1}}
```

### Avg

Calculates the average of values.

```python
from mongo_aggro import Avg

Avg(name="average", field="price")
# {"average": {"$avg": "$price"}}
```

### Min / Max

Gets minimum or maximum values.

```python
from mongo_aggro import Min, Max

Min(name="lowestPrice", field="price")
# {"lowestPrice": {"$min": "$price"}}

Max(name="highestPrice", field="price")
# {"highestPrice": {"$max": "$price"}}
```

### First / Last

Gets the first or last value in each group.

```python
from mongo_aggro import First, Last

First(name="firstOrder", field="orderId")
# {"firstOrder": {"$first": "$orderId"}}

Last(name="lastOrder", field="orderId")
# {"lastOrder": {"$last": "$orderId"}}
```

## Array Accumulators

### Push

Adds values to an array.

```python
from mongo_aggro import Push

# Push field values
Push(name="items", field="itemName")
# {"items": {"$push": "$itemName"}}

# Push expressions
Push(name="orderDetails", expression={"id": "$orderId", "amount": "$total"})
# {"orderDetails": {"$push": {"id": "$orderId", "amount": "$total"}}}
```

### AddToSet

Adds unique values to an array.

```python
from mongo_aggro import AddToSet

AddToSet(name="uniqueTags", field="tag")
# {"uniqueTags": {"$addToSet": "$tag"}}
```

## Statistical Accumulators

### StdDevPop / StdDevSamp

Calculates standard deviation.

```python
from mongo_aggro import StdDevPop, StdDevSamp

# Population standard deviation
StdDevPop(name="stdDev", field="score")
# {"stdDev": {"$stdDevPop": "$score"}}

# Sample standard deviation
StdDevSamp(name="sampleStdDev", field="score")
# {"sampleStdDev": {"$stdDevSamp": "$score"}}
```

## Count Accumulator

### Count_

Counts documents in each group.

```python
from mongo_aggro import Count_

Count_(name="documentCount")
# {"documentCount": {"$count": {}}}
```

!!! note
    The class is named `Count_` (with underscore) to avoid conflict with the `Count` stage.

## Object Accumulators

### MergeObjects

Merges documents into a single document.

```python
from mongo_aggro import MergeObjects

MergeObjects(name="combined", field="metadata")
# {"combined": {"$mergeObjects": "$metadata"}}
```

## N-Value Accumulators

### TopN / BottomN

Gets top or bottom N values based on sort order.

```python
from mongo_aggro import TopN, BottomN

TopN(
    name="top3Products",
    n=3,
    sort_by={"sales": -1},
    output="$productName"
)
# {"top3Products": {"$topN": {"n": 3, "sortBy": {"sales": -1}, "output": "$productName"}}}

BottomN(
    name="bottom3Products",
    n=3,
    sort_by={"sales": -1},
    output="$productName"
)
```

### FirstN / LastN

Gets first or last N values.

```python
from mongo_aggro import FirstN, LastN

FirstN(name="first5", n=5, input="$item")
# {"first5": {"$firstN": {"n": 5, "input": "$item"}}}

LastN(name="last5", n=5, input="$item")
# {"last5": {"$lastN": {"n": 5, "input": "$item"}}}
```

### MaxN / MinN

Gets N maximum or minimum values.

```python
from mongo_aggro import MaxN, MinN

MaxN(name="top3Scores", n=3, input="$score")
# {"top3Scores": {"$maxN": {"n": 3, "input": "$score"}}}

MinN(name="lowest3Scores", n=3, input="$score")
# {"lowest3Scores": {"$minN": {"n": 3, "input": "$score"}}}
```

## Complete Example

```python
from mongo_aggro import (
    Pipeline, Match, Group, Sort, Limit,
    Sum, Avg, Max, Min, First, Last, Push, Count_,
    merge_accumulators
)

pipeline = Pipeline([
    Match(query={"status": "completed", "year": 2024}),
    Group(
        id="$category",
        accumulators=merge_accumulators(
            Sum(name="totalRevenue", field="amount"),
            Avg(name="avgOrderValue", field="amount"),
            Max(name="largestOrder", field="amount"),
            Min(name="smallestOrder", field="amount"),
            First(name="firstOrderDate", field="orderDate"),
            Last(name="lastOrderDate", field="orderDate"),
            Push(name="allOrderIds", field="orderId"),
            Count_(name="orderCount"),
        )
    ),
    Sort(fields={"totalRevenue": -1}),
    Limit(count=10),
])
```

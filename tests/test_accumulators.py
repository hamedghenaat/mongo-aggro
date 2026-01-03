"""Tests for accumulator classes."""

from mongo_aggro import (
    AddToSet,
    Avg,
    BottomN,
    Count_,
    First,
    FirstN,
    Last,
    LastN,
    Max,
    MaxN,
    MergeObjects,
    Min,
    MinN,
    Push,
    StdDevPop,
    StdDevSamp,
    Sum,
    TopN,
    merge_accumulators,
)

# --- Sum Tests ---


def test_sum_field() -> None:
    """Sum with field path."""
    acc = Sum(name="totalQuantity", field="quantity")
    assert acc.model_dump() == {"totalQuantity": {"$sum": "$quantity"}}


def test_sum_field_with_dollar() -> None:
    """Sum field already has $."""
    acc = Sum(name="total", field="$amount")
    assert acc.model_dump() == {"total": {"$sum": "$amount"}}


def test_sum_value() -> None:
    """Sum with literal value for counting."""
    acc = Sum(name="count", value=1)
    assert acc.model_dump() == {"count": {"$sum": 1}}


def test_sum_value_float() -> None:
    """Sum with float value."""
    acc = Sum(name="weighted", value=0.5)
    assert acc.model_dump() == {"weighted": {"$sum": 0.5}}


# --- Avg Tests ---


def test_avg() -> None:
    """Avg accumulator."""
    acc = Avg(name="avgPrice", field="price")
    assert acc.model_dump() == {"avgPrice": {"$avg": "$price"}}


def test_avg_with_dollar() -> None:
    """Avg field already has $."""
    acc = Avg(name="average", field="$score")
    assert acc.model_dump() == {"average": {"$avg": "$score"}}


# --- Min/Max Tests ---


def test_min() -> None:
    """Min accumulator."""
    acc = Min(name="minPrice", field="price")
    assert acc.model_dump() == {"minPrice": {"$min": "$price"}}


def test_max() -> None:
    """Max accumulator."""
    acc = Max(name="maxPrice", field="price")
    assert acc.model_dump() == {"maxPrice": {"$max": "$price"}}


# --- First/Last Tests ---


def test_first() -> None:
    """First accumulator."""
    acc = First(name="firstItem", field="item")
    assert acc.model_dump() == {"firstItem": {"$first": "$item"}}


def test_last() -> None:
    """Last accumulator."""
    acc = Last(name="lastItem", field="item")
    assert acc.model_dump() == {"lastItem": {"$last": "$item"}}


# --- Push Tests ---


def test_push_field() -> None:
    """Push with field path."""
    acc = Push(name="items", field="item")
    assert acc.model_dump() == {"items": {"$push": "$item"}}


def test_push_expression() -> None:
    """Push with expression."""
    acc = Push(
        name="orderDetails",
        expression={"name": "$name", "qty": "$quantity"},
    )
    assert acc.model_dump() == {
        "orderDetails": {"$push": {"name": "$name", "qty": "$quantity"}}
    }


# --- AddToSet Tests ---


def test_add_to_set() -> None:
    """AddToSet accumulator."""
    acc = AddToSet(name="uniqueTags", field="tag")
    assert acc.model_dump() == {"uniqueTags": {"$addToSet": "$tag"}}


# --- StdDev Tests ---


def test_std_dev_pop() -> None:
    """StdDevPop accumulator."""
    acc = StdDevPop(name="stdDev", field="score")
    assert acc.model_dump() == {"stdDev": {"$stdDevPop": "$score"}}


def test_std_dev_samp() -> None:
    """StdDevSamp accumulator."""
    acc = StdDevSamp(name="stdDevSample", field="score")
    assert acc.model_dump() == {"stdDevSample": {"$stdDevSamp": "$score"}}


# --- Count_ Tests ---


def test_count_accumulator() -> None:
    """Count_ accumulator."""
    acc = Count_(name="totalDocs")
    assert acc.model_dump() == {"totalDocs": {"$count": {}}}


# --- MergeObjects Tests ---


def test_merge_objects() -> None:
    """MergeObjects accumulator."""
    acc = MergeObjects(name="merged", field="details")
    assert acc.model_dump() == {"merged": {"$mergeObjects": "$details"}}


# --- TopN/BottomN Tests ---


def test_top_n() -> None:
    """TopN accumulator."""
    acc = TopN(
        name="top3",
        n=3,
        sort_by={"score": -1},
        output="$item",
    )
    assert acc.model_dump() == {
        "top3": {
            "$topN": {
                "n": 3,
                "sortBy": {"score": -1},
                "output": "$item",
            }
        }
    }


def test_bottom_n() -> None:
    """BottomN accumulator."""
    acc = BottomN(
        name="bottom3",
        n=3,
        sort_by={"score": -1},
        output="$item",
    )
    assert acc.model_dump() == {
        "bottom3": {
            "$bottomN": {
                "n": 3,
                "sortBy": {"score": -1},
                "output": "$item",
            }
        }
    }


# --- FirstN/LastN Tests ---


def test_first_n() -> None:
    """FirstN accumulator."""
    acc = FirstN(name="first3", n=3, input="$item")
    assert acc.model_dump() == {
        "first3": {"$firstN": {"n": 3, "input": "$item"}}
    }


def test_last_n() -> None:
    """LastN accumulator."""
    acc = LastN(name="last3", n=3, input="$item")
    assert acc.model_dump() == {
        "last3": {"$lastN": {"n": 3, "input": "$item"}}
    }


# --- MaxN/MinN Tests ---


def test_max_n() -> None:
    """MaxN accumulator."""
    acc = MaxN(name="top3Scores", n=3, input="$score")
    assert acc.model_dump() == {
        "top3Scores": {"$maxN": {"n": 3, "input": "$score"}}
    }


def test_min_n() -> None:
    """MinN accumulator."""
    acc = MinN(name="lowest3", n=3, input="$score")
    assert acc.model_dump() == {
        "lowest3": {"$minN": {"n": 3, "input": "$score"}}
    }


# --- merge_accumulators Tests ---


def test_merge_single() -> None:
    """Merge single accumulator."""
    result = merge_accumulators(Sum(name="total", field="amount"))
    assert result == {"total": {"$sum": "$amount"}}


def test_merge_multiple() -> None:
    """Merge multiple accumulators."""
    result = merge_accumulators(
        Sum(name="total", field="amount"),
        Avg(name="average", field="amount"),
        Count_(name="count"),
    )
    assert result == {
        "total": {"$sum": "$amount"},
        "average": {"$avg": "$amount"},
        "count": {"$count": {}},
    }


def test_merge_empty() -> None:
    """Merge no accumulators."""
    result = merge_accumulators()
    assert result == {}


def test_merge_preserves_order() -> None:
    """Merge preserves key insertion order."""
    result = merge_accumulators(
        Sum(name="a", value=1),
        Sum(name="b", value=2),
        Sum(name="c", value=3),
    )
    assert list(result.keys()) == ["a", "b", "c"]

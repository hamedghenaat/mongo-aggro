"""Tests for array expression operators.

This module tests:
- ArraySizeExpr, SliceExpr
- FilterExpr, MapExpr, ReduceExpr
- ArrayElemAtExpr, ConcatArraysExpr, InArrayExpr
- IndexOfArrayExpr, IsArrayExpr, ReverseArrayExpr
- SortArrayExpr, RangeExpr
- FirstNExpr, LastNExpr, MaxNExpr, MinNExpr
"""

import pytest
from pydantic import ValidationError

from mongo_aggro.expressions import (
    AddExpr,
    ArrayElemAtExpr,
    ArraySizeExpr,
    ConcatArraysExpr,
    F,
    Field,
    FilterExpr,
    FirstNExpr,
    GteExpr,
    GtExpr,
    InArrayExpr,
    IndexOfArrayExpr,
    IsArrayExpr,
    LastNExpr,
    MapExpr,
    MaxNExpr,
    MinNExpr,
    MultiplyExpr,
    RangeExpr,
    ReduceExpr,
    ReverseArrayExpr,
    SliceExpr,
    SortArrayExpr,
)

# --- ArraySizeExpr Tests ---


def test_array_size_expr() -> None:
    """ArraySizeExpr serialization."""
    expr = ArraySizeExpr(array=F("items"))
    assert expr.model_dump() == {"$size": "$items"}


def test_array_size_missing_array_raises() -> None:
    """ArraySizeExpr requires array."""
    with pytest.raises(ValidationError):
        ArraySizeExpr()  # type: ignore[call-arg]


# --- SliceExpr Tests ---


def test_slice_expr_n_only() -> None:
    """SliceExpr with n only."""
    expr = SliceExpr(array=F("items"), n=5)
    assert expr.model_dump() == {"$slice": ["$items", 5]}


def test_slice_expr_with_position() -> None:
    """SliceExpr with position and n."""
    expr = SliceExpr(array=F("items"), position=2, n=3)
    assert expr.model_dump() == {"$slice": ["$items", 2, 3]}


def test_slice_expr_missing_n_raises() -> None:
    """SliceExpr requires n."""
    with pytest.raises(ValidationError):
        SliceExpr(array=F("items"))  # type: ignore[call-arg]


# --- FilterExpr Tests ---


def test_filter_expr() -> None:
    """FilterExpr serialization."""
    expr = FilterExpr(
        input=F("items"),
        as_="item",
        cond=GteExpr(left=Field("$$item.price"), right=100),
    )
    result = expr.model_dump()
    assert result["$filter"]["input"] == "$items"
    assert result["$filter"]["as"] == "item"
    assert result["$filter"]["cond"] == {"$gte": ["$$item.price", 100]}


def test_filter_expr_with_limit() -> None:
    """FilterExpr with limit."""
    expr = FilterExpr(
        input=F("items"),
        cond=GtExpr(left=Field("$$this.qty"), right=0),
        limit=5,
    )
    result = expr.model_dump()
    assert result["$filter"]["limit"] == 5


def test_filter_expr_missing_cond_raises() -> None:
    """FilterExpr requires cond."""
    with pytest.raises(ValidationError):
        FilterExpr(input=F("items"))  # type: ignore[call-arg]


# --- MapExpr Tests ---


def test_map_expr() -> None:
    """MapExpr serialization."""
    expr = MapExpr(
        input=F("prices"),
        as_="price",
        in_=MultiplyExpr(operands=[Field("$$price"), 1.1]),
    )
    result = expr.model_dump()
    assert result["$map"]["input"] == "$prices"
    assert result["$map"]["as"] == "price"
    assert result["$map"]["in"] == {"$multiply": ["$$price", 1.1]}


def test_map_expr_missing_in_raises() -> None:
    """MapExpr requires in_."""
    with pytest.raises(ValidationError):
        MapExpr(input=F("items"))  # type: ignore[call-arg]


# --- ReduceExpr Tests ---


def test_reduce_expr() -> None:
    """ReduceExpr serialization."""
    expr = ReduceExpr(
        input=F("items"),
        initial_value=0,
        in_=AddExpr(operands=[Field("$$value"), Field("$$this.qty")]),
    )
    result = expr.model_dump()
    assert result["$reduce"]["input"] == "$items"
    assert result["$reduce"]["initialValue"] == 0
    assert result["$reduce"]["in"] == {"$add": ["$$value", "$$this.qty"]}


def test_reduce_expr_missing_initial_raises() -> None:
    """ReduceExpr requires initial_value."""
    with pytest.raises(ValidationError):
        ReduceExpr(
            input=F("items"),
            in_=F("$$this"),
        )  # type: ignore[call-arg]


# --- ArrayElemAtExpr Tests ---


def test_array_elem_at_expr() -> None:
    """ArrayElemAtExpr serialization."""
    expr = ArrayElemAtExpr(array=F("items"), index=0)
    assert expr.model_dump() == {"$arrayElemAt": ["$items", 0]}


# --- ConcatArraysExpr Tests ---


def test_concat_arrays_expr() -> None:
    """ConcatArraysExpr serialization."""
    expr = ConcatArraysExpr(arrays=[F("arr1"), F("arr2")])
    assert expr.model_dump() == {"$concatArrays": ["$arr1", "$arr2"]}


def test_concat_arrays_missing_arrays_raises() -> None:
    """ConcatArraysExpr requires arrays."""
    with pytest.raises(ValidationError):
        ConcatArraysExpr()  # type: ignore[call-arg]


# --- InArrayExpr Tests ---


def test_in_array_expr() -> None:
    """InArrayExpr serialization."""
    expr = InArrayExpr(value="admin", array=F("roles"))
    assert expr.model_dump() == {"$in": ["admin", "$roles"]}


# --- IndexOfArrayExpr Tests ---


def test_index_of_array_expr() -> None:
    """IndexOfArrayExpr serialization."""
    expr = IndexOfArrayExpr(array=F("items"), value="target")
    assert expr.model_dump() == {"$indexOfArray": ["$items", "target"]}


def test_index_of_array_expr_with_range() -> None:
    """IndexOfArrayExpr with start and end."""
    expr = IndexOfArrayExpr(array=F("items"), value="x", start=2, end=10)
    assert expr.model_dump() == {"$indexOfArray": ["$items", "x", 2, 10]}


# --- IsArrayExpr Tests ---


def test_is_array_expr() -> None:
    """IsArrayExpr serialization."""
    expr = IsArrayExpr(input=F("field"))
    assert expr.model_dump() == {"$isArray": "$field"}


# --- ReverseArrayExpr Tests ---


def test_reverse_array_expr() -> None:
    """ReverseArrayExpr serialization."""
    expr = ReverseArrayExpr(input=F("items"))
    assert expr.model_dump() == {"$reverseArray": "$items"}


# --- SortArrayExpr Tests ---


def test_sort_array_expr() -> None:
    """SortArrayExpr serialization."""
    expr = SortArrayExpr(input=F("scores"), sort_by={"score": -1})
    assert expr.model_dump() == {
        "$sortArray": {"input": "$scores", "sortBy": {"score": -1}}
    }


def test_sort_array_missing_sort_by_raises() -> None:
    """SortArrayExpr requires sort_by."""
    with pytest.raises(ValidationError):
        SortArrayExpr(input=F("items"))  # type: ignore[call-arg]


# --- RangeExpr Tests ---


def test_range_expr() -> None:
    """RangeExpr serialization."""
    expr = RangeExpr(start=0, end=10, step=2)
    assert expr.model_dump() == {"$range": [0, 10, 2]}


def test_range_expr_default_step() -> None:
    """RangeExpr with default step."""
    expr = RangeExpr(start=0, end=5)
    assert expr.model_dump() == {"$range": [0, 5, 1]}


def test_range_missing_end_raises() -> None:
    """RangeExpr requires end."""
    with pytest.raises(ValidationError):
        RangeExpr(start=0)  # type: ignore[call-arg]


# --- FirstNExpr Tests ---


def test_first_n_expr() -> None:
    """FirstNExpr serialization."""
    expr = FirstNExpr(input=F("items"), n=3)
    assert expr.model_dump() == {"$firstN": {"input": "$items", "n": 3}}


# --- LastNExpr Tests ---


def test_last_n_expr() -> None:
    """LastNExpr serialization."""
    expr = LastNExpr(input=F("items"), n=3)
    assert expr.model_dump() == {"$lastN": {"input": "$items", "n": 3}}


# --- MaxNExpr Tests ---


def test_max_n_expr() -> None:
    """MaxNExpr serialization."""
    expr = MaxNExpr(input=F("scores"), n=3)
    assert expr.model_dump() == {"$maxN": {"input": "$scores", "n": 3}}


# --- MinNExpr Tests ---


def test_min_n_expr() -> None:
    """MinNExpr serialization."""
    expr = MinNExpr(input=F("scores"), n=3)
    assert expr.model_dump() == {"$minN": {"input": "$scores", "n": 3}}


def test_first_n_missing_n_raises() -> None:
    """FirstNExpr requires n."""
    with pytest.raises(ValidationError):
        FirstNExpr(input=F("items"))  # type: ignore[call-arg]

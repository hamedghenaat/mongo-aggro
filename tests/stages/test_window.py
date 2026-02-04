"""Tests for window function aggregation stages."""

import pytest
from pydantic import ValidationError

from mongo_aggro.stages import Densify, Fill, SetWindowFields

# --- SetWindowFields Tests ---


def test_set_window_fields() -> None:
    """SetWindowFields stage."""
    swf = SetWindowFields(
        partition_by="$state",
        sort_by={"date": 1},
        output={
            "cumulative": {
                "$sum": "$quantity",
                "window": {"documents": ["unbounded", "current"]},
            }
        },
    )
    result = swf.model_dump()
    assert result["$setWindowFields"]["partitionBy"] == "$state"
    assert result["$setWindowFields"]["sortBy"] == {"date": 1}
    assert "cumulative" in result["$setWindowFields"]["output"]


def test_set_window_fields_minimal() -> None:
    """SetWindowFields with only output."""
    swf = SetWindowFields(output={"rank": {"$rank": {}}})
    result = swf.model_dump()
    assert result == {"$setWindowFields": {"output": {"rank": {"$rank": {}}}}}


def test_set_window_fields_partition_dict() -> None:
    """SetWindowFields with compound partition."""
    swf = SetWindowFields(
        partition_by={"region": "$region", "year": "$year"},
        output={"total": {"$sum": "$amount"}},
    )
    result = swf.model_dump()
    assert result["$setWindowFields"]["partitionBy"] == {
        "region": "$region",
        "year": "$year",
    }


def test_set_window_fields_missing_output() -> None:
    """SetWindowFields requires output parameter."""
    with pytest.raises(ValidationError):
        SetWindowFields()  # type: ignore[call-arg]


# --- Densify Tests ---


def test_densify() -> None:
    """Densify stage."""
    densify = Densify(
        field="date",
        range={"step": 1, "unit": "day", "bounds": "full"},
    )
    result = densify.model_dump()
    assert result == {
        "$densify": {
            "field": "date",
            "range": {"step": 1, "unit": "day", "bounds": "full"},
        }
    }


def test_densify_with_partition() -> None:
    """Densify with partition fields."""
    densify = Densify(
        field="timestamp",
        range={"step": 1, "unit": "hour", "bounds": "full"},
        partition_by_fields=["device", "location"],
    )
    result = densify.model_dump()
    assert result["$densify"]["partitionByFields"] == ["device", "location"]


def test_densify_numeric_range() -> None:
    """Densify with numeric range."""
    densify = Densify(
        field="sequence",
        range={"step": 10, "bounds": [0, 100]},
    )
    result = densify.model_dump()
    assert result["$densify"]["range"]["step"] == 10
    assert result["$densify"]["range"]["bounds"] == [0, 100]


def test_densify_missing_field() -> None:
    """Densify requires field parameter."""
    with pytest.raises(ValidationError):
        Densify(range={"step": 1})  # type: ignore[call-arg]


def test_densify_missing_range() -> None:
    """Densify requires range parameter."""
    with pytest.raises(ValidationError):
        Densify(field="date")  # type: ignore[call-arg]


# --- Fill Tests ---


def test_fill() -> None:
    """Fill stage."""
    fill = Fill(
        sort_by={"date": 1},
        output={
            "score": {"method": "linear"},
            "status": {"value": "unknown"},
        },
    )
    result = fill.model_dump()
    assert result["$fill"]["sortBy"] == {"date": 1}
    assert "score" in result["$fill"]["output"]


def test_fill_with_partition_by() -> None:
    """Fill with partitionBy."""
    fill = Fill(
        partition_by="$category",
        output={"value": {"method": "locf"}},
    )
    result = fill.model_dump()
    assert result["$fill"]["partitionBy"] == "$category"


def test_fill_with_partition_by_fields() -> None:
    """Fill with partitionByFields."""
    fill = Fill(
        partition_by_fields=["region", "product"],
        output={"price": {"value": 0}},
    )
    result = fill.model_dump()
    assert result["$fill"]["partitionByFields"] == ["region", "product"]


def test_fill_minimal() -> None:
    """Fill with only output."""
    fill = Fill(output={"missing": {"value": None}})
    result = fill.model_dump()
    assert result == {"$fill": {"output": {"missing": {"value": None}}}}


def test_fill_missing_output() -> None:
    """Fill requires output parameter."""
    with pytest.raises(ValidationError):
        Fill()  # type: ignore[call-arg]

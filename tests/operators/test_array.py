"""Tests for array query operators."""

import pytest
from pydantic import ValidationError

from mongo_aggro.operators.array import All, ElemMatch, Size

# --- ElemMatch Operator Tests ---


def test_elem_match() -> None:
    """$elemMatch operator with valid conditions."""
    op = ElemMatch(
        conditions={
            "quantity": {"$gt": 5},
            "price": {"$lt": 100},
        }
    )
    assert op.model_dump() == {
        "$elemMatch": {
            "quantity": {"$gt": 5},
            "price": {"$lt": 100},
        }
    }


def test_elem_match_missing_conditions() -> None:
    """$elemMatch requires conditions parameter."""
    with pytest.raises(ValidationError):
        ElemMatch()  # type: ignore[call-arg]


def test_elem_match_invalid_type() -> None:
    """$elemMatch conditions must be a dict."""
    with pytest.raises(ValidationError):
        ElemMatch(conditions="not a dict")  # type: ignore[arg-type]


# --- Size Operator Tests ---


def test_size() -> None:
    """$size operator with valid size."""
    op = Size(size=5)
    assert op.model_dump() == {"$size": 5}


def test_size_zero() -> None:
    """$size operator with zero."""
    op = Size(size=0)
    assert op.model_dump() == {"$size": 0}


def test_size_missing_value() -> None:
    """$size requires size parameter."""
    with pytest.raises(ValidationError):
        Size()  # type: ignore[call-arg]


def test_size_invalid_type() -> None:
    """$size must be an integer."""
    with pytest.raises(ValidationError):
        Size(size="not an int")  # type: ignore[arg-type]


# --- All Operator Tests ---


def test_all() -> None:
    """$all operator with valid values."""
    op = All(values=["red", "green", "blue"])
    assert op.model_dump() == {"$all": ["red", "green", "blue"]}


def test_all_empty() -> None:
    """$all operator with empty list."""
    op = All(values=[])
    assert op.model_dump() == {"$all": []}


def test_all_missing_values() -> None:
    """$all requires values parameter."""
    with pytest.raises(ValidationError):
        All()  # type: ignore[call-arg]


def test_all_invalid_type() -> None:
    """$all values must be a list."""
    with pytest.raises(ValidationError):
        All(values="not a list")  # type: ignore[arg-type]

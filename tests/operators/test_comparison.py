"""Tests for comparison query operators."""

import pytest
from pydantic import ValidationError

from mongo_aggro.operators.comparison import Eq, Gt, Gte, In, Lt, Lte, Ne, Nin

# --- Eq Operator Tests ---


def test_eq() -> None:
    """$eq operator with numeric value."""
    op = Eq(value=5)
    assert op.model_dump() == {"$eq": 5}


def test_eq_string() -> None:
    """$eq with string value."""
    op = Eq(value="active")
    assert op.model_dump() == {"$eq": "active"}


def test_eq_missing_value() -> None:
    """$eq requires value parameter."""
    with pytest.raises(ValidationError):
        Eq()  # type: ignore[call-arg]


# --- Ne Operator Tests ---


def test_ne() -> None:
    """$ne operator."""
    op = Ne(value="deleted")
    assert op.model_dump() == {"$ne": "deleted"}


def test_ne_missing_value() -> None:
    """$ne requires value parameter."""
    with pytest.raises(ValidationError):
        Ne()  # type: ignore[call-arg]


# --- Gt Operator Tests ---


def test_gt() -> None:
    """$gt operator."""
    op = Gt(value=10)
    assert op.model_dump() == {"$gt": 10}


def test_gt_missing_value() -> None:
    """$gt requires value parameter."""
    with pytest.raises(ValidationError):
        Gt()  # type: ignore[call-arg]


# --- Gte Operator Tests ---


def test_gte() -> None:
    """$gte operator."""
    op = Gte(value=18)
    assert op.model_dump() == {"$gte": 18}


def test_gte_missing_value() -> None:
    """$gte requires value parameter."""
    with pytest.raises(ValidationError):
        Gte()  # type: ignore[call-arg]


# --- Lt Operator Tests ---


def test_lt() -> None:
    """$lt operator."""
    op = Lt(value=100)
    assert op.model_dump() == {"$lt": 100}


def test_lt_missing_value() -> None:
    """$lt requires value parameter."""
    with pytest.raises(ValidationError):
        Lt()  # type: ignore[call-arg]


# --- Lte Operator Tests ---


def test_lte() -> None:
    """$lte operator."""
    op = Lte(value=65)
    assert op.model_dump() == {"$lte": 65}


def test_lte_missing_value() -> None:
    """$lte requires value parameter."""
    with pytest.raises(ValidationError):
        Lte()  # type: ignore[call-arg]


# --- In Operator Tests ---


def test_in() -> None:
    """$in operator with numeric values."""
    op = In(values=[1, 2, 3])
    assert op.model_dump() == {"$in": [1, 2, 3]}


def test_in_strings() -> None:
    """$in with string values."""
    op = In(values=["active", "pending", "review"])
    assert op.model_dump() == {"$in": ["active", "pending", "review"]}


def test_in_missing_values() -> None:
    """$in requires values parameter."""
    with pytest.raises(ValidationError):
        In()  # type: ignore[call-arg]


def test_in_invalid_type() -> None:
    """$in values must be a list."""
    with pytest.raises(ValidationError):
        In(values="not a list")  # type: ignore[arg-type]


# --- Nin Operator Tests ---


def test_nin() -> None:
    """$nin operator."""
    op = Nin(values=["deleted", "archived"])
    assert op.model_dump() == {"$nin": ["deleted", "archived"]}


def test_nin_missing_values() -> None:
    """$nin requires values parameter."""
    with pytest.raises(ValidationError):
        Nin()  # type: ignore[call-arg]

"""Tests for logical query operators."""

import pytest
from pydantic import ValidationError

from mongo_aggro.operators.logical import And, Expr, Nor, Not, Or

# --- And Operator Tests ---


def test_and() -> None:
    """$and operator with valid conditions."""
    op = And(
        conditions=[
            {"status": "active"},
            {"age": {"$gt": 18}},
        ]
    )
    assert op.model_dump() == {
        "$and": [
            {"status": "active"},
            {"age": {"$gt": 18}},
        ]
    }


def test_and_empty() -> None:
    """$and with empty conditions."""
    op = And(conditions=[])
    assert op.model_dump() == {"$and": []}


def test_and_missing_conditions() -> None:
    """$and requires conditions parameter."""
    with pytest.raises(ValidationError):
        And()  # type: ignore[call-arg]


def test_and_invalid_conditions_type() -> None:
    """$and conditions must be a list."""
    with pytest.raises(ValidationError):
        And(conditions="not a list")  # type: ignore[arg-type]


# --- Or Operator Tests ---


def test_or() -> None:
    """$or operator with valid conditions."""
    op = Or(
        conditions=[
            {"status": "active"},
            {"status": "pending"},
        ]
    )
    assert op.model_dump() == {
        "$or": [
            {"status": "active"},
            {"status": "pending"},
        ]
    }


def test_or_missing_conditions() -> None:
    """$or requires conditions parameter."""
    with pytest.raises(ValidationError):
        Or()  # type: ignore[call-arg]


# --- Not Operator Tests ---


def test_not() -> None:
    """$not operator with valid condition."""
    op = Not(condition={"$regex": "^test"})
    assert op.model_dump() == {"$not": {"$regex": "^test"}}


def test_not_missing_condition() -> None:
    """$not requires condition parameter."""
    with pytest.raises(ValidationError):
        Not()  # type: ignore[call-arg]


def test_not_invalid_condition_type() -> None:
    """$not condition must be a dict."""
    with pytest.raises(ValidationError):
        Not(condition="not a dict")  # type: ignore[arg-type]


# --- Nor Operator Tests ---


def test_nor() -> None:
    """$nor operator with valid conditions."""
    op = Nor(
        conditions=[
            {"price": {"$gt": 1000}},
            {"rating": {"$lt": 3}},
        ]
    )
    assert op.model_dump() == {
        "$nor": [
            {"price": {"$gt": 1000}},
            {"rating": {"$lt": 3}},
        ]
    }


def test_nor_missing_conditions() -> None:
    """$nor requires conditions parameter."""
    with pytest.raises(ValidationError):
        Nor()  # type: ignore[call-arg]


# --- Expr Operator Tests ---


def test_expr() -> None:
    """$expr operator with valid expression."""
    op = Expr(expression={"$eq": ["$field1", "$field2"]})
    assert op.model_dump() == {"$expr": {"$eq": ["$field1", "$field2"]}}


def test_expr_complex() -> None:
    """$expr with complex expression."""
    op = Expr(
        expression={
            "$and": [
                {"$eq": ["$status", "active"]},
                {"$gt": ["$balance", 100]},
            ]
        }
    )
    result = op.model_dump()
    assert "$expr" in result
    assert "$and" in result["$expr"]


def test_expr_missing_expression() -> None:
    """$expr requires expression parameter."""
    with pytest.raises(ValidationError):
        Expr()  # type: ignore[call-arg]

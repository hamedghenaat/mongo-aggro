"""Tests for logical expression operators.

This module tests:
- AndExpr, OrExpr, NotExpr
- Operator overloading (&, |, ~)
- Expression flattening for chained AND/OR
- Deeply nested expressions
"""

import pytest
from pydantic import ValidationError

from mongo_aggro.expressions import (
    AndExpr,
    EqExpr,
    F,
    GtExpr,
    LtExpr,
    NotExpr,
    OrExpr,
)

# --- AndExpr Tests ---


def test_and_expr_serialization() -> None:
    """AndExpr serializes with nested expressions."""
    nested_and_expr = AndExpr(
        conditions=[
            EqExpr(left=F("status"), right="active"),
            GtExpr(left=F("age"), right=18),
        ]
    )
    assert nested_and_expr.model_dump() == {
        "$and": [{"$eq": ["$status", "active"]}, {"$gt": ["$age", 18]}]
    }


def test_and_expr_multiple_conditions() -> None:
    """AndExpr with multiple conditions."""
    expr = AndExpr(
        conditions=[
            EqExpr(left=F("a"), right=1),
            EqExpr(left=F("b"), right=2),
            EqExpr(left=F("c"), right=3),
        ]
    )
    result = expr.model_dump()
    assert len(result["$and"]) == 3


def test_and_expr_missing_conditions_raises() -> None:
    """AndExpr requires conditions list."""
    with pytest.raises(ValidationError):
        AndExpr()  # type: ignore[call-arg]


def test_and_expr_empty_conditions_allowed() -> None:
    """AndExpr with empty conditions serializes (MongoDB handles)."""
    expr = AndExpr(conditions=[])
    assert expr.model_dump() == {"$and": []}


# --- OrExpr Tests ---


def test_or_expr_serialization() -> None:
    """OrExpr serializes correctly."""
    expr = OrExpr(
        conditions=[
            EqExpr(left=F("a"), right=1),
            EqExpr(left=F("a"), right=2),
        ]
    )
    assert expr.model_dump() == {
        "$or": [{"$eq": ["$a", 1]}, {"$eq": ["$a", 2]}]
    }


def test_or_expr_missing_conditions_raises() -> None:
    """OrExpr requires conditions list."""
    with pytest.raises(ValidationError):
        OrExpr()  # type: ignore[call-arg]


# --- NotExpr Tests ---


def test_not_expr_serialization() -> None:
    """NotExpr serializes correctly."""
    expr = NotExpr(condition=EqExpr(left=F("status"), right="deleted"))
    assert expr.model_dump() == {"$not": {"$eq": ["$status", "deleted"]}}


def test_not_expr_missing_condition_raises() -> None:
    """NotExpr requires condition."""
    with pytest.raises(ValidationError):
        NotExpr()  # type: ignore[call-arg]


# --- Logical Operators Tests ---


def test_and_via_operator() -> None:
    """& operator creates AndExpr."""
    expr = (F("a") == 1) & (F("b") == 2)
    assert isinstance(expr, AndExpr)
    assert expr.model_dump() == {
        "$and": [{"$eq": ["$a", 1]}, {"$eq": ["$b", 2]}]
    }


def test_or_via_operator() -> None:
    """| operator creates OrExpr."""
    expr = (F("a") == 1) | (F("b") == 2)
    assert isinstance(expr, OrExpr)
    assert expr.model_dump() == {
        "$or": [{"$eq": ["$a", 1]}, {"$eq": ["$b", 2]}]
    }


def test_not_via_operator() -> None:
    """~ operator creates NotExpr."""
    expr = ~(F("status") == "deleted")
    assert isinstance(expr, NotExpr)
    assert expr.model_dump() == {"$not": {"$eq": ["$status", "deleted"]}}


# --- Flattening Tests ---


def test_and_flattening() -> None:
    """Chained & flattens into single AndExpr."""
    expr = (F("a") == 1) & (F("b") == 2) & (F("c") == 3)
    assert isinstance(expr, AndExpr)
    assert len(expr.conditions) == 3
    assert expr.model_dump() == {
        "$and": [
            {"$eq": ["$a", 1]},
            {"$eq": ["$b", 2]},
            {"$eq": ["$c", 3]},
        ]
    }


def test_or_flattening() -> None:
    """Chained | flattens into single OrExpr."""
    expr = (F("a") == 1) | (F("b") == 2) | (F("c") == 3)
    assert isinstance(expr, OrExpr)
    assert len(expr.conditions) == 3
    assert expr.model_dump() == {
        "$or": [
            {"$eq": ["$a", 1]},
            {"$eq": ["$b", 2]},
            {"$eq": ["$c", 3]},
        ]
    }


# --- Deeply Nested Expressions Tests ---


def test_deeply_nested_serialization() -> None:
    """Deeply nested expressions serialize correctly."""
    deeply_nested_expr = OrExpr(
        conditions=[
            AndExpr(
                conditions=[
                    EqExpr(left=F("x"), right=1),
                    LtExpr(left=F("y"), right=10),
                ]
            ),
            GtExpr(left=F("z"), right=100),
        ]
    )
    assert deeply_nested_expr.model_dump() == {
        "$or": [
            {"$and": [{"$eq": ["$x", 1]}, {"$lt": ["$y", 10]}]},
            {"$gt": ["$z", 100]},
        ]
    }


def test_and_containing_or() -> None:
    """AND containing OR serializes correctly."""
    expr = (F("a") == 1) & ((F("b") == 2) | (F("c") == 3))
    assert expr.model_dump() == {
        "$and": [
            {"$eq": ["$a", 1]},
            {"$or": [{"$eq": ["$b", 2]}, {"$eq": ["$c", 3]}]},
        ]
    }


def test_or_containing_and() -> None:
    """OR containing AND serializes correctly."""
    expr = (F("a") == 1) | ((F("b") == 2) & (F("c") == 3))
    assert expr.model_dump() == {
        "$or": [
            {"$eq": ["$a", 1]},
            {"$and": [{"$eq": ["$b", 2]}, {"$eq": ["$c", 3]}]},
        ]
    }


def test_complex_combined_expr() -> None:
    """Complex expression from fixture serializes correctly."""
    complex_combined_expr = (
        (F("status") == "active")
        & (F("is_active") == True)  # noqa: E712
        & (F("age") > 18)
        & ((F("score") < 50) | (F("bonus") >= 10))
    )
    result = complex_combined_expr.model_dump()
    assert "$and" in result
    assert len(result["$and"]) == 4
    assert "$or" in result["$and"][3]


# --- Mixed Expressions Tests ---


def test_mixed_with_raw_dicts() -> None:
    """Expressions can be mixed with raw dicts."""
    expr = AndExpr(
        conditions=[
            EqExpr(left=F("a"), right=1),
            {"$regex": {"input": "$name", "regex": "^test"}},
        ]
    )
    assert expr.model_dump() == {
        "$and": [
            {"$eq": ["$a", 1]},
            {"$regex": {"input": "$name", "regex": "^test"}},
        ]
    }

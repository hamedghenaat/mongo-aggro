"""Tests for comparison expression operators.

This module tests:
- EqExpr, NeExpr, GtExpr, GteExpr, LtExpr, LteExpr, CmpExpr
- Operator overloading (==, !=, >, >=, <, <=)
- Field-to-field comparisons
- Various value types in comparisons
"""

from datetime import datetime

import pytest
from pydantic import ValidationError

from mongo_aggro.expressions import (
    CmpExpr,
    EqExpr,
    F,
    Field,
    GteExpr,
    GtExpr,
    LteExpr,
    LtExpr,
    NeExpr,
)

# --- EqExpr Tests ---


def test_eq_expr_serialization() -> None:
    """EqExpr serializes correctly."""
    expr = EqExpr(left=F("status"), right="active")
    assert expr.model_dump() == {"$eq": ["$status", "active"]}


def test_eq_expr_with_number() -> None:
    """EqExpr works with numeric values."""
    expr = EqExpr(left=F("count"), right=42)
    assert expr.model_dump() == {"$eq": ["$count", 42]}


def test_eq_expr_with_boolean() -> None:
    """EqExpr works with boolean values."""
    expr = EqExpr(left=F("active"), right=True)
    assert expr.model_dump() == {"$eq": ["$active", True]}


def test_eq_expr_with_none() -> None:
    """EqExpr works with None values."""
    expr = EqExpr(left=F("value"), right=None)
    assert expr.model_dump() == {"$eq": ["$value", None]}


def test_eq_expr_missing_left_raises() -> None:
    """EqExpr requires left operand."""
    with pytest.raises(ValidationError):
        EqExpr(right="value")  # type: ignore[call-arg]


def test_eq_expr_missing_right_raises() -> None:
    """EqExpr requires right operand."""
    with pytest.raises(ValidationError):
        EqExpr(left=F("field"))  # type: ignore[call-arg]


def test_eq_expr_extra_field_raises() -> None:
    """EqExpr rejects extra fields."""
    with pytest.raises(ValidationError):
        EqExpr(left=F("a"), right=1, extra="invalid")  # type: ignore


# --- NeExpr Tests ---


def test_ne_expr_serialization() -> None:
    """NeExpr serializes correctly."""
    expr = NeExpr(left=F("status"), right="deleted")
    assert expr.model_dump() == {"$ne": ["$status", "deleted"]}


def test_ne_expr_missing_left_raises() -> None:
    """NeExpr requires left operand."""
    with pytest.raises(ValidationError):
        NeExpr(right="value")  # type: ignore[call-arg]


# --- GtExpr Tests ---


def test_gt_expr_serialization() -> None:
    """GtExpr serializes correctly."""
    expr = GtExpr(left=F("age"), right=18)
    assert expr.model_dump() == {"$gt": ["$age", 18]}


def test_gt_expr_missing_right_raises() -> None:
    """GtExpr requires right operand."""
    with pytest.raises(ValidationError):
        GtExpr(left=F("age"))  # type: ignore[call-arg]


# --- GteExpr Tests ---


def test_gte_expr_serialization() -> None:
    """GteExpr serializes correctly."""
    expr = GteExpr(left=F("age"), right=18)
    assert expr.model_dump() == {"$gte": ["$age", 18]}


# --- LtExpr Tests ---


def test_lt_expr_serialization() -> None:
    """LtExpr serializes correctly."""
    expr = LtExpr(left=F("age"), right=65)
    assert expr.model_dump() == {"$lt": ["$age", 65]}


# --- LteExpr Tests ---


def test_lte_expr_serialization() -> None:
    """LteExpr serializes correctly."""
    expr = LteExpr(left=F("age"), right=65)
    assert expr.model_dump() == {"$lte": ["$age", 65]}


# --- CmpExpr Tests ---


def test_cmp_expr_serialization() -> None:
    """CmpExpr serializes correctly."""
    expr = CmpExpr(left=F("a"), right=F("b"))
    assert expr.model_dump() == {"$cmp": ["$a", "$b"]}


def test_cmp_expr_missing_both_raises() -> None:
    """CmpExpr requires both operands."""
    with pytest.raises(ValidationError):
        CmpExpr()  # type: ignore[call-arg]


# --- Comparison Operators Tests ---


def test_eq_via_operator() -> None:
    """== operator creates EqExpr."""
    status_field = F("status")
    expr = status_field == "active"
    assert isinstance(expr, EqExpr)
    assert expr.model_dump() == {"$eq": ["$status", "active"]}


def test_ne_via_operator() -> None:
    """!= operator creates NeExpr."""
    status_field = F("status")
    expr = status_field != "deleted"
    assert isinstance(expr, NeExpr)
    assert expr.model_dump() == {"$ne": ["$status", "deleted"]}


def test_gt_via_operator(age_field: Field) -> None:
    """> operator creates GtExpr."""
    expr = age_field > 18
    assert isinstance(expr, GtExpr)
    assert expr.model_dump() == {"$gt": ["$age", 18]}


def test_ge_via_operator(age_field: Field) -> None:
    """>= operator creates GteExpr."""
    expr = age_field >= 18
    assert isinstance(expr, GteExpr)
    assert expr.model_dump() == {"$gte": ["$age", 18]}


def test_lt_via_operator(age_field: Field) -> None:
    """< operator creates LtExpr."""
    expr = age_field < 65
    assert isinstance(expr, LtExpr)
    assert expr.model_dump() == {"$lt": ["$age", 65]}


def test_le_via_operator(age_field: Field) -> None:
    """<= operator creates LteExpr."""
    expr = age_field <= 65
    assert isinstance(expr, LteExpr)
    assert expr.model_dump() == {"$lte": ["$age", 65]}


# --- Field to Field Comparison Tests ---


def test_field_to_field_comparison() -> None:
    """Comparing two fields works."""
    expr = F("price") > F("cost")
    assert expr.model_dump() == {"$gt": ["$price", "$cost"]}


def test_field_with_datetime() -> None:
    """Field comparison with datetime works."""
    dt = datetime(2024, 1, 1)
    expr = F("created_at") >= dt
    assert expr.model_dump() == {"$gte": ["$created_at", dt]}


# --- Parametrized Comparisons Tests ---


@pytest.mark.parametrize(
    "value",
    [
        10,
        "string",
        True,
        False,
        None,
        3.14,
        datetime(2024, 1, 1),
    ],
)
def test_eq_with_various_types(value) -> None:
    """EqExpr handles various Python types."""
    expr = F("field") == value
    result = expr.model_dump()
    assert result == {"$eq": ["$field", value]}


@pytest.mark.parametrize(
    "op_method,expr_class,mongo_op",
    [
        ("__eq__", EqExpr, "$eq"),
        ("__ne__", NeExpr, "$ne"),
        ("__gt__", GtExpr, "$gt"),
        ("__ge__", GteExpr, "$gte"),
        ("__lt__", LtExpr, "$lt"),
        ("__le__", LteExpr, "$lte"),
    ],
)
def test_all_comparison_operators(op_method, expr_class, mongo_op) -> None:
    """All comparison operators create correct expression types."""
    field = F("value")
    expr = getattr(field, op_method)(10)

    assert isinstance(expr, expr_class)
    assert mongo_op in expr.model_dump()

"""Tests for conditional expression operators.

This module tests:
- CondExpr (ternary conditional)
- IfNullExpr (null coalescing)
- SwitchExpr (multi-branch conditional)
"""

import pytest
from pydantic import ValidationError

from mongo_aggro.expressions import (
    CondExpr,
    EqExpr,
    F,
    GtExpr,
    IfNullExpr,
    MultiplyExpr,
    SwitchBranch,
    SwitchExpr,
)

# --- CondExpr Tests ---


def test_cond_expr() -> None:
    """CondExpr serialization."""
    expr = CondExpr(
        if_=GtExpr(left=F("qty"), right=100),
        then="bulk",
        else_="retail",
    )
    result = expr.model_dump()
    assert result == {
        "$cond": {
            "if": {"$gt": ["$qty", 100]},
            "then": "bulk",
            "else": "retail",
        }
    }


def test_cond_with_comparison_operator() -> None:
    """CondExpr with operator-built expression."""
    expr = CondExpr(
        if_=(F("qty") > 100),
        then=MultiplyExpr(operands=[F("price"), 0.9]),
        else_=F("price"),
    )
    result = expr.model_dump()
    assert result["$cond"]["if"] == {"$gt": ["$qty", 100]}
    assert result["$cond"]["then"] == {"$multiply": ["$price", 0.9]}
    assert result["$cond"]["else"] == "$price"


def test_cond_with_nested_cond() -> None:
    """CondExpr can contain nested CondExpr."""
    inner_cond = CondExpr(
        if_=(F("level") > 5),
        then="expert",
        else_="intermediate",
    )
    expr = CondExpr(
        if_=(F("level") > 0),
        then=inner_cond,
        else_="beginner",
    )
    result = expr.model_dump()
    assert "$cond" in result["$cond"]["then"]


def test_cond_expr_missing_if_raises() -> None:
    """CondExpr requires if_ parameter."""
    with pytest.raises(ValidationError):
        CondExpr(then="yes", else_="no")  # type: ignore[call-arg]


def test_cond_expr_missing_then_raises() -> None:
    """CondExpr requires then parameter."""
    with pytest.raises(ValidationError):
        CondExpr(if_=(F("x") > 0), else_="no")  # type: ignore[call-arg]


def test_cond_expr_missing_else_raises() -> None:
    """CondExpr requires else_ parameter."""
    with pytest.raises(ValidationError):
        CondExpr(if_=(F("x") > 0), then="yes")  # type: ignore[call-arg]


# --- IfNullExpr Tests ---


def test_ifnull_expr() -> None:
    """IfNullExpr serialization."""
    expr = IfNullExpr(input=F("name"), replacement="Unknown")
    assert expr.model_dump() == {"$ifNull": ["$name", "Unknown"]}


def test_ifnull_with_field_replacement() -> None:
    """IfNullExpr with field as replacement."""
    expr = IfNullExpr(input=F("nickname"), replacement=F("name"))
    assert expr.model_dump() == {"$ifNull": ["$nickname", "$name"]}


def test_ifnull_expr_missing_input_raises() -> None:
    """IfNullExpr requires input."""
    with pytest.raises(ValidationError):
        IfNullExpr(replacement="default")  # type: ignore[call-arg]


def test_ifnull_expr_missing_replacement_raises() -> None:
    """IfNullExpr requires replacement."""
    with pytest.raises(ValidationError):
        IfNullExpr(input=F("name"))  # type: ignore[call-arg]


# --- SwitchExpr Tests ---


def test_switch_expr() -> None:
    """SwitchExpr serialization."""
    expr = SwitchExpr(
        branches=[
            SwitchBranch(case=EqExpr(left=F("status"), right="A"), then=1),
            SwitchBranch(case=EqExpr(left=F("status"), right="B"), then=2),
        ],
        default=0,
    )
    result = expr.model_dump()
    assert result["$switch"]["branches"][0] == {
        "case": {"$eq": ["$status", "A"]},
        "then": 1,
    }
    assert result["$switch"]["default"] == 0


def test_switch_expr_no_default() -> None:
    """SwitchExpr without default."""
    expr = SwitchExpr(
        branches=[
            SwitchBranch(case=EqExpr(left=F("x"), right=1), then="one"),
        ],
    )
    result = expr.model_dump()
    assert "default" not in result["$switch"]


def test_switch_with_operator_expressions() -> None:
    """SwitchExpr with operator-built expressions."""
    expr = SwitchExpr(
        branches=[
            SwitchBranch(case=(F("score") >= 90), then="A"),
            SwitchBranch(case=(F("score") >= 80), then="B"),
            SwitchBranch(case=(F("score") >= 70), then="C"),
        ],
        default="F",
    )
    result = expr.model_dump()
    assert len(result["$switch"]["branches"]) == 3
    assert result["$switch"]["default"] == "F"


def test_switch_expr_missing_branches_raises() -> None:
    """SwitchExpr requires branches list."""
    with pytest.raises(ValidationError):
        SwitchExpr(default=0)  # type: ignore[call-arg]


def test_switch_branch_missing_case_raises() -> None:
    """SwitchBranch requires case."""
    with pytest.raises(ValidationError):
        SwitchBranch(then=1)  # type: ignore[call-arg]


def test_switch_branch_missing_then_raises() -> None:
    """SwitchBranch requires then."""
    with pytest.raises(ValidationError):
        SwitchBranch(case=EqExpr(left=F("x"), right=1))  # type: ignore[call-arg]

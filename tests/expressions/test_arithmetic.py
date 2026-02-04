"""Tests for arithmetic expression operators.

This module tests:
- AddExpr, SubtractExpr, MultiplyExpr, DivideExpr
- AbsExpr, ModExpr
- CeilExpr, FloorExpr, RoundExpr, TruncExpr
- SqrtExpr, PowExpr, ExpExpr, LnExpr, Log10Expr, LogExpr
- Nested arithmetic expressions
"""

import pytest
from pydantic import ValidationError

from mongo_aggro.expressions import (
    AbsExpr,
    AddExpr,
    CeilExpr,
    DivideExpr,
    ExpExpr,
    F,
    FloorExpr,
    LnExpr,
    Log10Expr,
    LogExpr,
    ModExpr,
    MultiplyExpr,
    PowExpr,
    RoundExpr,
    SqrtExpr,
    SubtractExpr,
    TruncExpr,
)

# --- AddExpr Tests ---


def test_add_expr_two_operands() -> None:
    """AddExpr with two operands."""
    expr = AddExpr(operands=[F("price"), F("tax")])
    assert expr.model_dump() == {"$add": ["$price", "$tax"]}


def test_add_expr_multiple_operands() -> None:
    """AddExpr with multiple operands."""
    expr = AddExpr(operands=[F("a"), F("b"), 10])
    assert expr.model_dump() == {"$add": ["$a", "$b", 10]}


def test_add_expr_with_constants() -> None:
    """AddExpr with constant values."""
    expr = AddExpr(operands=[1, 2, 3])
    assert expr.model_dump() == {"$add": [1, 2, 3]}


def test_add_expr_missing_operands_raises() -> None:
    """AddExpr requires operands list."""
    with pytest.raises(ValidationError):
        AddExpr()  # type: ignore[call-arg]


# --- SubtractExpr Tests ---


def test_subtract_expr() -> None:
    """SubtractExpr serialization."""
    expr = SubtractExpr(left=F("total"), right=F("discount"))
    assert expr.model_dump() == {"$subtract": ["$total", "$discount"]}


def test_subtract_expr_missing_left_raises() -> None:
    """SubtractExpr requires left operand."""
    with pytest.raises(ValidationError):
        SubtractExpr(right=F("value"))  # type: ignore[call-arg]


# --- MultiplyExpr Tests ---


def test_multiply_expr() -> None:
    """MultiplyExpr serialization."""
    expr = MultiplyExpr(operands=[F("price"), F("quantity")])
    assert expr.model_dump() == {"$multiply": ["$price", "$quantity"]}


def test_multiply_expr_missing_operands_raises() -> None:
    """MultiplyExpr requires operands list."""
    with pytest.raises(ValidationError):
        MultiplyExpr()  # type: ignore[call-arg]


# --- DivideExpr Tests ---


def test_divide_expr() -> None:
    """DivideExpr serialization."""
    expr = DivideExpr(dividend=F("total"), divisor=F("count"))
    assert expr.model_dump() == {"$divide": ["$total", "$count"]}


def test_divide_expr_missing_dividend_raises() -> None:
    """DivideExpr requires dividend."""
    with pytest.raises(ValidationError):
        DivideExpr(divisor=F("count"))  # type: ignore[call-arg]


def test_divide_expr_missing_divisor_raises() -> None:
    """DivideExpr requires divisor."""
    with pytest.raises(ValidationError):
        DivideExpr(dividend=F("total"))  # type: ignore[call-arg]


# --- AbsExpr Tests ---


def test_abs_expr() -> None:
    """AbsExpr serialization."""
    expr = AbsExpr(value=F("balance"))
    assert expr.model_dump() == {"$abs": "$balance"}


def test_abs_expr_missing_value_raises() -> None:
    """AbsExpr requires value."""
    with pytest.raises(ValidationError):
        AbsExpr()  # type: ignore[call-arg]


# --- ModExpr Tests ---


def test_mod_expr() -> None:
    """ModExpr serialization."""
    expr = ModExpr(dividend=F("num"), divisor=2)
    assert expr.model_dump() == {"$mod": ["$num", 2]}


# --- Rounding Expressions Tests ---


def test_ceil_expr() -> None:
    """CeilExpr serialization."""
    expr = CeilExpr(input=F("value"))
    assert expr.model_dump() == {"$ceil": "$value"}


def test_floor_expr() -> None:
    """FloorExpr serialization."""
    expr = FloorExpr(input=F("value"))
    assert expr.model_dump() == {"$floor": "$value"}


def test_round_expr() -> None:
    """RoundExpr serialization."""
    expr = RoundExpr(input=F("value"), place=2)
    assert expr.model_dump() == {"$round": ["$value", 2]}


def test_round_expr_default_place() -> None:
    """RoundExpr with default place (0)."""
    expr = RoundExpr(input=F("value"))
    assert expr.model_dump() == {"$round": ["$value", 0]}


def test_trunc_expr() -> None:
    """TruncExpr serialization."""
    expr = TruncExpr(input=F("value"), place=1)
    assert expr.model_dump() == {"$trunc": ["$value", 1]}


def test_ceil_expr_missing_input_raises() -> None:
    """CeilExpr requires input."""
    with pytest.raises(ValidationError):
        CeilExpr()  # type: ignore[call-arg]


# --- Power Expressions Tests ---


def test_sqrt_expr() -> None:
    """SqrtExpr serialization."""
    expr = SqrtExpr(input=F("value"))
    assert expr.model_dump() == {"$sqrt": "$value"}


def test_pow_expr() -> None:
    """PowExpr serialization."""
    expr = PowExpr(base=F("value"), exponent=2)
    assert expr.model_dump() == {"$pow": ["$value", 2]}


def test_exp_expr() -> None:
    """ExpExpr serialization."""
    expr = ExpExpr(input=F("value"))
    assert expr.model_dump() == {"$exp": "$value"}


def test_ln_expr() -> None:
    """LnExpr serialization."""
    expr = LnExpr(input=F("value"))
    assert expr.model_dump() == {"$ln": "$value"}


def test_log10_expr() -> None:
    """Log10Expr serialization."""
    expr = Log10Expr(input=F("value"))
    assert expr.model_dump() == {"$log10": "$value"}


def test_log_expr() -> None:
    """LogExpr serialization."""
    expr = LogExpr(input=F("value"), base=2)
    assert expr.model_dump() == {"$log": ["$value", 2]}


def test_pow_expr_missing_base_raises() -> None:
    """PowExpr requires base."""
    with pytest.raises(ValidationError):
        PowExpr(exponent=2)  # type: ignore[call-arg]


def test_log_expr_missing_base_raises() -> None:
    """LogExpr requires base."""
    with pytest.raises(ValidationError):
        LogExpr(input=F("value"))  # type: ignore[call-arg]


# --- Nested Arithmetic Expressions Tests ---


def test_nested_arithmetic_expressions() -> None:
    """Nested arithmetic expressions serialize correctly."""
    # (price * qty) / total
    expr = DivideExpr(
        dividend=MultiplyExpr(operands=[F("price"), F("qty")]),
        divisor=F("total"),
    )
    result = expr.model_dump()
    assert result == {
        "$divide": [
            {"$multiply": ["$price", "$qty"]},
            "$total",
        ]
    }

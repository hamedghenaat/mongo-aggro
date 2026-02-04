"""Tests for type conversion expression operators.

This module tests:
- ToStringExpr, ToIntExpr, ToDoubleExpr, ToBoolExpr
- ToObjectIdExpr, ToLongExpr, ToDecimalExpr
- ConvertExpr (generic conversion with error handling)
- TypeExpr (BSON type detection)
- IsNumberExpr (numeric type check)
"""

import pytest
from pydantic import ValidationError

from mongo_aggro.expressions import (
    ConvertExpr,
    F,
    IsNumberExpr,
    ToBoolExpr,
    ToDecimalExpr,
    ToDoubleExpr,
    ToIntExpr,
    ToLongExpr,
    ToObjectIdExpr,
    ToStringExpr,
    TypeExpr,
)

# --- ToStringExpr Tests ---


def test_to_string_expr() -> None:
    """ToStringExpr serialization."""
    expr = ToStringExpr(input=F("numericId"))
    assert expr.model_dump() == {"$toString": "$numericId"}


def test_to_string_missing_input_raises() -> None:
    """ToStringExpr requires input."""
    with pytest.raises(ValidationError):
        ToStringExpr()  # type: ignore[call-arg]


# --- ToIntExpr Tests ---


def test_to_int_expr() -> None:
    """ToIntExpr serialization."""
    expr = ToIntExpr(input=F("stringNum"))
    assert expr.model_dump() == {"$toInt": "$stringNum"}


def test_to_int_missing_input_raises() -> None:
    """ToIntExpr requires input."""
    with pytest.raises(ValidationError):
        ToIntExpr()  # type: ignore[call-arg]


# --- ToDoubleExpr Tests ---


def test_to_double_expr() -> None:
    """ToDoubleExpr serialization."""
    expr = ToDoubleExpr(input=F("intValue"))
    assert expr.model_dump() == {"$toDouble": "$intValue"}


# --- ToBoolExpr Tests ---


def test_to_bool_expr() -> None:
    """ToBoolExpr serialization."""
    expr = ToBoolExpr(input=F("flag"))
    assert expr.model_dump() == {"$toBool": "$flag"}


# --- ToObjectIdExpr Tests ---


def test_to_object_id_expr() -> None:
    """ToObjectIdExpr serialization."""
    expr = ToObjectIdExpr(input=F("idString"))
    assert expr.model_dump() == {"$toObjectId": "$idString"}


# --- ToLongExpr Tests ---


def test_to_long_expr() -> None:
    """ToLongExpr serialization."""
    expr = ToLongExpr(input=F("value"))
    assert expr.model_dump() == {"$toLong": "$value"}


# --- ToDecimalExpr Tests ---


def test_to_decimal_expr() -> None:
    """ToDecimalExpr serialization."""
    expr = ToDecimalExpr(input=F("value"))
    assert expr.model_dump() == {"$toDecimal": "$value"}


# --- ConvertExpr Tests ---


def test_convert_expr() -> None:
    """ConvertExpr serialization."""
    expr = ConvertExpr(input=F("value"), to="int")
    assert expr.model_dump() == {
        "$convert": {
            "input": "$value",
            "to": "int",
        }
    }


def test_convert_expr_with_error_handling() -> None:
    """ConvertExpr with error handling."""
    expr = ConvertExpr(
        input=F("value"),
        to="double",
        on_error=0.0,
        on_null=-1.0,
    )
    result = expr.model_dump()
    assert result["$convert"]["onError"] == 0.0
    assert result["$convert"]["onNull"] == -1.0


def test_convert_expr_missing_input_raises() -> None:
    """ConvertExpr requires input."""
    with pytest.raises(ValidationError):
        ConvertExpr(to="int")  # type: ignore[call-arg]


def test_convert_expr_missing_to_raises() -> None:
    """ConvertExpr requires to parameter."""
    with pytest.raises(ValidationError):
        ConvertExpr(input=F("value"))  # type: ignore[call-arg]


# --- TypeExpr Tests ---


def test_type_expr() -> None:
    """TypeExpr serialization."""
    expr = TypeExpr(input=F("field"))
    assert expr.model_dump() == {"$type": "$field"}


def test_type_missing_input_raises() -> None:
    """TypeExpr requires input."""
    with pytest.raises(ValidationError):
        TypeExpr()  # type: ignore[call-arg]


# --- IsNumberExpr Tests ---


def test_is_number_expr() -> None:
    """IsNumberExpr serialization."""
    expr = IsNumberExpr(input=F("value"))
    assert expr.model_dump() == {"$isNumber": "$value"}


def test_is_number_missing_input_raises() -> None:
    """IsNumberExpr requires input."""
    with pytest.raises(ValidationError):
        IsNumberExpr()  # type: ignore[call-arg]

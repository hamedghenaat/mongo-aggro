"""Arithmetic expression operators for MongoDB aggregation."""

from typing import Any

from pydantic import model_serializer

from mongo_aggro.base import serialize_value
from mongo_aggro.expressions.base import ExpressionBase


class AddExpr(ExpressionBase):
    """
    $add expression operator - adds numbers or dates.

    Example:
        >>> AddExpr(operands=[F("price"), F("tax")]).model_dump()
        {"$add": ["$price", "$tax"]}
    """

    operands: list[Any]

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $add expression."""
        return {"$add": [serialize_value(o) for o in self.operands]}


class SubtractExpr(ExpressionBase):
    """
    $subtract expression operator - subtracts two numbers or dates.

    Example:
        >>> SubtractExpr(left=F("total"), right=F("discount")).model_dump()
        {"$subtract": ["$total", "$discount"]}
    """

    left: Any
    right: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $subtract expression."""
        return {
            "$subtract": [
                serialize_value(self.left),
                serialize_value(self.right),
            ]
        }


class MultiplyExpr(ExpressionBase):
    """
    $multiply expression operator - multiplies numbers.

    Example:
        >>> MultiplyExpr(operands=[F("price"), F("qty")]).model_dump()
        {"$multiply": ["$price", "$qty"]}
    """

    operands: list[Any]

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $multiply expression."""
        return {"$multiply": [serialize_value(o) for o in self.operands]}


class DivideExpr(ExpressionBase):
    """
    $divide expression operator - divides two numbers.

    Example:
        >>> DivideExpr(dividend=F("total"), divisor=F("count")).model_dump()
        {"$divide": ["$total", "$count"]}
    """

    dividend: Any
    divisor: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $divide expression."""
        return {
            "$divide": [
                serialize_value(self.dividend),
                serialize_value(self.divisor),
            ]
        }


class AbsExpr(ExpressionBase):
    """
    $abs expression operator - returns absolute value.

    Example:
        >>> AbsExpr(value=F("balance")).model_dump()
        {"$abs": "$balance"}
    """

    value: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $abs expression."""
        return {"$abs": serialize_value(self.value)}


class ModExpr(ExpressionBase):
    """
    $mod expression operator - returns remainder of division.

    Example:
        >>> ModExpr(dividend=F("num"), divisor=2).model_dump()
        {"$mod": ["$num", 2]}
    """

    dividend: Any
    divisor: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $mod expression."""
        return {
            "$mod": [
                serialize_value(self.dividend),
                serialize_value(self.divisor),
            ]
        }


class CeilExpr(ExpressionBase):
    """
    $ceil expression operator - rounds up to nearest integer.

    Example:
        >>> CeilExpr(input=F("value")).model_dump()
        {"$ceil": "$value"}
    """

    input: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $ceil expression."""
        return {"$ceil": serialize_value(self.input)}


class FloorExpr(ExpressionBase):
    """
    $floor expression operator - rounds down to nearest integer.

    Example:
        >>> FloorExpr(input=F("value")).model_dump()
        {"$floor": "$value"}
    """

    input: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $floor expression."""
        return {"$floor": serialize_value(self.input)}


class RoundExpr(ExpressionBase):
    """
    $round expression operator - rounds to specified decimal place.

    Example:
        >>> RoundExpr(input=F("value"), place=2).model_dump()
        {"$round": ["$value", 2]}
    """

    input: Any
    place: int = 0

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $round expression."""
        return {"$round": [serialize_value(self.input), self.place]}


class TruncExpr(ExpressionBase):
    """
    $trunc expression operator - truncates to specified decimal place.

    Example:
        >>> TruncExpr(input=F("value"), place=2).model_dump()
        {"$trunc": ["$value", 2]}
    """

    input: Any
    place: int = 0

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $trunc expression."""
        return {"$trunc": [serialize_value(self.input), self.place]}


class SqrtExpr(ExpressionBase):
    """
    $sqrt expression operator - calculates square root.

    Example:
        >>> SqrtExpr(input=F("value")).model_dump()
        {"$sqrt": "$value"}
    """

    input: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $sqrt expression."""
        return {"$sqrt": serialize_value(self.input)}


class PowExpr(ExpressionBase):
    """
    $pow expression operator - raises number to exponent.

    Example:
        >>> PowExpr(base=F("value"), exponent=2).model_dump()
        {"$pow": ["$value", 2]}
    """

    base: Any
    exponent: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $pow expression."""
        return {
            "$pow": [
                serialize_value(self.base),
                serialize_value(self.exponent),
            ]
        }


class ExpExpr(ExpressionBase):
    """
    $exp expression operator - raises e to the specified exponent.

    Example:
        >>> ExpExpr(input=F("value")).model_dump()
        {"$exp": "$value"}
    """

    input: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $exp expression."""
        return {"$exp": serialize_value(self.input)}


class LnExpr(ExpressionBase):
    """
    $ln expression operator - calculates natural logarithm.

    Example:
        >>> LnExpr(input=F("value")).model_dump()
        {"$ln": "$value"}
    """

    input: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $ln expression."""
        return {"$ln": serialize_value(self.input)}


class Log10Expr(ExpressionBase):
    """
    $log10 expression operator - calculates log base 10.

    Example:
        >>> Log10Expr(input=F("value")).model_dump()
        {"$log10": "$value"}
    """

    input: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $log10 expression."""
        return {"$log10": serialize_value(self.input)}


class LogExpr(ExpressionBase):
    """
    $log expression operator - calculates log with specified base.

    Example:
        >>> LogExpr(input=F("value"), base=2).model_dump()
        {"$log": ["$value", 2]}
    """

    input: Any
    base: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $log expression."""
        return {
            "$log": [serialize_value(self.input), serialize_value(self.base)]
        }


__all__ = [
    "AddExpr",
    "SubtractExpr",
    "MultiplyExpr",
    "DivideExpr",
    "AbsExpr",
    "ModExpr",
    "CeilExpr",
    "FloorExpr",
    "RoundExpr",
    "TruncExpr",
    "SqrtExpr",
    "PowExpr",
    "ExpExpr",
    "LnExpr",
    "Log10Expr",
    "LogExpr",
]

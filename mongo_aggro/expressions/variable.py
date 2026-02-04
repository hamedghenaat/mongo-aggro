"""Variable expression operators for MongoDB aggregation."""

from typing import Any

from pydantic import model_serializer

from mongo_aggro.base import serialize_value
from mongo_aggro.expressions.base import ExpressionBase


class LetExpr(ExpressionBase):
    """
    $let expression operator - defines variables for use in expression.

    Example:
        >>> LetExpr(
        ...     vars={"total": MultiplyExpr(operands=[F("price"), F("qty")])},
        ...     in_=GtExpr(left=Field("$$total"), right=100)
        ... ).model_dump()
        {"$let": {"vars": {"total": {...}}, "in": {...}}}
    """

    vars: dict[str, Any]
    in_: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $let expression."""
        return {
            "$let": {
                "vars": {k: serialize_value(v) for k, v in self.vars.items()},
                "in": serialize_value(self.in_),
            }
        }


class LiteralExpr(ExpressionBase):
    """
    $literal expression operator - returns value without parsing.

    Example:
        >>> LiteralExpr(value="$field").model_dump()
        {"$literal": "$field"}
    """

    value: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $literal expression."""
        return {"$literal": self.value}


class RandExpr(ExpressionBase):
    """
    $rand expression operator - returns random float between 0 and 1.

    Example:
        >>> RandExpr().model_dump()
        {"$rand": {}}
    """

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $rand expression."""
        return {"$rand": {}}


__all__ = [
    "LetExpr",
    "LiteralExpr",
    "RandExpr",
]

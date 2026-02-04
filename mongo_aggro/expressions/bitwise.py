"""Bitwise expression operators for MongoDB aggregation."""

from typing import Any

from pydantic import model_serializer

from mongo_aggro.base import serialize_value
from mongo_aggro.expressions.base import ExpressionBase


class BitAndExpr(ExpressionBase):
    """
    $bitAnd expression operator - bitwise AND.

    Example:
        >>> BitAndExpr(operands=[F("a"), F("b")]).model_dump()
        {"$bitAnd": ["$a", "$b"]}
    """

    operands: list[Any]

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $bitAnd expression."""
        return {"$bitAnd": [serialize_value(o) for o in self.operands]}


class BitOrExpr(ExpressionBase):
    """
    $bitOr expression operator - bitwise OR.

    Example:
        >>> BitOrExpr(operands=[F("a"), F("b")]).model_dump()
        {"$bitOr": ["$a", "$b"]}
    """

    operands: list[Any]

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $bitOr expression."""
        return {"$bitOr": [serialize_value(o) for o in self.operands]}


class BitXorExpr(ExpressionBase):
    """
    $bitXor expression operator - bitwise XOR.

    Example:
        >>> BitXorExpr(operands=[F("a"), F("b")]).model_dump()
        {"$bitXor": ["$a", "$b"]}
    """

    operands: list[Any]

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $bitXor expression."""
        return {"$bitXor": [serialize_value(o) for o in self.operands]}


class BitNotExpr(ExpressionBase):
    """
    $bitNot expression operator - bitwise NOT.

    Example:
        >>> BitNotExpr(input=F("value")).model_dump()
        {"$bitNot": "$value"}
    """

    input: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $bitNot expression."""
        return {"$bitNot": serialize_value(self.input)}


__all__ = [
    "BitAndExpr",
    "BitOrExpr",
    "BitXorExpr",
    "BitNotExpr",
]

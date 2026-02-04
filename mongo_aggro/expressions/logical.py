"""Logical expression operators for MongoDB aggregation."""

from typing import Any

from pydantic import model_serializer

from mongo_aggro.base import serialize_value
from mongo_aggro.expressions.base import ExpressionBase


class AndExpr(ExpressionBase):
    """
    $and expression operator - logical AND.

    Example:
        >>> AndExpr(conditions=[
        ...     EqExpr(left=F("a"), right=1),
        ...     GtExpr(left=F("b"), right=2)
        ... ]).model_dump()
        {"$and": [{"$eq": ["$a", 1]}, {"$gt": ["$b", 2]}]}
    """

    conditions: list[Any]

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $and expression."""
        return {"$and": [serialize_value(c) for c in self.conditions]}


class OrExpr(ExpressionBase):
    """
    $or expression operator - logical OR.

    Example:
        >>> OrExpr(conditions=[
        ...     EqExpr(left=F("a"), right=1),
        ...     EqExpr(left=F("a"), right=2)
        ... ]).model_dump()
        {"$or": [{"$eq": ["$a", 1]}, {"$eq": ["$a", 2]}]}
    """

    conditions: list[Any]

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $or expression."""
        return {"$or": [serialize_value(c) for c in self.conditions]}


class NotExpr(ExpressionBase):
    """
    $not expression operator - logical NOT.

    Example:
        >>> NotExpr(condition=EqExpr(left=F("a"), right=1)).model_dump()
        {"$not": {"$eq": ["$a", 1]}}
    """

    condition: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $not expression."""
        return {"$not": serialize_value(self.condition)}


__all__ = [
    "AndExpr",
    "OrExpr",
    "NotExpr",
]

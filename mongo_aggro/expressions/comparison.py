"""Comparison expression operators for MongoDB aggregation."""

from typing import Any

from pydantic import model_serializer

from mongo_aggro.base import serialize_value
from mongo_aggro.expressions.base import ExpressionBase


class EqExpr(ExpressionBase):
    """
    $eq expression operator - tests equality.

    Example:
        >>> EqExpr(left=F("status"), right="active").model_dump()
        {"$eq": ["$status", "active"]}
    """

    left: Any
    right: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $eq expression."""
        return {
            "$eq": [serialize_value(self.left), serialize_value(self.right)]
        }


class NeExpr(ExpressionBase):
    """
    $ne expression operator - tests inequality.

    Example:
        >>> NeExpr(left=F("status"), right="deleted").model_dump()
        {"$ne": ["$status", "deleted"]}
    """

    left: Any
    right: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $ne expression."""
        return {
            "$ne": [serialize_value(self.left), serialize_value(self.right)]
        }


class GtExpr(ExpressionBase):
    """
    $gt expression operator - tests greater than.

    Example:
        >>> GtExpr(left=F("age"), right=18).model_dump()
        {"$gt": ["$age", 18]}
    """

    left: Any
    right: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $gt expression."""
        return {
            "$gt": [serialize_value(self.left), serialize_value(self.right)]
        }


class GteExpr(ExpressionBase):
    """
    $gte expression operator - tests greater than or equal.

    Example:
        >>> GteExpr(left=F("age"), right=18).model_dump()
        {"$gte": ["$age", 18]}
    """

    left: Any
    right: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $gte expression."""
        return {
            "$gte": [serialize_value(self.left), serialize_value(self.right)]
        }


class LtExpr(ExpressionBase):
    """
    $lt expression operator - tests less than.

    Example:
        >>> LtExpr(left=F("age"), right=65).model_dump()
        {"$lt": ["$age", 65]}
    """

    left: Any
    right: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $lt expression."""
        return {
            "$lt": [serialize_value(self.left), serialize_value(self.right)]
        }


class LteExpr(ExpressionBase):
    """
    $lte expression operator - tests less than or equal.

    Example:
        >>> LteExpr(left=F("age"), right=65).model_dump()
        {"$lte": ["$age", 65]}
    """

    left: Any
    right: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $lte expression."""
        return {
            "$lte": [serialize_value(self.left), serialize_value(self.right)]
        }


class CmpExpr(ExpressionBase):
    """
    $cmp expression operator - compares two values.

    Returns -1 if first < second, 0 if equal, 1 if first > second.

    Example:
        >>> CmpExpr(left=F("a"), right=F("b")).model_dump()
        {"$cmp": ["$a", "$b"]}
    """

    left: Any
    right: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $cmp expression."""
        return {
            "$cmp": [serialize_value(self.left), serialize_value(self.right)]
        }


__all__ = [
    "EqExpr",
    "NeExpr",
    "GtExpr",
    "GteExpr",
    "LtExpr",
    "LteExpr",
    "CmpExpr",
]

"""Set expression operators for MongoDB aggregation."""

from typing import Any

from pydantic import model_serializer

from mongo_aggro.base import serialize_value
from mongo_aggro.expressions.base import ExpressionBase


class SetUnionExpr(ExpressionBase):
    """
    $setUnion expression operator - returns union of arrays (unique values).

    Example:
        >>> SetUnionExpr(arrays=[F("tags1"), F("tags2")]).model_dump()
        {"$setUnion": ["$tags1", "$tags2"]}
    """

    arrays: list[Any]

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $setUnion expression."""
        return {"$setUnion": [serialize_value(a) for a in self.arrays]}


class SetIntersectionExpr(ExpressionBase):
    """
    $setIntersection expression operator - returns common elements.

    Example:
        >>> SetIntersectionExpr(arrays=[F("a"), F("b")]).model_dump()
        {"$setIntersection": ["$a", "$b"]}
    """

    arrays: list[Any]

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $setIntersection expression."""
        return {"$setIntersection": [serialize_value(a) for a in self.arrays]}


class SetDifferenceExpr(ExpressionBase):
    """
    $setDifference expression operator - returns elements in first not in second.

    Example:
        >>> SetDifferenceExpr(first=F("all"), second=F("excluded")).model_dump()
        {"$setDifference": ["$all", "$excluded"]}
    """

    first: Any
    second: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $setDifference expression."""
        return {
            "$setDifference": [
                serialize_value(self.first),
                serialize_value(self.second),
            ]
        }


class SetEqualsExpr(ExpressionBase):
    """
    $setEquals expression operator - checks if arrays have same elements.

    Example:
        >>> SetEqualsExpr(arrays=[F("a"), F("b")]).model_dump()
        {"$setEquals": ["$a", "$b"]}
    """

    arrays: list[Any]

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $setEquals expression."""
        return {"$setEquals": [serialize_value(a) for a in self.arrays]}


class SetIsSubsetExpr(ExpressionBase):
    """
    $setIsSubset expression operator - checks if first is subset of second.

    Example:
        >>> SetIsSubsetExpr(first=F("small"), second=F("large")).model_dump()
        {"$setIsSubset": ["$small", "$large"]}
    """

    first: Any
    second: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $setIsSubset expression."""
        return {
            "$setIsSubset": [
                serialize_value(self.first),
                serialize_value(self.second),
            ]
        }


class AnyElementTrueExpr(ExpressionBase):
    """
    $anyElementTrue expression operator - true if any array element is truthy.

    Example:
        >>> AnyElementTrueExpr(input=F("flags")).model_dump()
        {"$anyElementTrue": "$flags"}
    """

    input: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $anyElementTrue expression."""
        return {"$anyElementTrue": serialize_value(self.input)}


class AllElementsTrueExpr(ExpressionBase):
    """
    $allElementsTrue expression operator - true if all array elements truthy.

    Example:
        >>> AllElementsTrueExpr(input=F("conditions")).model_dump()
        {"$allElementsTrue": "$conditions"}
    """

    input: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $allElementsTrue expression."""
        return {"$allElementsTrue": serialize_value(self.input)}


__all__ = [
    "SetUnionExpr",
    "SetIntersectionExpr",
    "SetDifferenceExpr",
    "SetEqualsExpr",
    "SetIsSubsetExpr",
    "AnyElementTrueExpr",
    "AllElementsTrueExpr",
]

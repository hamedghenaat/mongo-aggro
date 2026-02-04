"""Data size expression operators for MongoDB aggregation."""

from typing import Any

from pydantic import model_serializer

from mongo_aggro.base import serialize_value
from mongo_aggro.expressions.base import ExpressionBase


class BsonSizeExpr(ExpressionBase):
    """
    $bsonSize expression operator - returns size of document in bytes.

    Example:
        >>> BsonSizeExpr(input=F("doc")).model_dump()
        {"$bsonSize": "$doc"}
    """

    input: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $bsonSize expression."""
        return {"$bsonSize": serialize_value(self.input)}


class BinarySizeExpr(ExpressionBase):
    """
    $binarySize expression operator - returns size of string/binary in bytes.

    Example:
        >>> BinarySizeExpr(input=F("data")).model_dump()
        {"$binarySize": "$data"}
    """

    input: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $binarySize expression."""
        return {"$binarySize": serialize_value(self.input)}


__all__ = [
    "BsonSizeExpr",
    "BinarySizeExpr",
]

"""Object expression operators for MongoDB aggregation."""

from typing import Any

from pydantic import model_serializer

from mongo_aggro.base import serialize_value
from mongo_aggro.expressions.base import ExpressionBase


class MergeObjectsExpr(ExpressionBase):
    """
    $mergeObjects expression operator - merges documents into one.

    Example:
        >>> MergeObjectsExpr(objects=[F("defaults"), F("overrides")]).model_dump()
        {"$mergeObjects": ["$defaults", "$overrides"]}
    """

    objects: list[Any]

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $mergeObjects expression."""
        return {"$mergeObjects": [serialize_value(o) for o in self.objects]}


class ObjectToArrayExpr(ExpressionBase):
    """
    $objectToArray expression operator - converts object to array of k/v pairs.

    Example:
        >>> ObjectToArrayExpr(input=F("doc")).model_dump()
        {"$objectToArray": "$doc"}
    """

    input: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $objectToArray expression."""
        return {"$objectToArray": serialize_value(self.input)}


class ArrayToObjectExpr(ExpressionBase):
    """
    $arrayToObject expression operator - converts array of k/v pairs to object.

    Example:
        >>> ArrayToObjectExpr(input=F("pairs")).model_dump()
        {"$arrayToObject": "$pairs"}
    """

    input: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $arrayToObject expression."""
        return {"$arrayToObject": serialize_value(self.input)}


class GetFieldExpr(ExpressionBase):
    """
    $getField expression operator - gets a field value by name.

    Example:
        >>> GetFieldExpr(field="status", input=F("doc")).model_dump()
        {"$getField": {"field": "status", "input": "$doc"}}
    """

    field: Any
    input: Any | None = None

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $getField expression."""
        if self.input is None:
            return {"$getField": serialize_value(self.field)}
        return {
            "$getField": {
                "field": serialize_value(self.field),
                "input": serialize_value(self.input),
            }
        }


class SetFieldExpr(ExpressionBase):
    """
    $setField expression operator - sets or adds a field in a document.

    Example:
        >>> SetFieldExpr(
        ...     field="status",
        ...     input=F("doc"),
        ...     value="active"
        ... ).model_dump()
        {"$setField": {"field": "status", "input": "$doc", "value": "active"}}
    """

    field: Any
    input: Any
    value: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $setField expression."""
        return {
            "$setField": {
                "field": serialize_value(self.field),
                "input": serialize_value(self.input),
                "value": serialize_value(self.value),
            }
        }


__all__ = [
    "MergeObjectsExpr",
    "ObjectToArrayExpr",
    "ArrayToObjectExpr",
    "GetFieldExpr",
    "SetFieldExpr",
]

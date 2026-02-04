"""Type conversion expression operators for MongoDB aggregation."""

from typing import Any

from pydantic import model_serializer

from mongo_aggro.base import serialize_value
from mongo_aggro.expressions.base import ExpressionBase


class ToStringExpr(ExpressionBase):
    """
    $toString expression operator - converts value to string.

    Example:
        >>> ToStringExpr(input=F("numericId")).model_dump()
        {"$toString": "$numericId"}
    """

    input: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $toString expression."""
        return {"$toString": serialize_value(self.input)}


class ToIntExpr(ExpressionBase):
    """
    $toInt expression operator - converts value to integer.

    Example:
        >>> ToIntExpr(input=F("stringNum")).model_dump()
        {"$toInt": "$stringNum"}
    """

    input: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $toInt expression."""
        return {"$toInt": serialize_value(self.input)}


class ToDoubleExpr(ExpressionBase):
    """
    $toDouble expression operator - converts value to double.

    Example:
        >>> ToDoubleExpr(input=F("intValue")).model_dump()
        {"$toDouble": "$intValue"}
    """

    input: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $toDouble expression."""
        return {"$toDouble": serialize_value(self.input)}


class ToBoolExpr(ExpressionBase):
    """
    $toBool expression operator - converts value to boolean.

    Example:
        >>> ToBoolExpr(input=F("flag")).model_dump()
        {"$toBool": "$flag"}
    """

    input: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $toBool expression."""
        return {"$toBool": serialize_value(self.input)}


class ToObjectIdExpr(ExpressionBase):
    """
    $toObjectId expression operator - converts value to ObjectId.

    Example:
        >>> ToObjectIdExpr(input=F("idString")).model_dump()
        {"$toObjectId": "$idString"}
    """

    input: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $toObjectId expression."""
        return {"$toObjectId": serialize_value(self.input)}


class ToLongExpr(ExpressionBase):
    """
    $toLong expression operator - converts value to long integer.

    Example:
        >>> ToLongExpr(input=F("value")).model_dump()
        {"$toLong": "$value"}
    """

    input: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $toLong expression."""
        return {"$toLong": serialize_value(self.input)}


class ToDecimalExpr(ExpressionBase):
    """
    $toDecimal expression operator - converts value to Decimal128.

    Example:
        >>> ToDecimalExpr(input=F("value")).model_dump()
        {"$toDecimal": "$value"}
    """

    input: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $toDecimal expression."""
        return {"$toDecimal": serialize_value(self.input)}


class ConvertExpr(ExpressionBase):
    """
    $convert expression operator - converts value to specified type.

    Example:
        >>> ConvertExpr(input=F("value"), to="int").model_dump()
        {"$convert": {"input": "$value", "to": "int"}}
    """

    input: Any
    to: str
    on_error: Any = None
    on_null: Any = None

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $convert expression."""
        result: dict[str, Any] = {
            "$convert": {
                "input": serialize_value(self.input),
                "to": self.to,
            }
        }
        if self.on_error is not None:
            result["$convert"]["onError"] = serialize_value(self.on_error)
        if self.on_null is not None:
            result["$convert"]["onNull"] = serialize_value(self.on_null)
        return result


class TypeExpr(ExpressionBase):
    """
    $type expression operator - returns BSON type of a value.

    Example:
        >>> TypeExpr(input=F("field")).model_dump()
        {"$type": "$field"}
    """

    input: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $type expression."""
        return {"$type": serialize_value(self.input)}


class IsNumberExpr(ExpressionBase):
    """
    $isNumber expression operator - checks if value is numeric.

    Example:
        >>> IsNumberExpr(input=F("value")).model_dump()
        {"$isNumber": "$value"}
    """

    input: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $isNumber expression."""
        return {"$isNumber": serialize_value(self.input)}


__all__ = [
    "ToStringExpr",
    "ToIntExpr",
    "ToDoubleExpr",
    "ToBoolExpr",
    "ToObjectIdExpr",
    "ToLongExpr",
    "ToDecimalExpr",
    "ConvertExpr",
    "TypeExpr",
    "IsNumberExpr",
]

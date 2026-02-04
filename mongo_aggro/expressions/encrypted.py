"""Encrypted string expression operators for MongoDB aggregation."""

from typing import Any

from pydantic import model_serializer

from mongo_aggro.base import serialize_value
from mongo_aggro.expressions.base import ExpressionBase


class EncStrContainsExpr(ExpressionBase):
    """
    $encStrContains expression - checks if encrypted string contains substring.

    Used with Queryable Encryption for searching encrypted fields.

    Example:
        >>> EncStrContainsExpr(input=F("encryptedField"), substring="search").model_dump()
        {"$encStrContains": {"input": "$encryptedField", "substring": "search"}}
    """

    input: Any
    substring: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $encStrContains expression."""
        return {
            "$encStrContains": {
                "input": serialize_value(self.input),
                "substring": serialize_value(self.substring),
            }
        }


class EncStrStartsWithExpr(ExpressionBase):
    """
    $encStrStartsWith expression - checks if encrypted string starts with prefix.

    Used with Queryable Encryption for searching encrypted fields.

    Example:
        >>> EncStrStartsWithExpr(input=F("encryptedField"), prefix="abc").model_dump()
        {"$encStrStartsWith": {"input": "$encryptedField", "prefix": "abc"}}
    """

    input: Any
    prefix: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $encStrStartsWith expression."""
        return {
            "$encStrStartsWith": {
                "input": serialize_value(self.input),
                "prefix": serialize_value(self.prefix),
            }
        }


class EncStrEndsWithExpr(ExpressionBase):
    """
    $encStrEndsWith expression - checks if encrypted string ends with suffix.

    Used with Queryable Encryption for searching encrypted fields.

    Example:
        >>> EncStrEndsWithExpr(input=F("encryptedField"), suffix="xyz").model_dump()
        {"$encStrEndsWith": {"input": "$encryptedField", "suffix": "xyz"}}
    """

    input: Any
    suffix: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $encStrEndsWith expression."""
        return {
            "$encStrEndsWith": {
                "input": serialize_value(self.input),
                "suffix": serialize_value(self.suffix),
            }
        }


class EncStrNormalizedEqExpr(ExpressionBase):
    """
    $encStrNormalizedEq expression - normalized equality for encrypted strings.

    Used with Queryable Encryption for case-insensitive matching.

    Example:
        >>> EncStrNormalizedEqExpr(input=F("encryptedField"), value="test").model_dump()
        {"$encStrNormalizedEq": {"input": "$encryptedField", "value": "test"}}
    """

    input: Any
    value: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $encStrNormalizedEq expression."""
        return {
            "$encStrNormalizedEq": {
                "input": serialize_value(self.input),
                "value": serialize_value(self.value),
            }
        }


__all__ = [
    "EncStrContainsExpr",
    "EncStrStartsWithExpr",
    "EncStrEndsWithExpr",
    "EncStrNormalizedEqExpr",
]

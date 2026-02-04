"""Trigonometry expression operators for MongoDB aggregation."""

from typing import Any

from pydantic import model_serializer

from mongo_aggro.base import serialize_value
from mongo_aggro.expressions.base import ExpressionBase


class SinExpr(ExpressionBase):
    """
    $sin expression operator - calculates sine.

    Example:
        >>> SinExpr(input=F("angle")).model_dump()
        {"$sin": "$angle"}
    """

    input: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $sin expression."""
        return {"$sin": serialize_value(self.input)}


class CosExpr(ExpressionBase):
    """
    $cos expression operator - calculates cosine.

    Example:
        >>> CosExpr(input=F("angle")).model_dump()
        {"$cos": "$angle"}
    """

    input: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $cos expression."""
        return {"$cos": serialize_value(self.input)}


class TanExpr(ExpressionBase):
    """
    $tan expression operator - calculates tangent.

    Example:
        >>> TanExpr(input=F("angle")).model_dump()
        {"$tan": "$angle"}
    """

    input: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $tan expression."""
        return {"$tan": serialize_value(self.input)}


class AsinExpr(ExpressionBase):
    """
    $asin expression operator - calculates arc sine.

    Example:
        >>> AsinExpr(input=F("value")).model_dump()
        {"$asin": "$value"}
    """

    input: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $asin expression."""
        return {"$asin": serialize_value(self.input)}


class AcosExpr(ExpressionBase):
    """
    $acos expression operator - calculates arc cosine.

    Example:
        >>> AcosExpr(input=F("value")).model_dump()
        {"$acos": "$value"}
    """

    input: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $acos expression."""
        return {"$acos": serialize_value(self.input)}


class AtanExpr(ExpressionBase):
    """
    $atan expression operator - calculates arc tangent.

    Example:
        >>> AtanExpr(input=F("value")).model_dump()
        {"$atan": "$value"}
    """

    input: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $atan expression."""
        return {"$atan": serialize_value(self.input)}


class Atan2Expr(ExpressionBase):
    """
    $atan2 expression operator - calculates arc tangent of y/x.

    Example:
        >>> Atan2Expr(y=F("y"), x=F("x")).model_dump()
        {"$atan2": ["$y", "$x"]}
    """

    y: Any
    x: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $atan2 expression."""
        return {"$atan2": [serialize_value(self.y), serialize_value(self.x)]}


class SinhExpr(ExpressionBase):
    """
    $sinh expression operator - calculates hyperbolic sine.

    Example:
        >>> SinhExpr(input=F("value")).model_dump()
        {"$sinh": "$value"}
    """

    input: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $sinh expression."""
        return {"$sinh": serialize_value(self.input)}


class CoshExpr(ExpressionBase):
    """
    $cosh expression operator - calculates hyperbolic cosine.

    Example:
        >>> CoshExpr(input=F("value")).model_dump()
        {"$cosh": "$value"}
    """

    input: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $cosh expression."""
        return {"$cosh": serialize_value(self.input)}


class TanhExpr(ExpressionBase):
    """
    $tanh expression operator - calculates hyperbolic tangent.

    Example:
        >>> TanhExpr(input=F("value")).model_dump()
        {"$tanh": "$value"}
    """

    input: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $tanh expression."""
        return {"$tanh": serialize_value(self.input)}


class AsinhExpr(ExpressionBase):
    """
    $asinh expression operator - calculates hyperbolic arc sine.

    Example:
        >>> AsinhExpr(input=F("value")).model_dump()
        {"$asinh": "$value"}
    """

    input: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $asinh expression."""
        return {"$asinh": serialize_value(self.input)}


class AcoshExpr(ExpressionBase):
    """
    $acosh expression operator - calculates hyperbolic arc cosine.

    Example:
        >>> AcoshExpr(input=F("value")).model_dump()
        {"$acosh": "$value"}
    """

    input: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $acosh expression."""
        return {"$acosh": serialize_value(self.input)}


class AtanhExpr(ExpressionBase):
    """
    $atanh expression operator - calculates hyperbolic arc tangent.

    Example:
        >>> AtanhExpr(input=F("value")).model_dump()
        {"$atanh": "$value"}
    """

    input: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $atanh expression."""
        return {"$atanh": serialize_value(self.input)}


class DegreesToRadiansExpr(ExpressionBase):
    """
    $degreesToRadians expression operator - converts degrees to radians.

    Example:
        >>> DegreesToRadiansExpr(input=F("degrees")).model_dump()
        {"$degreesToRadians": "$degrees"}
    """

    input: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $degreesToRadians expression."""
        return {"$degreesToRadians": serialize_value(self.input)}


class RadiansToDegreesExpr(ExpressionBase):
    """
    $radiansToDegrees expression operator - converts radians to degrees.

    Example:
        >>> RadiansToDegreesExpr(input=F("radians")).model_dump()
        {"$radiansToDegrees": "$radians"}
    """

    input: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $radiansToDegrees expression."""
        return {"$radiansToDegrees": serialize_value(self.input)}


__all__ = [
    "SinExpr",
    "CosExpr",
    "TanExpr",
    "AsinExpr",
    "AcosExpr",
    "AtanExpr",
    "Atan2Expr",
    "SinhExpr",
    "CoshExpr",
    "TanhExpr",
    "AsinhExpr",
    "AcoshExpr",
    "AtanhExpr",
    "DegreesToRadiansExpr",
    "RadiansToDegreesExpr",
]

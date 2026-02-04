"""Conditional expression operators for MongoDB aggregation."""

from typing import Any

from pydantic import BaseModel, ConfigDict, model_serializer

from mongo_aggro.base import serialize_value
from mongo_aggro.expressions.base import ExpressionBase


class CondExpr(ExpressionBase):
    """
    $cond expression operator - ternary conditional.

    Example:
        >>> CondExpr(
        ...     if_=GtExpr(left=F("qty"), right=100),
        ...     then="bulk",
        ...     else_="retail"
        ... ).model_dump()
        {"$cond": {"if": {"$gt": ["$qty", 100]}, "then": "bulk", "else": "retail"}}
    """

    if_: Any
    then: Any
    else_: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $cond expression."""
        return {
            "$cond": {
                "if": serialize_value(self.if_),
                "then": serialize_value(self.then),
                "else": serialize_value(self.else_),
            }
        }


class IfNullExpr(ExpressionBase):
    """
    $ifNull expression operator - null coalescing.

    Example:
        >>> IfNullExpr(input=F("name"), replacement="Unknown").model_dump()
        {"$ifNull": ["$name", "Unknown"]}
    """

    input: Any
    replacement: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $ifNull expression."""
        return {
            "$ifNull": [
                serialize_value(self.input),
                serialize_value(self.replacement),
            ]
        }


class SwitchBranch(BaseModel):
    """A single branch in a $switch expression."""

    model_config = ConfigDict(
        populate_by_name=True,
        extra="forbid",
    )

    case: Any
    then: Any


class SwitchExpr(ExpressionBase):
    """
    $switch expression operator - multi-branch conditional.

    Example:
        >>> SwitchExpr(
        ...     branches=[
        ...         SwitchBranch(case=EqExpr(left=F("status"), right="A"), then=1),
        ...         SwitchBranch(case=EqExpr(left=F("status"), right="B"), then=2),
        ...     ],
        ...     default=0
        ... ).model_dump()
        {"$switch": {"branches": [...], "default": 0}}
    """

    branches: list[SwitchBranch]
    default: Any = None

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $switch expression."""
        result: dict[str, Any] = {
            "$switch": {
                "branches": [
                    {
                        "case": serialize_value(b.case),
                        "then": serialize_value(b.then),
                    }
                    for b in self.branches
                ]
            }
        }
        if self.default is not None:
            result["$switch"]["default"] = serialize_value(self.default)
        return result


__all__ = [
    "CondExpr",
    "IfNullExpr",
    "SwitchBranch",
    "SwitchExpr",
]

"""Base classes for MongoDB expression operators."""

from typing import TYPE_CHECKING, Any

from pydantic import BaseModel, ConfigDict

from mongo_aggro.base import serialize_value

if TYPE_CHECKING:
    from mongo_aggro.expressions.comparison import (
        EqExpr,
        GteExpr,
        GtExpr,
        LteExpr,
        LtExpr,
        NeExpr,
    )
    from mongo_aggro.expressions.logical import AndExpr, NotExpr, OrExpr


class Field:
    """
    Field reference with Python operator overloading support.

    Enables natural Python syntax for building MongoDB expressions:
        >>> (F("status") == "active") & (F("age") > 18)

    Note: Use & instead of 'and', | instead of 'or', ~ instead of 'not'.
    Parentheses are required due to operator precedence.

    Example:
        >>> F("age") > 18
        GtExpr(left=Field("age"), right=18)

        >>> (F("status") == "active") & (F("age") > 18)
        AndExpr([EqExpr(...), GtExpr(...)])
    """

    __slots__ = ("_path",)

    def __init__(self, path: str) -> None:
        """
        Initialize a field reference.

        Args:
            path: Field path (with or without $ prefix)
        """
        self._path = path if path.startswith("$") else f"${path}"

    def __str__(self) -> str:
        """Return the field path with $ prefix."""
        return self._path

    def __repr__(self) -> str:
        """Return a string representation for debugging."""
        return f"Field({self._path!r})"

    def __hash__(self) -> int:
        """Make Field hashable."""
        return hash(self._path)

    # Comparison operators - return expression objects
    def __eq__(self, other: Any) -> "EqExpr":  # type: ignore[override]
        """Create equality expression: F("field") == value."""
        from mongo_aggro.expressions.comparison import EqExpr

        return EqExpr(left=self, right=other)

    def __ne__(self, other: Any) -> "NeExpr":  # type: ignore[override]
        """Create not-equal expression: F("field") != value."""
        from mongo_aggro.expressions.comparison import NeExpr

        return NeExpr(left=self, right=other)

    def __gt__(self, other: Any) -> "GtExpr":
        """Create greater-than expression: F("field") > value."""
        from mongo_aggro.expressions.comparison import GtExpr

        return GtExpr(left=self, right=other)

    def __ge__(self, other: Any) -> "GteExpr":
        """Create greater-than-or-equal expression: F("field") >= value."""
        from mongo_aggro.expressions.comparison import GteExpr

        return GteExpr(left=self, right=other)

    def __lt__(self, other: Any) -> "LtExpr":
        """Create less-than expression: F("field") < value."""
        from mongo_aggro.expressions.comparison import LtExpr

        return LtExpr(left=self, right=other)

    def __le__(self, other: Any) -> "LteExpr":
        """Create less-than-or-equal expression: F("field") <= value."""
        from mongo_aggro.expressions.comparison import LteExpr

        return LteExpr(left=self, right=other)


def F(path: str) -> Field:
    """
    Create a field reference with operator overloading support.

    This is the primary way to reference document fields in expressions.
    Returns a Field object that supports Python comparison operators.

    Args:
        path: Field path (e.g., "status", "user.name", "$existing_ref")

    Returns:
        Field object with operator overloading

    Example:
        >>> F("status") == "active"
        EqExpr(left=Field("$status"), right="active")

        >>> F("price") > F("cost")
        GtExpr(left=Field("$price"), right=Field("$cost"))
    """
    return Field(path)


class ExpressionBase(BaseModel):
    """
    Base class for all MongoDB expression operators.

    Provides logical operator support (&, |, ~) for combining expressions.
    All expression subclasses should inherit from this class.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        extra="forbid",
        arbitrary_types_allowed=True,
    )

    def __and__(self, other: "ExpressionBase | dict[str, Any]") -> "AndExpr":
        """
        Combine expressions with AND: expr1 & expr2.

        Automatically flattens nested ANDs for cleaner output.
        """
        from mongo_aggro.expressions.logical import AndExpr

        left = self.conditions if isinstance(self, AndExpr) else [self]
        if isinstance(other, AndExpr):
            right = other.conditions
        else:
            right = [other]
        return AndExpr(conditions=left + right)

    def __or__(self, other: "ExpressionBase | dict[str, Any]") -> "OrExpr":
        """
        Combine expressions with OR: expr1 | expr2.

        Automatically flattens nested ORs for cleaner output.
        """
        from mongo_aggro.expressions.logical import OrExpr

        left = self.conditions if isinstance(self, OrExpr) else [self]
        if isinstance(other, OrExpr):
            right = other.conditions
        else:
            right = [other]
        return OrExpr(conditions=left + right)

    def __invert__(self) -> "NotExpr":
        """Negate expression with NOT: ~expr."""
        from mongo_aggro.expressions.logical import NotExpr

        return NotExpr(condition=self)


# Re-export serialize_value for use by expression modules
__all__ = [
    "Field",
    "F",
    "ExpressionBase",
    "serialize_value",
]

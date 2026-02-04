"""Expression operators for MongoDB aggregation with operator overloading."""

from typing import Any

from pydantic import BaseModel, ConfigDict, model_serializer

from mongo_aggro.base import serialize_value


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
        return EqExpr(left=self, right=other)

    def __ne__(self, other: Any) -> "NeExpr":  # type: ignore[override]
        """Create not-equal expression: F("field") != value."""
        return NeExpr(left=self, right=other)

    def __gt__(self, other: Any) -> "GtExpr":
        """Create greater-than expression: F("field") > value."""
        return GtExpr(left=self, right=other)

    def __ge__(self, other: Any) -> "GteExpr":
        """Create greater-than-or-equal expression: F("field") >= value."""
        return GteExpr(left=self, right=other)

    def __lt__(self, other: Any) -> "LtExpr":
        """Create less-than expression: F("field") < value."""
        return LtExpr(left=self, right=other)

    def __le__(self, other: Any) -> "LteExpr":
        """Create less-than-or-equal expression: F("field") <= value."""
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
        left = self.conditions if isinstance(self, OrExpr) else [self]
        if isinstance(other, OrExpr):
            right = other.conditions
        else:
            right = [other]
        return OrExpr(conditions=left + right)

    def __invert__(self) -> "NotExpr":
        """Negate expression with NOT: ~expr."""
        return NotExpr(condition=self)


# --- Comparison Expression Operators ---


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


# --- Logical Expression Operators ---


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


# --- Arithmetic Expression Operators ---


class AddExpr(ExpressionBase):
    """
    $add expression operator - adds numbers or dates.

    Example:
        >>> AddExpr(operands=[F("price"), F("tax")]).model_dump()
        {"$add": ["$price", "$tax"]}
    """

    operands: list[Any]

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $add expression."""
        return {"$add": [serialize_value(o) for o in self.operands]}


class SubtractExpr(ExpressionBase):
    """
    $subtract expression operator - subtracts two numbers or dates.

    Example:
        >>> SubtractExpr(left=F("total"), right=F("discount")).model_dump()
        {"$subtract": ["$total", "$discount"]}
    """

    left: Any
    right: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $subtract expression."""
        return {"$subtract": [serialize_value(self.left), serialize_value(self.right)]}


class MultiplyExpr(ExpressionBase):
    """
    $multiply expression operator - multiplies numbers.

    Example:
        >>> MultiplyExpr(operands=[F("price"), F("qty")]).model_dump()
        {"$multiply": ["$price", "$qty"]}
    """

    operands: list[Any]

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $multiply expression."""
        return {"$multiply": [serialize_value(o) for o in self.operands]}


class DivideExpr(ExpressionBase):
    """
    $divide expression operator - divides two numbers.

    Example:
        >>> DivideExpr(dividend=F("total"), divisor=F("count")).model_dump()
        {"$divide": ["$total", "$count"]}
    """

    dividend: Any
    divisor: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $divide expression."""
        return {
            "$divide": [serialize_value(self.dividend), serialize_value(self.divisor)]
        }


class AbsExpr(ExpressionBase):
    """
    $abs expression operator - returns absolute value.

    Example:
        >>> AbsExpr(value=F("balance")).model_dump()
        {"$abs": "$balance"}
    """

    value: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $abs expression."""
        return {"$abs": serialize_value(self.value)}


class ModExpr(ExpressionBase):
    """
    $mod expression operator - returns remainder of division.

    Example:
        >>> ModExpr(dividend=F("num"), divisor=2).model_dump()
        {"$mod": ["$num", 2]}
    """

    dividend: Any
    divisor: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $mod expression."""
        return {
            "$mod": [serialize_value(self.dividend), serialize_value(self.divisor)]
        }


# --- Conditional Expression Operators ---


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
            "$ifNull": [serialize_value(self.input), serialize_value(self.replacement)]
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


# --- String Expression Operators ---


class ConcatExpr(ExpressionBase):
    """
    $concat expression operator - concatenates strings.

    Example:
        >>> ConcatExpr(strings=[F("first"), " ", F("last")]).model_dump()
        {"$concat": ["$first", " ", "$last"]}
    """

    strings: list[Any]

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $concat expression."""
        return {"$concat": [serialize_value(s) for s in self.strings]}


class SplitExpr(ExpressionBase):
    """
    $split expression operator - splits string by delimiter.

    Example:
        >>> SplitExpr(input=F("fullName"), delimiter=" ").model_dump()
        {"$split": ["$fullName", " "]}
    """

    input: Any
    delimiter: str

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $split expression."""
        return {"$split": [serialize_value(self.input), self.delimiter]}


class ToLowerExpr(ExpressionBase):
    """
    $toLower expression operator - converts to lowercase.

    Example:
        >>> ToLowerExpr(input=F("name")).model_dump()
        {"$toLower": "$name"}
    """

    input: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $toLower expression."""
        return {"$toLower": serialize_value(self.input)}


class ToUpperExpr(ExpressionBase):
    """
    $toUpper expression operator - converts to uppercase.

    Example:
        >>> ToUpperExpr(input=F("name")).model_dump()
        {"$toUpper": "$name"}
    """

    input: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $toUpper expression."""
        return {"$toUpper": serialize_value(self.input)}


# --- Array Expression Operators ---


class ArraySizeExpr(ExpressionBase):
    """
    $size expression operator - returns array length.

    Example:
        >>> ArraySizeExpr(array=F("items")).model_dump()
        {"$size": "$items"}
    """

    array: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $size expression."""
        return {"$size": serialize_value(self.array)}


class SliceExpr(ExpressionBase):
    """
    $slice expression operator - returns subset of array.

    Example:
        >>> SliceExpr(array=F("items"), n=5).model_dump()
        {"$slice": ["$items", 5]}

        >>> SliceExpr(array=F("items"), position=2, n=3).model_dump()
        {"$slice": ["$items", 2, 3]}
    """

    array: Any
    n: int
    position: int | None = None

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $slice expression."""
        if self.position is not None:
            return {"$slice": [serialize_value(self.array), self.position, self.n]}
        return {"$slice": [serialize_value(self.array), self.n]}


class FilterExpr(ExpressionBase):
    """
    $filter expression operator - filters array elements.

    Example:
        >>> FilterExpr(
        ...     input=F("items"),
        ...     as_="item",
        ...     cond=GteExpr(left=Field("$$item.price"), right=100)
        ... ).model_dump()
        {"$filter": {"input": "$items", "as": "item", "cond": {...}}}
    """

    input: Any
    cond: Any
    as_: str = "this"
    limit: int | None = None

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $filter expression."""
        result: dict[str, Any] = {
            "$filter": {
                "input": serialize_value(self.input),
                "as": self.as_,
                "cond": serialize_value(self.cond),
            }
        }
        if self.limit is not None:
            result["$filter"]["limit"] = self.limit
        return result


class MapExpr(ExpressionBase):
    """
    $map expression operator - applies expression to each array element.

    Example:
        >>> MapExpr(
        ...     input=F("items"),
        ...     as_="item",
        ...     in_=MultiplyExpr(operands=[Field("$$item.price"), 1.1])
        ... ).model_dump()
        {"$map": {"input": "$items", "as": "item", "in": {...}}}
    """

    input: Any
    in_: Any
    as_: str = "this"

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $map expression."""
        return {
            "$map": {
                "input": serialize_value(self.input),
                "as": self.as_,
                "in": serialize_value(self.in_),
            }
        }


class ReduceExpr(ExpressionBase):
    """
    $reduce expression operator - reduces array to single value.

    Example:
        >>> ReduceExpr(
        ...     input=F("items"),
        ...     initial_value=0,
        ...     in_=AddExpr(operands=[Field("$$value"), Field("$$this.qty")])
        ... ).model_dump()
        {"$reduce": {"input": "$items", "initialValue": 0, "in": {...}}}
    """

    input: Any
    initial_value: Any
    in_: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $reduce expression."""
        return {
            "$reduce": {
                "input": serialize_value(self.input),
                "initialValue": serialize_value(self.initial_value),
                "in": serialize_value(self.in_),
            }
        }

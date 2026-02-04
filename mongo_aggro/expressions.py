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


# --- Date Expression Operators ---


class DateAddExpr(ExpressionBase):
    """
    $dateAdd expression operator - adds time to a date.

    Example:
        >>> DateAddExpr(
        ...     start_date=F("orderDate"),
        ...     unit="day",
        ...     amount=7
        ... ).model_dump()
        {"$dateAdd": {"startDate": "$orderDate", "unit": "day", "amount": 7}}
    """

    start_date: Any
    unit: str
    amount: Any
    timezone: str | None = None

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $dateAdd expression."""
        result: dict[str, Any] = {
            "$dateAdd": {
                "startDate": serialize_value(self.start_date),
                "unit": self.unit,
                "amount": serialize_value(self.amount),
            }
        }
        if self.timezone:
            result["$dateAdd"]["timezone"] = self.timezone
        return result


class DateSubtractExpr(ExpressionBase):
    """
    $dateSubtract expression operator - subtracts time from a date.

    Example:
        >>> DateSubtractExpr(
        ...     start_date=F("endDate"),
        ...     unit="month",
        ...     amount=1
        ... ).model_dump()
        {"$dateSubtract": {"startDate": "$endDate", "unit": "month", "amount": 1}}
    """

    start_date: Any
    unit: str
    amount: Any
    timezone: str | None = None

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $dateSubtract expression."""
        result: dict[str, Any] = {
            "$dateSubtract": {
                "startDate": serialize_value(self.start_date),
                "unit": self.unit,
                "amount": serialize_value(self.amount),
            }
        }
        if self.timezone:
            result["$dateSubtract"]["timezone"] = self.timezone
        return result


class DateDiffExpr(ExpressionBase):
    """
    $dateDiff expression operator - calculates difference between dates.

    Example:
        >>> DateDiffExpr(
        ...     start_date=F("start"),
        ...     end_date=F("end"),
        ...     unit="day"
        ... ).model_dump()
        {"$dateDiff": {"startDate": "$start", "endDate": "$end", "unit": "day"}}
    """

    start_date: Any
    end_date: Any
    unit: str
    timezone: str | None = None
    start_of_week: str | None = None

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $dateDiff expression."""
        result: dict[str, Any] = {
            "$dateDiff": {
                "startDate": serialize_value(self.start_date),
                "endDate": serialize_value(self.end_date),
                "unit": self.unit,
            }
        }
        if self.timezone:
            result["$dateDiff"]["timezone"] = self.timezone
        if self.start_of_week:
            result["$dateDiff"]["startOfWeek"] = self.start_of_week
        return result


class DateToStringExpr(ExpressionBase):
    """
    $dateToString expression operator - converts date to string.

    Example:
        >>> DateToStringExpr(
        ...     date=F("orderDate"),
        ...     format="%Y-%m-%d"
        ... ).model_dump()
        {"$dateToString": {"date": "$orderDate", "format": "%Y-%m-%d"}}
    """

    date: Any
    format: str | None = None
    timezone: str | None = None
    on_null: Any = None

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $dateToString expression."""
        result: dict[str, Any] = {
            "$dateToString": {
                "date": serialize_value(self.date),
            }
        }
        if self.format:
            result["$dateToString"]["format"] = self.format
        if self.timezone:
            result["$dateToString"]["timezone"] = self.timezone
        if self.on_null is not None:
            result["$dateToString"]["onNull"] = serialize_value(self.on_null)
        return result


class DateFromStringExpr(ExpressionBase):
    """
    $dateFromString expression operator - parses string to date.

    Example:
        >>> DateFromStringExpr(
        ...     date_string=F("dateStr"),
        ...     format="%Y-%m-%d"
        ... ).model_dump()
        {"$dateFromString": {"dateString": "$dateStr", "format": "%Y-%m-%d"}}
    """

    date_string: Any
    format: str | None = None
    timezone: str | None = None
    on_error: Any = None
    on_null: Any = None

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $dateFromString expression."""
        result: dict[str, Any] = {
            "$dateFromString": {
                "dateString": serialize_value(self.date_string),
            }
        }
        if self.format:
            result["$dateFromString"]["format"] = self.format
        if self.timezone:
            result["$dateFromString"]["timezone"] = self.timezone
        if self.on_error is not None:
            result["$dateFromString"]["onError"] = serialize_value(self.on_error)
        if self.on_null is not None:
            result["$dateFromString"]["onNull"] = serialize_value(self.on_null)
        return result


# --- Type Conversion Expression Operators ---


class ToDateExpr(ExpressionBase):
    """
    $toDate expression operator - converts value to date.

    Example:
        >>> ToDateExpr(input=F("dateString")).model_dump()
        {"$toDate": "$dateString"}
    """

    input: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $toDate expression."""
        return {"$toDate": serialize_value(self.input)}


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


# --- Set Expression Operators ---


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


# --- Object Expression Operators ---


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


# --- Variable Expression Operators ---


class LetExpr(ExpressionBase):
    """
    $let expression operator - defines variables for use in expression.

    Example:
        >>> LetExpr(
        ...     vars={"total": MultiplyExpr(operands=[F("price"), F("qty")])},
        ...     in_=GtExpr(left=Field("$$total"), right=100)
        ... ).model_dump()
        {"$let": {"vars": {"total": {...}}, "in": {...}}}
    """

    vars: dict[str, Any]
    in_: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $let expression."""
        return {
            "$let": {
                "vars": {k: serialize_value(v) for k, v in self.vars.items()},
                "in": serialize_value(self.in_),
            }
        }


# --- Miscellaneous Expression Operators ---


class LiteralExpr(ExpressionBase):
    """
    $literal expression operator - returns value without parsing.

    Example:
        >>> LiteralExpr(value="$field").model_dump()
        {"$literal": "$field"}
    """

    value: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $literal expression."""
        return {"$literal": self.value}


class RandExpr(ExpressionBase):
    """
    $rand expression operator - returns random float between 0 and 1.

    Example:
        >>> RandExpr().model_dump()
        {"$rand": {}}
    """

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $rand expression."""
        return {"$rand": {}}


# --- Additional Array Expression Operators ---


class ArrayElemAtExpr(ExpressionBase):
    """
    $arrayElemAt expression operator - gets element at array index.

    Example:
        >>> ArrayElemAtExpr(array=F("items"), index=0).model_dump()
        {"$arrayElemAt": ["$items", 0]}
    """

    array: Any
    index: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $arrayElemAt expression."""
        return {
            "$arrayElemAt": [
                serialize_value(self.array),
                serialize_value(self.index),
            ]
        }


class ConcatArraysExpr(ExpressionBase):
    """
    $concatArrays expression operator - concatenates arrays.

    Example:
        >>> ConcatArraysExpr(arrays=[F("arr1"), F("arr2")]).model_dump()
        {"$concatArrays": ["$arr1", "$arr2"]}
    """

    arrays: list[Any]

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $concatArrays expression."""
        return {"$concatArrays": [serialize_value(a) for a in self.arrays]}


class InArrayExpr(ExpressionBase):
    """
    $in expression operator - checks if value is in array.

    Example:
        >>> InArrayExpr(value="admin", array=F("roles")).model_dump()
        {"$in": ["admin", "$roles"]}
    """

    value: Any
    array: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $in expression."""
        return {
            "$in": [serialize_value(self.value), serialize_value(self.array)]
        }


class IndexOfArrayExpr(ExpressionBase):
    """
    $indexOfArray expression operator - finds index of value in array.

    Example:
        >>> IndexOfArrayExpr(array=F("items"), value="target").model_dump()
        {"$indexOfArray": ["$items", "target"]}
    """

    array: Any
    value: Any
    start: int | None = None
    end: int | None = None

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $indexOfArray expression."""
        args: list[Any] = [
            serialize_value(self.array),
            serialize_value(self.value),
        ]
        if self.start is not None:
            args.append(self.start)
            if self.end is not None:
                args.append(self.end)
        return {"$indexOfArray": args}


class IsArrayExpr(ExpressionBase):
    """
    $isArray expression operator - checks if value is an array.

    Example:
        >>> IsArrayExpr(input=F("field")).model_dump()
        {"$isArray": "$field"}
    """

    input: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $isArray expression."""
        return {"$isArray": serialize_value(self.input)}


class ReverseArrayExpr(ExpressionBase):
    """
    $reverseArray expression operator - reverses array elements.

    Example:
        >>> ReverseArrayExpr(input=F("items")).model_dump()
        {"$reverseArray": "$items"}
    """

    input: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $reverseArray expression."""
        return {"$reverseArray": serialize_value(self.input)}


class SortArrayExpr(ExpressionBase):
    """
    $sortArray expression operator - sorts array elements.

    Example:
        >>> SortArrayExpr(input=F("scores"), sort_by={"score": -1}).model_dump()
        {"$sortArray": {"input": "$scores", "sortBy": {"score": -1}}}
    """

    input: Any
    sort_by: dict[str, int] | int

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $sortArray expression."""
        return {
            "$sortArray": {
                "input": serialize_value(self.input),
                "sortBy": self.sort_by,
            }
        }


class RangeExpr(ExpressionBase):
    """
    $range expression operator - generates sequence of numbers.

    Example:
        >>> RangeExpr(start=0, end=10, step=2).model_dump()
        {"$range": [0, 10, 2]}
    """

    start: Any
    end: Any
    step: Any = 1

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $range expression."""
        return {
            "$range": [
                serialize_value(self.start),
                serialize_value(self.end),
                serialize_value(self.step),
            ]
        }


class FirstNExpr(ExpressionBase):
    """
    $firstN expression operator - returns first N elements of array.

    Example:
        >>> FirstNExpr(input=F("items"), n=3).model_dump()
        {"$firstN": {"input": "$items", "n": 3}}
    """

    input: Any
    n: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $firstN expression."""
        return {
            "$firstN": {
                "input": serialize_value(self.input),
                "n": serialize_value(self.n),
            }
        }


class LastNExpr(ExpressionBase):
    """
    $lastN expression operator - returns last N elements of array.

    Example:
        >>> LastNExpr(input=F("items"), n=3).model_dump()
        {"$lastN": {"input": "$items", "n": 3}}
    """

    input: Any
    n: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $lastN expression."""
        return {
            "$lastN": {
                "input": serialize_value(self.input),
                "n": serialize_value(self.n),
            }
        }


class MaxNExpr(ExpressionBase):
    """
    $maxN expression operator - returns N largest values from array.

    Example:
        >>> MaxNExpr(input=F("scores"), n=3).model_dump()
        {"$maxN": {"input": "$scores", "n": 3}}
    """

    input: Any
    n: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $maxN expression."""
        return {
            "$maxN": {
                "input": serialize_value(self.input),
                "n": serialize_value(self.n),
            }
        }


class MinNExpr(ExpressionBase):
    """
    $minN expression operator - returns N smallest values from array.

    Example:
        >>> MinNExpr(input=F("scores"), n=3).model_dump()
        {"$minN": {"input": "$scores", "n": 3}}
    """

    input: Any
    n: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $minN expression."""
        return {
            "$minN": {
                "input": serialize_value(self.input),
                "n": serialize_value(self.n),
            }
        }


# --- Additional String Expression Operators ---


class TrimExpr(ExpressionBase):
    """
    $trim expression operator - trims whitespace from both ends.

    Example:
        >>> TrimExpr(input=F("text")).model_dump()
        {"$trim": {"input": "$text"}}
    """

    input: Any
    chars: str | None = None

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $trim expression."""
        result: dict[str, Any] = {"$trim": {"input": serialize_value(self.input)}}
        if self.chars is not None:
            result["$trim"]["chars"] = self.chars
        return result


class LTrimExpr(ExpressionBase):
    """
    $ltrim expression operator - trims whitespace from left.

    Example:
        >>> LTrimExpr(input=F("text")).model_dump()
        {"$ltrim": {"input": "$text"}}
    """

    input: Any
    chars: str | None = None

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $ltrim expression."""
        result: dict[str, Any] = {"$ltrim": {"input": serialize_value(self.input)}}
        if self.chars is not None:
            result["$ltrim"]["chars"] = self.chars
        return result


class RTrimExpr(ExpressionBase):
    """
    $rtrim expression operator - trims whitespace from right.

    Example:
        >>> RTrimExpr(input=F("text")).model_dump()
        {"$rtrim": {"input": "$text"}}
    """

    input: Any
    chars: str | None = None

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $rtrim expression."""
        result: dict[str, Any] = {"$rtrim": {"input": serialize_value(self.input)}}
        if self.chars is not None:
            result["$rtrim"]["chars"] = self.chars
        return result


class ReplaceOneExpr(ExpressionBase):
    """
    $replaceOne expression operator - replaces first occurrence.

    Example:
        >>> ReplaceOneExpr(
        ...     input=F("text"),
        ...     find="old",
        ...     replacement="new"
        ... ).model_dump()
        {"$replaceOne": {"input": "$text", "find": "old", "replacement": "new"}}
    """

    input: Any
    find: Any
    replacement: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $replaceOne expression."""
        return {
            "$replaceOne": {
                "input": serialize_value(self.input),
                "find": serialize_value(self.find),
                "replacement": serialize_value(self.replacement),
            }
        }


class ReplaceAllExpr(ExpressionBase):
    """
    $replaceAll expression operator - replaces all occurrences.

    Example:
        >>> ReplaceAllExpr(
        ...     input=F("text"),
        ...     find="old",
        ...     replacement="new"
        ... ).model_dump()
        {"$replaceAll": {"input": "$text", "find": "old", "replacement": "new"}}
    """

    input: Any
    find: Any
    replacement: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $replaceAll expression."""
        return {
            "$replaceAll": {
                "input": serialize_value(self.input),
                "find": serialize_value(self.find),
                "replacement": serialize_value(self.replacement),
            }
        }


class RegexMatchExpr(ExpressionBase):
    """
    $regexMatch expression operator - tests if string matches regex.

    Example:
        >>> RegexMatchExpr(input=F("email"), regex=r"@.*\\.com$").model_dump()
        {"$regexMatch": {"input": "$email", "regex": "@.*\\\\.com$"}}
    """

    input: Any
    regex: str
    options: str | None = None

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $regexMatch expression."""
        result: dict[str, Any] = {
            "$regexMatch": {
                "input": serialize_value(self.input),
                "regex": self.regex,
            }
        }
        if self.options is not None:
            result["$regexMatch"]["options"] = self.options
        return result


class RegexFindExpr(ExpressionBase):
    """
    $regexFind expression operator - finds first regex match.

    Example:
        >>> RegexFindExpr(input=F("text"), regex=r"\\d+").model_dump()
        {"$regexFind": {"input": "$text", "regex": "\\\\d+"}}
    """

    input: Any
    regex: str
    options: str | None = None

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $regexFind expression."""
        result: dict[str, Any] = {
            "$regexFind": {
                "input": serialize_value(self.input),
                "regex": self.regex,
            }
        }
        if self.options is not None:
            result["$regexFind"]["options"] = self.options
        return result


class RegexFindAllExpr(ExpressionBase):
    """
    $regexFindAll expression operator - finds all regex matches.

    Example:
        >>> RegexFindAllExpr(input=F("text"), regex=r"\\w+").model_dump()
        {"$regexFindAll": {"input": "$text", "regex": "\\\\w+"}}
    """

    input: Any
    regex: str
    options: str | None = None

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $regexFindAll expression."""
        result: dict[str, Any] = {
            "$regexFindAll": {
                "input": serialize_value(self.input),
                "regex": self.regex,
            }
        }
        if self.options is not None:
            result["$regexFindAll"]["options"] = self.options
        return result


class SubstrCPExpr(ExpressionBase):
    """
    $substrCP expression operator - substring by code points.

    Example:
        >>> SubstrCPExpr(input=F("text"), start=0, length=5).model_dump()
        {"$substrCP": ["$text", 0, 5]}
    """

    input: Any
    start: int
    length: int

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $substrCP expression."""
        return {
            "$substrCP": [serialize_value(self.input), self.start, self.length]
        }


class StrLenCPExpr(ExpressionBase):
    """
    $strLenCP expression operator - string length in code points.

    Example:
        >>> StrLenCPExpr(input=F("text")).model_dump()
        {"$strLenCP": "$text"}
    """

    input: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $strLenCP expression."""
        return {"$strLenCP": serialize_value(self.input)}


class StrCaseCmpExpr(ExpressionBase):
    """
    $strcasecmp expression operator - case-insensitive string comparison.

    Example:
        >>> StrCaseCmpExpr(first=F("a"), second=F("b")).model_dump()
        {"$strcasecmp": ["$a", "$b"]}
    """

    first: Any
    second: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $strcasecmp expression."""
        return {
            "$strcasecmp": [
                serialize_value(self.first),
                serialize_value(self.second),
            ]
        }


# --- Additional Arithmetic Expression Operators ---


class CeilExpr(ExpressionBase):
    """
    $ceil expression operator - rounds up to nearest integer.

    Example:
        >>> CeilExpr(input=F("value")).model_dump()
        {"$ceil": "$value"}
    """

    input: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $ceil expression."""
        return {"$ceil": serialize_value(self.input)}


class FloorExpr(ExpressionBase):
    """
    $floor expression operator - rounds down to nearest integer.

    Example:
        >>> FloorExpr(input=F("value")).model_dump()
        {"$floor": "$value"}
    """

    input: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $floor expression."""
        return {"$floor": serialize_value(self.input)}


class RoundExpr(ExpressionBase):
    """
    $round expression operator - rounds to specified decimal place.

    Example:
        >>> RoundExpr(input=F("value"), place=2).model_dump()
        {"$round": ["$value", 2]}
    """

    input: Any
    place: int = 0

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $round expression."""
        return {"$round": [serialize_value(self.input), self.place]}


class TruncExpr(ExpressionBase):
    """
    $trunc expression operator - truncates to specified decimal place.

    Example:
        >>> TruncExpr(input=F("value"), place=2).model_dump()
        {"$trunc": ["$value", 2]}
    """

    input: Any
    place: int = 0

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $trunc expression."""
        return {"$trunc": [serialize_value(self.input), self.place]}


class SqrtExpr(ExpressionBase):
    """
    $sqrt expression operator - calculates square root.

    Example:
        >>> SqrtExpr(input=F("value")).model_dump()
        {"$sqrt": "$value"}
    """

    input: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $sqrt expression."""
        return {"$sqrt": serialize_value(self.input)}


class PowExpr(ExpressionBase):
    """
    $pow expression operator - raises number to exponent.

    Example:
        >>> PowExpr(base=F("value"), exponent=2).model_dump()
        {"$pow": ["$value", 2]}
    """

    base: Any
    exponent: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $pow expression."""
        return {
            "$pow": [
                serialize_value(self.base),
                serialize_value(self.exponent),
            ]
        }


class ExpExpr(ExpressionBase):
    """
    $exp expression operator - raises e to the specified exponent.

    Example:
        >>> ExpExpr(input=F("value")).model_dump()
        {"$exp": "$value"}
    """

    input: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $exp expression."""
        return {"$exp": serialize_value(self.input)}


class LnExpr(ExpressionBase):
    """
    $ln expression operator - calculates natural logarithm.

    Example:
        >>> LnExpr(input=F("value")).model_dump()
        {"$ln": "$value"}
    """

    input: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $ln expression."""
        return {"$ln": serialize_value(self.input)}


class Log10Expr(ExpressionBase):
    """
    $log10 expression operator - calculates log base 10.

    Example:
        >>> Log10Expr(input=F("value")).model_dump()
        {"$log10": "$value"}
    """

    input: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $log10 expression."""
        return {"$log10": serialize_value(self.input)}


class LogExpr(ExpressionBase):
    """
    $log expression operator - calculates log with specified base.

    Example:
        >>> LogExpr(input=F("value"), base=2).model_dump()
        {"$log": ["$value", 2]}
    """

    input: Any
    base: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $log expression."""
        return {
            "$log": [serialize_value(self.input), serialize_value(self.base)]
        }


# --- Additional Type Expression Operators ---


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

"""Array expression operators for MongoDB aggregation."""

from typing import Any

from pydantic import model_serializer

from mongo_aggro.base import serialize_value
from mongo_aggro.expressions.base import ExpressionBase


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
            return {
                "$slice": [serialize_value(self.array), self.position, self.n]
            }
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


__all__ = [
    "ArraySizeExpr",
    "SliceExpr",
    "FilterExpr",
    "MapExpr",
    "ReduceExpr",
    "ArrayElemAtExpr",
    "ConcatArraysExpr",
    "InArrayExpr",
    "IndexOfArrayExpr",
    "IsArrayExpr",
    "ReverseArrayExpr",
    "SortArrayExpr",
    "RangeExpr",
    "FirstNExpr",
    "LastNExpr",
    "MaxNExpr",
    "MinNExpr",
]

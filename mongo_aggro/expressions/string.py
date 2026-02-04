"""String expression operators for MongoDB aggregation."""

from typing import Any

from pydantic import model_serializer

from mongo_aggro.base import serialize_value
from mongo_aggro.expressions.base import ExpressionBase


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
        result: dict[str, Any] = {
            "$trim": {"input": serialize_value(self.input)}
        }
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
        result: dict[str, Any] = {
            "$ltrim": {"input": serialize_value(self.input)}
        }
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
        result: dict[str, Any] = {
            "$rtrim": {"input": serialize_value(self.input)}
        }
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


__all__ = [
    "ConcatExpr",
    "SplitExpr",
    "ToLowerExpr",
    "ToUpperExpr",
    "TrimExpr",
    "LTrimExpr",
    "RTrimExpr",
    "ReplaceOneExpr",
    "ReplaceAllExpr",
    "RegexMatchExpr",
    "RegexFindExpr",
    "RegexFindAllExpr",
    "SubstrCPExpr",
    "StrLenCPExpr",
    "StrCaseCmpExpr",
]

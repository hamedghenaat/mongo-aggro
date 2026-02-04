"""Miscellaneous query operators for MongoDB aggregation."""

from typing import Any

from pydantic import Field

from mongo_aggro.operators.base import QueryOperator


class Mod(QueryOperator):
    """
    $mod operator - matches where field % divisor == remainder.

    Example:
        >>> Mod(divisor=4, remainder=0).model_dump()
        {"$mod": [4, 0]}
    """

    divisor: int = Field(..., description="The divisor value")
    remainder: int = Field(..., description="The remainder value")

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return {"$mod": [self.divisor, self.remainder]}


class JsonSchema(QueryOperator):
    """
    $jsonSchema operator - validates documents against JSON Schema.

    Example:
        >>> JsonSchema(json_schema={
        ...     "bsonType": "object",
        ...     "required": ["name", "email"],
        ...     "properties": {
        ...         "name": {"bsonType": "string"},
        ...         "email": {"bsonType": "string"}
        ...     }
        ... }).model_dump()
        {"$jsonSchema": {...}}
    """

    json_schema: dict[str, Any] = Field(
        ..., description="JSON Schema document"
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return {"$jsonSchema": self.json_schema}


class Where(QueryOperator):
    """
    $where operator - matches using JavaScript expression.

    Note: $where is slow and should be avoided when possible.

    Example:
        >>> Where(expression="this.credits == this.debits").model_dump()
        {"$where": "this.credits == this.debits"}
    """

    expression: str = Field(..., description="JavaScript expression string")

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return {"$where": self.expression}


class Text(QueryOperator):
    """
    $text operator - performs text search on indexed fields.

    Example:
        >>> Text(search="coffee shop", language="en").model_dump()
        {"$text": {"$search": "coffee shop", "$language": "en"}}
    """

    search: str = Field(..., description="Text to search for")
    language: str | None = Field(
        default=None, description="Language for text search"
    )
    case_sensitive: bool | None = Field(
        default=None,
        serialization_alias="$caseSensitive",
        description="Enable case sensitivity",
    )
    diacritic_sensitive: bool | None = Field(
        default=None,
        serialization_alias="$diacriticSensitive",
        description="Enable diacritic sensitivity",
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        result: dict[str, Any] = {"$search": self.search}
        if self.language is not None:
            result["$language"] = self.language
        if self.case_sensitive is not None:
            result["$caseSensitive"] = self.case_sensitive
        if self.diacritic_sensitive is not None:
            result["$diacriticSensitive"] = self.diacritic_sensitive
        return {"$text": result}


__all__ = ["Mod", "JsonSchema", "Where", "Text"]

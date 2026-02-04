"""Element query operators for MongoDB aggregation."""

from typing import Any

from pydantic import Field

from mongo_aggro.operators.base import QueryOperator


class Exists(QueryOperator):
    """$exists operator - matches documents where field exists/doesn't."""

    exists: bool = Field(
        default=True, description="True if field should exist"
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return {"$exists": self.exists}


class Type(QueryOperator):
    """$type operator - matches documents where field is of specified type."""

    bson_type: str | int | list[str | int] = Field(
        ..., description="BSON type(s) to match"
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return {"$type": self.bson_type}


__all__ = ["Exists", "Type"]

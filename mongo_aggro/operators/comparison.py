"""Comparison query operators for MongoDB aggregation."""

from typing import Any

from pydantic import Field

from mongo_aggro.operators.base import QueryOperator


class Eq(QueryOperator):
    """$eq comparison operator."""

    value: Any = Field(..., description="Value to compare")

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return {"$eq": self.value}


class Ne(QueryOperator):
    """$ne (not equal) comparison operator."""

    value: Any = Field(..., description="Value to compare")

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return {"$ne": self.value}


class Gt(QueryOperator):
    """$gt (greater than) comparison operator."""

    value: Any = Field(..., description="Value to compare")

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return {"$gt": self.value}


class Gte(QueryOperator):
    """$gte (greater than or equal) comparison operator."""

    value: Any = Field(..., description="Value to compare")

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return {"$gte": self.value}


class Lt(QueryOperator):
    """$lt (less than) comparison operator."""

    value: Any = Field(..., description="Value to compare")

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return {"$lt": self.value}


class Lte(QueryOperator):
    """$lte (less than or equal) comparison operator."""

    value: Any = Field(..., description="Value to compare")

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return {"$lte": self.value}


class In(QueryOperator):
    """$in operator - matches any value in the array."""

    values: list[Any] = Field(..., description="List of values to match")

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return {"$in": self.values}


class Nin(QueryOperator):
    """$nin operator - matches none of the values in the array."""

    values: list[Any] = Field(..., description="List of values to exclude")

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return {"$nin": self.values}


__all__ = ["Eq", "Ne", "Gt", "Gte", "Lt", "Lte", "In", "Nin"]

"""Array query operators for MongoDB aggregation."""

from typing import Any

from pydantic import Field

from mongo_aggro.operators.base import QueryOperator


class ElemMatch(QueryOperator):
    """$elemMatch operator - matches array elements."""

    conditions: dict[str, Any] = Field(
        ..., description="Conditions for array elements"
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return {"$elemMatch": self.conditions}


class Size(QueryOperator):
    """$size operator - matches arrays with specific length."""

    size: int = Field(..., description="Array size to match")

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return {"$size": self.size}


class All(QueryOperator):
    """$all operator - matches arrays containing all specified elements."""

    values: list[Any] = Field(
        ..., description="Values that must all be present"
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return {"$all": self.values}


__all__ = ["ElemMatch", "Size", "All"]

"""Regex query operators for MongoDB aggregation."""

from typing import Any

from pydantic import Field

from mongo_aggro.operators.base import QueryOperator


class Regex(QueryOperator):
    """$regex operator for pattern matching."""

    pattern: str = Field(..., description="Regular expression pattern")
    options: str | None = Field(
        default=None, description="Regex options (i, m, x, s)"
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        result: dict[str, Any] = {"$regex": self.pattern}
        if self.options:
            result["$options"] = self.options
        return result


__all__ = ["Regex"]

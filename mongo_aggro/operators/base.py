"""Base class and utilities for MongoDB query operators."""

from pydantic import BaseModel, ConfigDict


class QueryOperator(BaseModel):
    """Base class for query operators used in $match and other stages."""

    model_config = ConfigDict(
        populate_by_name=True,
        extra="forbid",
    )


__all__ = ["QueryOperator"]

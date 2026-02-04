"""Window function MongoDB aggregation pipeline stages.

This module contains stages for window operations and data filling:
SetWindowFields, Densify, and Fill.
"""

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class SetWindowFields(BaseModel):
    """
    $setWindowFields stage - performs window calculations.

    Example:
        >>> SetWindowFields(
        ...     partition_by="$state",
        ...     sort_by={"date": 1},
        ...     output={
        ...         "cumulative": {
        ...             "$sum": "$quantity",
        ...             "window": {"documents": ["unbounded", "current"]}
        ...         }
        ...     }
        ... ).model_dump()
    """

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    partition_by: str | dict[str, Any] | None = Field(
        default=None,
        validation_alias="partitionBy",
        serialization_alias="partitionBy",
        description="Partitioning expression",
    )
    sort_by: dict[str, Literal[-1, 1]] | None = Field(
        default=None,
        validation_alias="sortBy",
        serialization_alias="sortBy",
        description="Sort specification",
    )
    output: dict[str, Any] = Field(
        ..., description="Output field specifications"
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        result: dict[str, Any] = {"output": self.output}
        if self.partition_by is not None:
            result["partitionBy"] = self.partition_by
        if self.sort_by is not None:
            result["sortBy"] = self.sort_by
        return {"$setWindowFields": result}


class Densify(BaseModel):
    """
    $densify stage - fills gaps in data.

    Example:
        >>> Densify(
        ...     field="date",
        ...     range={"step": 1, "unit": "day", "bounds": "full"},
        ...     partition_by_fields=["series"]
        ... ).model_dump()
    """

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    field: str = Field(..., description="Field to densify")
    range: dict[str, Any] = Field(..., description="Range specification")
    partition_by_fields: list[str] | None = Field(
        default=None,
        validation_alias="partitionByFields",
        serialization_alias="partitionByFields",
        description="Fields to partition by",
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        result: dict[str, Any] = {"field": self.field, "range": self.range}
        if self.partition_by_fields is not None:
            result["partitionByFields"] = self.partition_by_fields
        return {"$densify": result}


class Fill(BaseModel):
    """
    $fill stage - fills null/missing field values.

    Example:
        >>> Fill(
        ...     sort_by={"date": 1},
        ...     output={
        ...         "score": {"method": "linear"},
        ...         "bootcamp": {"value": "missing"}
        ...     }
        ... ).model_dump()
    """

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    output: dict[str, Any] = Field(
        ..., description="Output field specifications"
    )
    partition_by: str | dict[str, Any] | None = Field(
        default=None,
        validation_alias="partitionBy",
        serialization_alias="partitionBy",
        description="Partitioning expression",
    )
    partition_by_fields: list[str] | None = Field(
        default=None,
        validation_alias="partitionByFields",
        serialization_alias="partitionByFields",
        description="Fields to partition by",
    )
    sort_by: dict[str, Literal[-1, 1]] | None = Field(
        default=None,
        validation_alias="sortBy",
        serialization_alias="sortBy",
        description="Sort specification",
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        result: dict[str, Any] = {"output": self.output}
        if self.partition_by is not None:
            result["partitionBy"] = self.partition_by
        if self.partition_by_fields is not None:
            result["partitionByFields"] = self.partition_by_fields
        if self.sort_by is not None:
            result["sortBy"] = self.sort_by
        return {"$fill": result}


__all__ = [
    "SetWindowFields",
    "Densify",
    "Fill",
]

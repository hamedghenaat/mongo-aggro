"""Grouping and bucketing MongoDB aggregation pipeline stages.

This module contains stages for advanced grouping operations:
Facet, Bucket, BucketAuto, and SortByCount.
"""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from mongo_aggro.base import BaseStage, Pipeline


class SortByCount(BaseModel, BaseStage):
    """
    $sortByCount stage - groups and counts by field, sorted by count.

    Example:
        >>> SortByCount(field="category").model_dump()
        {"$sortByCount": "$category"}
    """

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    field: str = Field(..., description="Field to group and count by")

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        field_path = (
            f"${self.field}" if not self.field.startswith("$") else self.field
        )
        return {"$sortByCount": field_path}


class Facet(BaseModel, BaseStage):
    """
    $facet stage - processes multiple pipelines within a single stage.

    Example:
        >>> Facet(pipelines={
        ...     "byCategory": Pipeline([Group(id="$category")]),
        ...     "byYear": Pipeline([Group(id="$year")])
        ... }).model_dump()
        {"$facet": {
            "byCategory": [{"$group": {"_id": "$category"}}],
            "byYear": [{"$group": {"_id": "$year"}}]
        }}
    """

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    pipelines: dict[str, Pipeline | list[dict[str, Any]]] = Field(
        ..., description="Named pipelines"
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        result: dict[str, list[dict[str, Any]]] = {}
        for name, pipeline in self.pipelines.items():
            if isinstance(pipeline, Pipeline):
                result[name] = pipeline.to_list()
            else:
                result[name] = pipeline
        return {"$facet": result}


class Bucket(BaseModel, BaseStage):
    """
    $bucket stage - categorizes documents into buckets.

    Example:
        >>> Bucket(
        ...     group_by="$price",
        ...     boundaries=[0, 100, 500, 1000],
        ...     default="Other",
        ...     output={"count": {"$sum": 1}}
        ... ).model_dump()
        {"$bucket": {
            "groupBy": "$price",
            "boundaries": [0, 100, 500, 1000],
            "default": "Other",
            "output": {"count": {"$sum": 1}}
        }}
    """

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    group_by: str | dict[str, Any] = Field(
        ...,
        validation_alias="groupBy",
        serialization_alias="groupBy",
        description="Expression to group by",
    )
    boundaries: list[Any] = Field(..., description="Bucket boundaries")
    default: Any | None = Field(
        default=None, description="Default bucket for non-matching docs"
    )
    output: dict[str, Any] | None = Field(
        default=None, description="Output document specification"
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        result: dict[str, Any] = {
            "groupBy": self.group_by,
            "boundaries": self.boundaries,
        }
        if self.default is not None:
            result["default"] = self.default
        if self.output is not None:
            result["output"] = self.output
        return {"$bucket": result}


class BucketAuto(BaseModel, BaseStage):
    """
    $bucketAuto stage - automatically categorizes into specified buckets.

    Example:
        >>> BucketAuto(group_by="$age", buckets=5).model_dump()
        {"$bucketAuto": {"groupBy": "$age", "buckets": 5}}
    """

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    group_by: str | dict[str, Any] = Field(
        ...,
        validation_alias="groupBy",
        serialization_alias="groupBy",
        description="Expression to group by",
    )
    buckets: int = Field(..., gt=0, description="Number of buckets")
    output: dict[str, Any] | None = Field(
        default=None, description="Output document specification"
    )
    granularity: str | None = Field(
        default=None, description="Preferred number series"
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        result: dict[str, Any] = {
            "groupBy": self.group_by,
            "buckets": self.buckets,
        }
        if self.output is not None:
            result["output"] = self.output
        if self.granularity is not None:
            result["granularity"] = self.granularity
        return {"$bucketAuto": result}


__all__ = [
    "Facet",
    "Bucket",
    "BucketAuto",
    "SortByCount",
]

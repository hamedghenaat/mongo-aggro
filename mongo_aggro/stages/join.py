"""Join-related MongoDB aggregation pipeline stages.

This module contains stages for joining and combining data from multiple
collections: Lookup, UnionWith, and GraphLookup.
"""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from mongo_aggro.base import BaseStage, Pipeline


class Lookup(BaseModel, BaseStage):
    """
    $lookup stage - performs a left outer join.

    Example:
        >>> # Simple lookup
        >>> Lookup(
        ...     from_collection="products",
        ...     local_field="product_id",
        ...     foreign_field="_id",
        ...     as_field="product"
        ... ).model_dump()
        {"$lookup": {
            "from": "products",
            "localField": "product_id",
            "foreignField": "_id",
            "as": "product"
        }}

        >>> # With pipeline
        >>> Lookup(
        ...     from_collection="orders",
        ...     let={"customerId": "$_id"},
        ...     pipeline=Pipeline([Match(query={"status": "active"})]),
        ...     as_field="orders"
        ... ).model_dump()
    """

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    from_collection: str = Field(
        ...,
        validation_alias="from",
        serialization_alias="from",
        description="Foreign collection name",
    )
    local_field: str | None = Field(
        default=None,
        validation_alias="localField",
        serialization_alias="localField",
        description="Local field for join",
    )
    foreign_field: str | None = Field(
        default=None,
        validation_alias="foreignField",
        serialization_alias="foreignField",
        description="Foreign field for join",
    )
    let: dict[str, Any] | None = Field(
        default=None, description="Variables for pipeline"
    )
    pipeline: Pipeline | list[dict[str, Any]] | None = Field(
        default=None, description="Sub-pipeline for complex joins"
    )
    as_field: str = Field(
        ...,
        validation_alias="as",
        serialization_alias="as",
        description="Output array field name",
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        result: dict[str, Any] = {
            "from": self.from_collection,
            "as": self.as_field,
        }

        if self.local_field is not None:
            result["localField"] = self.local_field
        if self.foreign_field is not None:
            result["foreignField"] = self.foreign_field
        if self.let is not None:
            result["let"] = self.let
        if self.pipeline is not None:
            if isinstance(self.pipeline, Pipeline):
                result["pipeline"] = self.pipeline.to_list()
            else:
                result["pipeline"] = self.pipeline

        return {"$lookup": result}


class UnionWith(BaseModel, BaseStage):
    """
    $unionWith stage - combines pipeline results with another collection.

    Example:
        >>> UnionWith(collection="archive").model_dump()
        {"$unionWith": "archive"}

        >>> UnionWith(
        ...     collection="archive",
        ...     pipeline=Pipeline([Match(query={"year": 2023})])
        ... ).model_dump()
        {"$unionWith": {"coll": "archive", "pipeline": [...]}}
    """

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    collection: str = Field(
        ...,
        validation_alias="coll",
        serialization_alias="coll",
        description="Collection to union",
    )
    pipeline: Pipeline | list[dict[str, Any]] | None = Field(
        default=None, description="Pipeline for the other collection"
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        if self.pipeline is None:
            return {"$unionWith": self.collection}

        pl = (
            self.pipeline.to_list()
            if isinstance(self.pipeline, Pipeline)
            else self.pipeline
        )
        return {"$unionWith": {"coll": self.collection, "pipeline": pl}}


class GraphLookup(BaseModel, BaseStage):
    """
    $graphLookup stage - performs recursive search.

    Example:
        >>> GraphLookup(
        ...     from_collection="employees",
        ...     start_with="$reportsTo",
        ...     connect_from_field="reportsTo",
        ...     connect_to_field="name",
        ...     as_field="reportingHierarchy"
        ... ).model_dump()
    """

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    from_collection: str = Field(
        ...,
        validation_alias="from",
        serialization_alias="from",
        description="Collection to search",
    )
    start_with: Any = Field(
        ...,
        validation_alias="startWith",
        serialization_alias="startWith",
        description="Expression for starting point",
    )
    connect_from_field: str = Field(
        ...,
        validation_alias="connectFromField",
        serialization_alias="connectFromField",
        description="Field to recurse from",
    )
    connect_to_field: str = Field(
        ...,
        validation_alias="connectToField",
        serialization_alias="connectToField",
        description="Field to match",
    )
    as_field: str = Field(
        ...,
        validation_alias="as",
        serialization_alias="as",
        description="Output array field",
    )
    max_depth: int | None = Field(
        default=None,
        validation_alias="maxDepth",
        serialization_alias="maxDepth",
        description="Maximum recursion depth",
    )
    depth_field: str | None = Field(
        default=None,
        validation_alias="depthField",
        serialization_alias="depthField",
        description="Field for recursion depth",
    )
    restrict_search_with_match: dict[str, Any] | None = Field(
        default=None,
        validation_alias="restrictSearchWithMatch",
        serialization_alias="restrictSearchWithMatch",
        description="Additional match conditions",
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        result: dict[str, Any] = {
            "from": self.from_collection,
            "startWith": self.start_with,
            "connectFromField": self.connect_from_field,
            "connectToField": self.connect_to_field,
            "as": self.as_field,
        }
        if self.max_depth is not None:
            result["maxDepth"] = self.max_depth
        if self.depth_field is not None:
            result["depthField"] = self.depth_field
        if self.restrict_search_with_match is not None:
            result["restrictSearchWithMatch"] = self.restrict_search_with_match
        return {"$graphLookup": result}


__all__ = [
    "Lookup",
    "UnionWith",
    "GraphLookup",
]

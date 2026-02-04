"""MongoDB aggregation pipeline stages."""

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from mongo_aggro.base import BaseStage, Pipeline


class Match(BaseModel, BaseStage):
    """
    $match stage - filters documents by specified criteria.

    Example:
        >>> Match(query={"status": "active"}).model_dump()
        {"$match": {"status": "active"}}

        >>> # With logical operators
        >>> Match(query={"$and": [{"status": "active"}, {"age": {"$gt": 18}}]})
    """

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    query: dict[str, Any] = Field(..., description="Query filter conditions")

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return {"$match": self.query}


class Project(BaseModel, BaseStage):
    """
    $project stage - shapes documents by including/excluding fields.

    Example:
        >>> Project(fields={"name": 1, "year": 1, "_id": 0}).model_dump()
        {"$project": {"name": 1, "year": 1, "_id": 0}}

        >>> # With expressions
        >>> Project(fields={"fullName": {"$concat": ["$first", " ", "$last"]}})
    """

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    fields: dict[str, Any] = Field(
        ..., description="Field projections (1=include, 0=exclude, or expr)"
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return {"$project": self.fields}


class Group(BaseModel, BaseStage):
    """
    $group stage - groups documents by specified expression.

    Example:
        >>> Group(
        ...     id="$category",
        ...     total={"$sum": "$quantity"},
        ...     count={"$sum": 1}
        ... ).model_dump()
        {
            "$group": {
                "_id": "$category",
                "total": {"$sum": "$quantity"},
                "count": {"$sum": 1}
            }
        }
    """

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    id: Any = Field(
        ...,
        validation_alias="_id",
        serialization_alias="_id",
        description="Grouping expression",
    )
    accumulators: dict[str, Any] = Field(
        default_factory=dict,
        description="Accumulator expressions (e.g., $sum, $avg)",
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        result = {"_id": self.id}
        result.update(self.accumulators)
        return {"$group": result}


class Sort(BaseModel, BaseStage):
    """
    $sort stage - sorts documents.

    Example:
        >>> Sort(fields={"age": -1, "name": 1}).model_dump()
        {"$sort": {"age": -1, "name": 1}}
    """

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    fields: dict[str, Literal[-1, 1]] = Field(
        ..., description="Sort specification (1=asc, -1=desc)"
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return {"$sort": self.fields}


class Limit(BaseModel, BaseStage):
    """
    $limit stage - limits the number of documents.

    Example:
        >>> Limit(count=10).model_dump()
        {"$limit": 10}
    """

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    count: int = Field(..., gt=0, description="Maximum number of documents")

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return {"$limit": self.count}


class Skip(BaseModel, BaseStage):
    """
    $skip stage - skips a number of documents.

    Example:
        >>> Skip(count=5).model_dump()
        {"$skip": 5}
    """

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    count: int = Field(..., ge=0, description="Number of documents to skip")

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return {"$skip": self.count}


class Unwind(BaseModel, BaseStage):
    """
    $unwind stage - deconstructs an array field.

    Example:
        >>> Unwind(path="cars").model_dump()
        {"$unwind": "$cars"}

        >>> # With options
        >>> Unwind(
        ...     path="items",
        ...     include_array_index="itemIndex",
        ...     preserve_null_and_empty=True
        ... ).model_dump()
        {"$unwind": {
            "path": "$items",
            "includeArrayIndex": "itemIndex",
            "preserveNullAndEmptyArrays": true
        }}
    """

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    path: str = Field(..., description="Array field path (without $)")
    include_array_index: str | None = Field(
        default=None,
        validation_alias="includeArrayIndex",
        serialization_alias="includeArrayIndex",
        description="Name of index field",
    )
    preserve_null_and_empty: bool | None = Field(
        default=None,
        validation_alias="preserveNullAndEmptyArrays",
        serialization_alias="preserveNullAndEmptyArrays",
        description="Output doc if array is null/empty/missing",
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        field_path = (
            f"${self.path}" if not self.path.startswith("$") else self.path
        )

        if (
            self.include_array_index is None
            and self.preserve_null_and_empty is None
        ):
            return {"$unwind": field_path}

        result: dict[str, Any] = {"path": field_path}
        if self.include_array_index is not None:
            result["includeArrayIndex"] = self.include_array_index
        if self.preserve_null_and_empty is not None:
            result["preserveNullAndEmptyArrays"] = self.preserve_null_and_empty
        return {"$unwind": result}


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


class AddFields(BaseModel, BaseStage):
    """
    $addFields stage - adds new fields to documents.

    Example:
        >>> AddFields(fields={"isActive": True, "score": {"$sum": "$marks"}})
        {"$addFields": {"isActive": true, "score": {"$sum": "$marks"}}}
    """

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    fields: dict[str, Any] = Field(..., description="Fields to add")

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return {"$addFields": self.fields}


class Set(BaseModel, BaseStage):
    """
    $set stage - alias for $addFields.

    Example:
        >>> Set(fields={"status": "processed"}).model_dump()
        {"$set": {"status": "processed"}}
    """

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    fields: dict[str, Any] = Field(..., description="Fields to set")

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return {"$set": self.fields}


class Unset(BaseModel, BaseStage):
    """
    $unset stage - removes fields from documents.

    Example:
        >>> Unset(fields=["password", "secret"]).model_dump()
        {"$unset": ["password", "secret"]}

        >>> Unset(fields="temporaryField").model_dump()
        {"$unset": "temporaryField"}
    """

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    fields: str | list[str] = Field(..., description="Field(s) to remove")

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return {"$unset": self.fields}


class Count(BaseModel, BaseStage):
    """
    $count stage - counts documents.

    Example:
        >>> Count(field="total").model_dump()
        {"$count": "total"}
    """

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    field: str = Field(..., description="Output field name for count")

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return {"$count": self.field}


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


class ReplaceRoot(BaseModel, BaseStage):
    """
    $replaceRoot stage - replaces document with specified embedded document.

    Example:
        >>> ReplaceRoot(new_root="$nested").model_dump()
        {"$replaceRoot": {"newRoot": "$nested"}}
    """

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    new_root: str | dict[str, Any] = Field(
        ...,
        validation_alias="newRoot",
        serialization_alias="newRoot",
        description="Expression for new root",
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return {"$replaceRoot": {"newRoot": self.new_root}}


class ReplaceWith(BaseModel, BaseStage):
    """
    $replaceWith stage - replaces document (alias for $replaceRoot).

    Example:
        >>> ReplaceWith(expression="$embedded").model_dump()
        {"$replaceWith": "$embedded"}
    """

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    expression: str | dict[str, Any] = Field(
        ..., description="Expression for new document"
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return {"$replaceWith": self.expression}


class Sample(BaseModel, BaseStage):
    """
    $sample stage - randomly selects documents.

    Example:
        >>> Sample(size=10).model_dump()
        {"$sample": {"size": 10}}
    """

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    size: int = Field(..., gt=0, description="Number of documents to sample")

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return {"$sample": {"size": self.size}}


class Out(BaseModel, BaseStage):
    """
    $out stage - writes results to a collection.

    Example:
        >>> Out(collection="results").model_dump()
        {"$out": "results"}

        >>> Out(collection="results", db="analytics").model_dump()
        {"$out": {"db": "analytics", "coll": "results"}}
    """

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    collection: str = Field(..., description="Output collection name")
    db: str | None = Field(default=None, description="Output database name")

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        if self.db is not None:
            return {"$out": {"db": self.db, "coll": self.collection}}
        return {"$out": self.collection}


class Merge(BaseModel, BaseStage):
    """
    $merge stage - writes results to a collection with merge behavior.

    Example:
        >>> Merge(
        ...     into="reports",
        ...     on="_id",
        ...     when_matched="merge",
        ...     when_not_matched="insert"
        ... ).model_dump()
        {"$merge": {
            "into": "reports",
            "on": "_id",
            "whenMatched": "merge",
            "whenNotMatched": "insert"
        }}
    """

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    into: str | dict[str, str] = Field(
        ..., description="Target collection (or {db, coll})"
    )
    on: str | list[str] | None = Field(
        default=None, description="Field(s) to match on"
    )
    let: dict[str, Any] | None = Field(
        default=None, description="Variables for pipeline"
    )
    when_matched: str | list[dict[str, Any]] | None = Field(
        default=None,
        validation_alias="whenMatched",
        serialization_alias="whenMatched",
        description="Action when matched (replace, keepExisting, merge, fail, "
        "or pipeline)",
    )
    when_not_matched: str | None = Field(
        default=None,
        validation_alias="whenNotMatched",
        serialization_alias="whenNotMatched",
        description="Action when not matched (insert, discard, fail)",
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        result: dict[str, Any] = {"into": self.into}
        if self.on is not None:
            result["on"] = self.on
        if self.let is not None:
            result["let"] = self.let
        if self.when_matched is not None:
            result["whenMatched"] = self.when_matched
        if self.when_not_matched is not None:
            result["whenNotMatched"] = self.when_not_matched
        return {"$merge": result}


class Redact(BaseModel, BaseStage):
    """
    $redact stage - restricts document content based on stored info.

    Example:
        >>> Redact(expression={
        ...     "$cond": {
        ...         "if": {"$eq": ["$level", 5]},
        ...         "then": "$$PRUNE",
        ...         "else": "$$DESCEND"
        ...     }
        ... }).model_dump()
    """

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    expression: dict[str, Any] = Field(..., description="Redaction expression")

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return {"$redact": self.expression}


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


class GeoNear(BaseModel, BaseStage):
    """
    $geoNear stage - returns documents near a geographic point.

    Example:
        >>> GeoNear(
        ...     near={"type": "Point", "coordinates": [-73.99, 40.73]},
        ...     distance_field="dist.calculated",
        ...     spherical=True,
        ...     max_distance=5000
        ... ).model_dump()
    """

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    near: dict[str, Any] | list[float] = Field(
        ..., description="GeoJSON point or legacy coordinates"
    )
    distance_field: str = Field(
        ...,
        validation_alias="distanceField",
        serialization_alias="distanceField",
        description="Field for calculated distance",
    )
    spherical: bool | None = Field(
        default=None, description="Use spherical geometry"
    )
    max_distance: float | None = Field(
        default=None,
        validation_alias="maxDistance",
        serialization_alias="maxDistance",
        description="Max distance in meters",
    )
    min_distance: float | None = Field(
        default=None,
        validation_alias="minDistance",
        serialization_alias="minDistance",
        description="Min distance in meters",
    )
    query: dict[str, Any] | None = Field(
        default=None, description="Additional query filter"
    )
    distance_multiplier: float | None = Field(
        default=None,
        validation_alias="distanceMultiplier",
        serialization_alias="distanceMultiplier",
        description="Multiplier for distances",
    )
    include_locs: str | None = Field(
        default=None,
        validation_alias="includeLocs",
        serialization_alias="includeLocs",
        description="Field for matched location",
    )
    key: str | None = Field(
        default=None, description="Geospatial index to use"
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        result: dict[str, Any] = {
            "near": self.near,
            "distanceField": self.distance_field,
        }
        if self.spherical is not None:
            result["spherical"] = self.spherical
        if self.max_distance is not None:
            result["maxDistance"] = self.max_distance
        if self.min_distance is not None:
            result["minDistance"] = self.min_distance
        if self.query is not None:
            result["query"] = self.query
        if self.distance_multiplier is not None:
            result["distanceMultiplier"] = self.distance_multiplier
        if self.include_locs is not None:
            result["includeLocs"] = self.include_locs
        if self.key is not None:
            result["key"] = self.key
        return {"$geoNear": result}


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


class SetWindowFields(BaseModel, BaseStage):
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


class Densify(BaseModel, BaseStage):
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


class Fill(BaseModel, BaseStage):
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


class Documents(BaseModel, BaseStage):
    """
    $documents stage - returns literal documents.

    Example:
        >>> Documents(documents=[
        ...     {"x": 1, "y": 2},
        ...     {"x": 3, "y": 4}
        ... ]).model_dump()
        {"$documents": [{"x": 1, "y": 2}, {"x": 3, "y": 4}]}
    """

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    documents: list[dict[str, Any]] = Field(
        ..., description="Documents to return"
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return {"$documents": self.documents}


class CollStats(BaseModel, BaseStage):
    """
    $collStats stage - returns collection statistics.

    Example:
        >>> CollStats(lat_stats={"histograms": True}).model_dump()
        {"$collStats": {"latencyStats": {"histograms": True}}}

        >>> CollStats(storage_stats={}).model_dump()
        {"$collStats": {"storageStats": {}}}

        >>> CollStats(count={}).model_dump()
        {"$collStats": {"count": {}}}
    """

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    lat_stats: dict[str, Any] | None = Field(
        default=None,
        serialization_alias="latencyStats",
        description="Latency statistics options",
    )
    storage_stats: dict[str, Any] | None = Field(
        default=None,
        serialization_alias="storageStats",
        description="Storage statistics options",
    )
    count: dict[str, Any] | None = Field(
        default=None,
        description="Document count options",
    )
    query_exec_stats: dict[str, Any] | None = Field(
        default=None,
        serialization_alias="queryExecStats",
        description="Query execution statistics options",
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        result: dict[str, Any] = {}
        if self.lat_stats is not None:
            result["latencyStats"] = self.lat_stats
        if self.storage_stats is not None:
            result["storageStats"] = self.storage_stats
        if self.count is not None:
            result["count"] = self.count
        if self.query_exec_stats is not None:
            result["queryExecStats"] = self.query_exec_stats
        return {"$collStats": result}


class IndexStats(BaseModel, BaseStage):
    """
    $indexStats stage - returns index usage statistics.

    Example:
        >>> IndexStats().model_dump()
        {"$indexStats": {}}
    """

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return {"$indexStats": {}}


class PlanCacheStats(BaseModel, BaseStage):
    """
    $planCacheStats stage - returns plan cache information.

    Example:
        >>> PlanCacheStats().model_dump()
        {"$planCacheStats": {}}
    """

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return {"$planCacheStats": {}}


class ListSessions(BaseModel, BaseStage):
    """
    $listSessions stage - lists all sessions in system.sessions.

    Example:
        >>> ListSessions().model_dump()
        {"$listSessions": {}}

        >>> ListSessions(users=[{"user": "admin", "db": "admin"}]).model_dump()
        {"$listSessions": {"users": [{"user": "admin", "db": "admin"}]}}

        >>> ListSessions(all_users=True).model_dump()
        {"$listSessions": {"allUsers": True}}
    """

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    users: list[dict[str, str]] | None = Field(
        default=None,
        description="List of users to filter sessions",
    )
    all_users: bool | None = Field(
        default=None,
        serialization_alias="allUsers",
        description="Return sessions for all users",
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        result: dict[str, Any] = {}
        if self.users is not None:
            result["users"] = self.users
        if self.all_users is not None:
            result["allUsers"] = self.all_users
        return {"$listSessions": result}


class ListLocalSessions(BaseModel, BaseStage):
    """
    $listLocalSessions stage - lists local sessions (db.aggregate only).

    Example:
        >>> ListLocalSessions().model_dump()
        {"$listLocalSessions": {}}

        >>> ListLocalSessions(all_users=True).model_dump()
        {"$listLocalSessions": {"allUsers": True}}
    """

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    users: list[dict[str, str]] | None = Field(
        default=None,
        description="List of users to filter sessions",
    )
    all_users: bool | None = Field(
        default=None,
        serialization_alias="allUsers",
        description="Return sessions for all users",
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        result: dict[str, Any] = {}
        if self.users is not None:
            result["users"] = self.users
        if self.all_users is not None:
            result["allUsers"] = self.all_users
        return {"$listLocalSessions": result}


class ListSampledQueries(BaseModel, BaseStage):
    """
    $listSampledQueries stage - lists sampled queries.

    Example:
        >>> ListSampledQueries().model_dump()
        {"$listSampledQueries": {}}

        >>> ListSampledQueries(namespace="db.collection").model_dump()
        {"$listSampledQueries": {"namespace": "db.collection"}}
    """

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    namespace: str | None = Field(
        default=None,
        description="Namespace to filter sampled queries",
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        result: dict[str, Any] = {}
        if self.namespace is not None:
            result["namespace"] = self.namespace
        return {"$listSampledQueries": result}


class ChangeStream(BaseModel, BaseStage):
    """
    $changeStream stage - returns a change stream cursor.

    Must be the first stage in the pipeline.

    Example:
        >>> ChangeStream().model_dump()
        {"$changeStream": {}}

        >>> ChangeStream(full_document="updateLookup").model_dump()
        {"$changeStream": {"fullDocument": "updateLookup"}}
    """

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    full_document: (
        Literal["default", "updateLookup", "whenAvailable", "required"] | None
    ) = Field(
        default=None,
        serialization_alias="fullDocument",
        description="Full document option for update events",
    )
    full_document_before_change: (
        Literal["off", "whenAvailable", "required"] | None
    ) = Field(
        default=None,
        serialization_alias="fullDocumentBeforeChange",
        description="Include pre-image of modified document",
    )
    resume_after: dict[str, Any] | None = Field(
        default=None,
        serialization_alias="resumeAfter",
        description="Resume token to resume change stream",
    )
    start_after: dict[str, Any] | None = Field(
        default=None,
        serialization_alias="startAfter",
        description="Resume token to start after",
    )
    start_at_operation_time: Any | None = Field(
        default=None,
        serialization_alias="startAtOperationTime",
        description="Timestamp to start watching changes",
    )
    all_changes_for_cluster: bool | None = Field(
        default=None,
        serialization_alias="allChangesForCluster",
        description="Watch all changes for the cluster",
    )
    show_expanded_events: bool | None = Field(
        default=None,
        serialization_alias="showExpandedEvents",
        description="Show expanded change events",
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        result: dict[str, Any] = {}
        if self.full_document is not None:
            result["fullDocument"] = self.full_document
        if self.full_document_before_change is not None:
            result["fullDocumentBeforeChange"] = (
                self.full_document_before_change
            )
        if self.resume_after is not None:
            result["resumeAfter"] = self.resume_after
        if self.start_after is not None:
            result["startAfter"] = self.start_after
        if self.start_at_operation_time is not None:
            result["startAtOperationTime"] = self.start_at_operation_time
        if self.all_changes_for_cluster is not None:
            result["allChangesForCluster"] = self.all_changes_for_cluster
        if self.show_expanded_events is not None:
            result["showExpandedEvents"] = self.show_expanded_events
        return {"$changeStream": result}


class ChangeStreamSplitLargeEvent(BaseModel, BaseStage):
    """
    $changeStreamSplitLargeEvent stage - splits large change events.

    Must be the last stage in a $changeStream pipeline.

    Example:
        >>> ChangeStreamSplitLargeEvent().model_dump()
        {"$changeStreamSplitLargeEvent": {}}
    """

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return {"$changeStreamSplitLargeEvent": {}}


class CurrentOp(BaseModel, BaseStage):
    """
    $currentOp stage - returns current operations (db.aggregate only).

    Example:
        >>> CurrentOp().model_dump()
        {"$currentOp": {}}

        >>> CurrentOp(all_users=True, idle_connections=True).model_dump()
        {"$currentOp": {"allUsers": True, "idleConnections": True}}
    """

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    all_users: bool | None = Field(
        default=None,
        serialization_alias="allUsers",
        description="Return operations for all users",
    )
    idle_connections: bool | None = Field(
        default=None,
        serialization_alias="idleConnections",
        description="Include idle connections",
    )
    idle_cursors: bool | None = Field(
        default=None,
        serialization_alias="idleCursors",
        description="Include idle cursors",
    )
    idle_sessions: bool | None = Field(
        default=None,
        serialization_alias="idleSessions",
        description="Include idle sessions",
    )
    local_ops: bool | None = Field(
        default=None,
        serialization_alias="localOps",
        description="Return local operations only",
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        result: dict[str, Any] = {}
        if self.all_users is not None:
            result["allUsers"] = self.all_users
        if self.idle_connections is not None:
            result["idleConnections"] = self.idle_connections
        if self.idle_cursors is not None:
            result["idleCursors"] = self.idle_cursors
        if self.idle_sessions is not None:
            result["idleSessions"] = self.idle_sessions
        if self.local_ops is not None:
            result["localOps"] = self.local_ops
        return {"$currentOp": result}


class ListClusterCatalog(BaseModel, BaseStage):
    """
    $listClusterCatalog stage - lists collections in a cluster.

    Example:
        >>> ListClusterCatalog().model_dump()
        {"$listClusterCatalog": {}}
    """

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return {"$listClusterCatalog": {}}


class ListSearchIndexes(BaseModel, BaseStage):
    """
    $listSearchIndexes stage - lists Atlas Search indexes.

    Example:
        >>> ListSearchIndexes().model_dump()
        {"$listSearchIndexes": {}}

        >>> ListSearchIndexes(id="index_id").model_dump()
        {"$listSearchIndexes": {"id": "index_id"}}

        >>> ListSearchIndexes(name="index_name").model_dump()
        {"$listSearchIndexes": {"name": "index_name"}}
    """

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    id: str | None = Field(
        default=None,
        description="Search index ID to filter",
    )
    name: str | None = Field(
        default=None,
        description="Search index name to filter",
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        result: dict[str, Any] = {}
        if self.id is not None:
            result["id"] = self.id
        if self.name is not None:
            result["name"] = self.name
        return {"$listSearchIndexes": result}


class Search(BaseModel, BaseStage):
    """
    $search stage - Atlas full-text search.

    Example:
        >>> Search(index="default", text={"query": "coffee", "path": "title"}).model_dump()
        {"$search": {"index": "default", "text": {"query": "coffee", "path": "title"}}}
    """

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    index: str | None = Field(
        default=None,
        description="Name of the Atlas Search index",
    )
    text: dict[str, Any] | None = Field(
        default=None,
        description="Text search operator",
    )
    compound: dict[str, Any] | None = Field(
        default=None,
        description="Compound search operator",
    )
    autocomplete: dict[str, Any] | None = Field(
        default=None,
        description="Autocomplete search operator",
    )
    phrase: dict[str, Any] | None = Field(
        default=None,
        description="Phrase search operator",
    )
    wildcard: dict[str, Any] | None = Field(
        default=None,
        description="Wildcard search operator",
    )
    regex: dict[str, Any] | None = Field(
        default=None,
        description="Regex search operator",
    )
    near: dict[str, Any] | None = Field(
        default=None,
        description="Near search operator",
    )
    range: dict[str, Any] | None = Field(
        default=None,
        description="Range search operator",
    )
    exists: dict[str, Any] | None = Field(
        default=None,
        description="Exists search operator",
    )
    equals: dict[str, Any] | None = Field(
        default=None,
        description="Equals search operator",
    )
    more_like_this: dict[str, Any] | None = Field(
        default=None,
        serialization_alias="moreLikeThis",
        description="More like this search operator",
    )
    query_string: dict[str, Any] | None = Field(
        default=None,
        serialization_alias="queryString",
        description="Query string search operator",
    )
    highlight: dict[str, Any] | None = Field(
        default=None,
        description="Highlight options",
    )
    count: dict[str, Any] | None = Field(
        default=None,
        description="Count options",
    )
    return_stored_source: bool | None = Field(
        default=None,
        serialization_alias="returnStoredSource",
        description="Return stored source",
    )

    def _add_operators(self, result: dict[str, Any]) -> None:
        """Add search operators to result dict."""
        if self.text is not None:
            result["text"] = self.text
        if self.compound is not None:
            result["compound"] = self.compound
        if self.autocomplete is not None:
            result["autocomplete"] = self.autocomplete
        if self.phrase is not None:
            result["phrase"] = self.phrase
        if self.wildcard is not None:
            result["wildcard"] = self.wildcard
        if self.regex is not None:
            result["regex"] = self.regex
        if self.near is not None:
            result["near"] = self.near
        if self.range is not None:
            result["range"] = self.range

    def _add_advanced(self, result: dict[str, Any]) -> None:
        """Add advanced search options to result dict."""
        if self.exists is not None:
            result["exists"] = self.exists
        if self.equals is not None:
            result["equals"] = self.equals
        if self.more_like_this is not None:
            result["moreLikeThis"] = self.more_like_this
        if self.query_string is not None:
            result["queryString"] = self.query_string
        if self.highlight is not None:
            result["highlight"] = self.highlight
        if self.count is not None:
            result["count"] = self.count
        if self.return_stored_source is not None:
            result["returnStoredSource"] = self.return_stored_source

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        result: dict[str, Any] = {}
        if self.index is not None:
            result["index"] = self.index
        self._add_operators(result)
        self._add_advanced(result)
        return {"$search": result}


class SearchMeta(BaseModel, BaseStage):
    """
    $searchMeta stage - returns Atlas Search metadata.

    Example:
        >>> SearchMeta(index="default", count={"type": "total"}).model_dump()
        {"$searchMeta": {"index": "default", "count": {"type": "total"}}}
    """

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    index: str | None = Field(
        default=None,
        description="Name of the Atlas Search index",
    )
    count: dict[str, Any] | None = Field(
        default=None,
        description="Count options",
    )
    facet: dict[str, Any] | None = Field(
        default=None,
        description="Facet options",
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        result: dict[str, Any] = {}
        if self.index is not None:
            result["index"] = self.index
        if self.count is not None:
            result["count"] = self.count
        if self.facet is not None:
            result["facet"] = self.facet
        return {"$searchMeta": result}


class VectorSearch(BaseModel, BaseStage):
    """
    $vectorSearch stage - Atlas vector search (MongoDB 7.0.2+).

    Example:
        >>> VectorSearch(
        ...     index="vector_index",
        ...     path="embedding",
        ...     query_vector=[0.1, 0.2, 0.3],
        ...     num_candidates=100,
        ...     limit=10
        ... ).model_dump()
        {"$vectorSearch": {
            "index": "vector_index",
            "path": "embedding",
            "queryVector": [0.1, 0.2, 0.3],
            "numCandidates": 100,
            "limit": 10
        }}
    """

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    index: str = Field(
        ...,
        description="Name of the Atlas Vector Search index",
    )
    path: str = Field(
        ...,
        description="Field path containing the vector",
    )
    query_vector: list[float] = Field(
        ...,
        serialization_alias="queryVector",
        description="Query vector for similarity search",
    )
    num_candidates: int = Field(
        ...,
        serialization_alias="numCandidates",
        description="Number of candidates to consider",
    )
    limit: int = Field(
        ...,
        description="Maximum number of results to return",
    )
    filter: dict[str, Any] | None = Field(
        default=None,
        description="Pre-filter for vector search",
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        result: dict[str, Any] = {
            "index": self.index,
            "path": self.path,
            "queryVector": self.query_vector,
            "numCandidates": self.num_candidates,
            "limit": self.limit,
        }
        if self.filter is not None:
            result["filter"] = self.filter
        return {"$vectorSearch": result}


class QuerySettings(BaseModel, BaseStage):
    """
    $querySettings stage - returns query settings (MongoDB 8.0+).

    Example:
        >>> QuerySettings().model_dump()
        {"$querySettings": {}}
    """

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return {"$querySettings": {}}


class RankFusion(BaseModel, BaseStage):
    """
    $rankFusion stage - combines ranked results from multiple pipelines.

    Example:
        >>> RankFusion(
        ...     input={"search": [...], "vector": [...]},
        ...     combination={"weights": {"search": 0.7, "vector": 0.3}}
        ... ).model_dump()
        {"$rankFusion": {
            "input": {"search": [...], "vector": [...]},
            "combination": {"weights": {"search": 0.7, "vector": 0.3}}
        }}
    """

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    input: dict[str, list[dict[str, Any]]] = Field(
        ...,
        description="Named input pipelines",
    )
    combination: dict[str, Any] | None = Field(
        default=None,
        description="Combination options",
    )
    score_details: bool | None = Field(
        default=None,
        serialization_alias="scoreDetails",
        description="Include score details",
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        result: dict[str, Any] = {"input": self.input}
        if self.combination is not None:
            result["combination"] = self.combination
        if self.score_details is not None:
            result["scoreDetails"] = self.score_details
        return {"$rankFusion": result}

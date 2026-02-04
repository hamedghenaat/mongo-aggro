"""Output and sampling MongoDB aggregation pipeline stages.

This module contains stages for writing output and sampling:
Out, Merge, Sample, and Documents.
"""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from mongo_aggro.base import BaseStage


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


__all__ = [
    "Out",
    "Merge",
    "Sample",
    "Documents",
]

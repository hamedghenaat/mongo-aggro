"""Core MongoDB aggregation pipeline stages.

This module contains the fundamental stages used in most aggregation pipelines:
Match, Project, Group, Sort, Limit, Skip, and Count.
"""

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class Match(BaseModel):
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


class Project(BaseModel):
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


class Group(BaseModel):
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


class Sort(BaseModel):
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


class Limit(BaseModel):
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


class Skip(BaseModel):
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


class Count(BaseModel):
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


__all__ = [
    "Match",
    "Project",
    "Group",
    "Sort",
    "Limit",
    "Skip",
    "Count",
]

"""Geospatial MongoDB aggregation pipeline stages.

This module contains stages for geospatial queries: GeoNear.
"""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from mongo_aggro.base import BaseStage


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


__all__ = [
    "GeoNear",
]

"""Geospatial query operators for MongoDB aggregation."""

from typing import Any

from pydantic import Field

from mongo_aggro.operators.base import QueryOperator


class GeoIntersects(QueryOperator):
    """
    $geoIntersects operator - matches geometries that intersect.

    Example:
        >>> GeoIntersects(geometry={
        ...     "type": "Polygon",
        ...     "coordinates": [[[-100, 60], [-100, 0], [100, 0], [100, 60]]]
        ... }).model_dump()
        {"$geoIntersects": {"$geometry": {...}}}
    """

    geometry: dict[str, Any] = Field(
        ..., description="GeoJSON geometry object"
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return {"$geoIntersects": {"$geometry": self.geometry}}


class GeoWithin(QueryOperator):
    """
    $geoWithin operator - matches geometries within a bounding region.

    Example:
        >>> GeoWithin(geometry={
        ...     "type": "Polygon",
        ...     "coordinates": [[[-100, 60], [-100, 0], [100, 0], [100, 60]]]
        ... }).model_dump()
        {"$geoWithin": {"$geometry": {...}}}

        >>> # Using legacy shapes
        >>> GeoWithin(box=[[-100, -100], [100, 100]]).model_dump()
        {"$geoWithin": {"$box": [[-100, -100], [100, 100]]}}
    """

    geometry: dict[str, Any] | None = Field(
        default=None, description="GeoJSON geometry object"
    )
    box: list[list[float]] | None = Field(
        default=None, description="Legacy box coordinates [[x1,y1], [x2,y2]]"
    )
    polygon: list[list[float]] | None = Field(
        default=None, description="Legacy polygon coordinates"
    )
    center: list[Any] | None = Field(
        default=None, description="Legacy center coordinates [[x,y], radius]"
    )
    center_sphere: list[Any] | None = Field(
        default=None,
        serialization_alias="centerSphere",
        description="Center sphere [[x,y], radius]",
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        result: dict[str, Any] = {}
        if self.geometry is not None:
            result["$geometry"] = self.geometry
        if self.box is not None:
            result["$box"] = self.box
        if self.polygon is not None:
            result["$polygon"] = self.polygon
        if self.center is not None:
            result["$center"] = self.center
        if self.center_sphere is not None:
            result["$centerSphere"] = self.center_sphere
        return {"$geoWithin": result}


class Near(QueryOperator):
    """
    $near operator - matches geospatial objects near a point.

    Example:
        >>> Near(
        ...     geometry={"type": "Point", "coordinates": [-73.9667, 40.78]},
        ...     max_distance=5000,
        ...     min_distance=1000
        ... ).model_dump()
        {"$near": {"$geometry": {...}, "$maxDistance": 5000, "$minDistance": 1000}}
    """

    geometry: dict[str, Any] | None = Field(
        default=None, description="GeoJSON point"
    )
    max_distance: float | None = Field(
        default=None,
        serialization_alias="$maxDistance",
        description="Maximum distance in meters",
    )
    min_distance: float | None = Field(
        default=None,
        serialization_alias="$minDistance",
        description="Minimum distance in meters",
    )
    # Legacy 2d index format
    legacy_point: list[float] | None = Field(
        default=None, description="Legacy [x, y] coordinates"
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        if self.legacy_point is not None:
            result: dict[str, Any] = {"$near": self.legacy_point}
            if self.max_distance is not None:
                result["$maxDistance"] = self.max_distance
            return result
        result = {}
        if self.geometry is not None:
            result["$geometry"] = self.geometry
        if self.max_distance is not None:
            result["$maxDistance"] = self.max_distance
        if self.min_distance is not None:
            result["$minDistance"] = self.min_distance
        return {"$near": result}


class NearSphere(QueryOperator):
    """
    $nearSphere operator - matches geospatial objects near a point on sphere.

    Example:
        >>> NearSphere(
        ...     geometry={"type": "Point", "coordinates": [-73.9667, 40.78]},
        ...     max_distance=5000
        ... ).model_dump()
        {"$nearSphere": {"$geometry": {...}, "$maxDistance": 5000}}
    """

    geometry: dict[str, Any] | None = Field(
        default=None, description="GeoJSON point"
    )
    max_distance: float | None = Field(
        default=None,
        serialization_alias="$maxDistance",
        description="Maximum distance in meters",
    )
    min_distance: float | None = Field(
        default=None,
        serialization_alias="$minDistance",
        description="Minimum distance in meters",
    )
    legacy_point: list[float] | None = Field(
        default=None, description="Legacy [x, y] coordinates"
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        if self.legacy_point is not None:
            result: dict[str, Any] = {"$nearSphere": self.legacy_point}
            if self.max_distance is not None:
                result["$maxDistance"] = self.max_distance
            return result
        result = {}
        if self.geometry is not None:
            result["$geometry"] = self.geometry
        if self.max_distance is not None:
            result["$maxDistance"] = self.max_distance
        if self.min_distance is not None:
            result["$minDistance"] = self.min_distance
        return {"$nearSphere": result}


__all__ = ["GeoIntersects", "GeoWithin", "Near", "NearSphere"]

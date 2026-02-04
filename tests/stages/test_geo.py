"""Tests for geospatial aggregation stages."""

import pytest
from pydantic import ValidationError

from mongo_aggro.stages import GeoNear


def test_geo_near() -> None:
    """GeoNear stage."""
    geo = GeoNear(
        near={"type": "Point", "coordinates": [-73.99, 40.73]},
        distance_field="dist.calculated",
        spherical=True,
        max_distance=5000,
    )
    result = geo.model_dump()
    assert result["$geoNear"]["near"] == {
        "type": "Point",
        "coordinates": [-73.99, 40.73],
    }
    assert result["$geoNear"]["distanceField"] == "dist.calculated"
    assert result["$geoNear"]["spherical"] is True
    assert result["$geoNear"]["maxDistance"] == 5000


def test_geo_near_minimal() -> None:
    """GeoNear with only required fields."""
    geo = GeoNear(
        near={"type": "Point", "coordinates": [0, 0]},
        distance_field="distance",
    )
    result = geo.model_dump()
    assert result == {
        "$geoNear": {
            "near": {"type": "Point", "coordinates": [0, 0]},
            "distanceField": "distance",
        }
    }


def test_geo_near_legacy_coordinates() -> None:
    """GeoNear with legacy coordinate pair."""
    geo = GeoNear(
        near=[-73.99, 40.73],
        distance_field="dist",
    )
    result = geo.model_dump()
    assert result["$geoNear"]["near"] == [-73.99, 40.73]


def test_geo_near_all_options() -> None:
    """GeoNear with all options."""
    geo = GeoNear(
        near={"type": "Point", "coordinates": [-73.99, 40.73]},
        distance_field="dist",
        spherical=True,
        max_distance=10000,
        min_distance=100,
        query={"type": "restaurant"},
        distance_multiplier=0.001,
        include_locs="location",
        key="geoIndex",
    )
    result = geo.model_dump()
    assert result["$geoNear"]["minDistance"] == 100
    assert result["$geoNear"]["query"] == {"type": "restaurant"}
    assert result["$geoNear"]["distanceMultiplier"] == 0.001
    assert result["$geoNear"]["includeLocs"] == "location"
    assert result["$geoNear"]["key"] == "geoIndex"


def test_geo_near_missing_near() -> None:
    """GeoNear requires near parameter."""
    with pytest.raises(ValidationError):
        GeoNear(distance_field="dist")  # type: ignore[call-arg]


def test_geo_near_missing_distance_field() -> None:
    """GeoNear requires distance_field parameter."""
    with pytest.raises(ValidationError):
        GeoNear(  # type: ignore[call-arg]
            near={"type": "Point", "coordinates": [0, 0]}
        )

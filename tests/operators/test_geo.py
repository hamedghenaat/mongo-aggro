"""Tests for geospatial query operators."""

import pytest
from pydantic import ValidationError

from mongo_aggro.operators.geo import (
    GeoIntersects,
    GeoWithin,
    Near,
    NearSphere,
)

# --- GeoIntersects Operator Tests ---


def test_geo_intersects() -> None:
    """$geoIntersects operator with polygon geometry."""
    op = GeoIntersects(
        geometry={
            "type": "Polygon",
            "coordinates": [[[-100, 60], [-100, 0], [100, 0], [100, 60]]],
        }
    )
    assert op.model_dump() == {
        "$geoIntersects": {
            "$geometry": {
                "type": "Polygon",
                "coordinates": [[[-100, 60], [-100, 0], [100, 0], [100, 60]]],
            }
        }
    }


def test_geo_intersects_missing_geometry() -> None:
    """$geoIntersects requires geometry parameter."""
    with pytest.raises(ValidationError):
        GeoIntersects()  # type: ignore[call-arg]


def test_geo_intersects_invalid_geometry() -> None:
    """$geoIntersects geometry must be a dict."""
    with pytest.raises(ValidationError):
        GeoIntersects(geometry="not a dict")  # type: ignore[arg-type]


# --- GeoWithin Operator Tests ---


def test_geo_within_geometry() -> None:
    """$geoWithin with GeoJSON geometry."""
    op = GeoWithin(
        geometry={
            "type": "Polygon",
            "coordinates": [[[-100, 60], [-100, 0], [100, 0], [100, 60]]],
        }
    )
    assert op.model_dump() == {
        "$geoWithin": {
            "$geometry": {
                "type": "Polygon",
                "coordinates": [[[-100, 60], [-100, 0], [100, 0], [100, 60]]],
            }
        }
    }


def test_geo_within_box() -> None:
    """$geoWithin with legacy box."""
    op = GeoWithin(box=[[-100, -100], [100, 100]])
    assert op.model_dump() == {
        "$geoWithin": {"$box": [[-100, -100], [100, 100]]}
    }


def test_geo_within_no_params() -> None:
    """$geoWithin with no params returns empty geoWithin."""
    op = GeoWithin()
    assert op.model_dump() == {"$geoWithin": {}}


# --- Near Operator Tests ---


def test_near_geometry() -> None:
    """$near with GeoJSON point."""
    op = Near(
        geometry={"type": "Point", "coordinates": [-73.9667, 40.78]},
        max_distance=5000,
        min_distance=1000,
    )
    assert op.model_dump() == {
        "$near": {
            "$geometry": {"type": "Point", "coordinates": [-73.9667, 40.78]},
            "$maxDistance": 5000,
            "$minDistance": 1000,
        }
    }


def test_near_legacy() -> None:
    """$near with legacy coordinates."""
    op = Near(legacy_point=[-73.9667, 40.78], max_distance=5000)
    result = op.model_dump()
    assert result["$near"] == [-73.9667, 40.78]
    assert result["$maxDistance"] == 5000


def test_near_no_location() -> None:
    """$near with no location returns empty near."""
    op = Near()
    assert op.model_dump() == {"$near": {}}


# --- NearSphere Operator Tests ---


def test_near_sphere() -> None:
    """$nearSphere operator with GeoJSON point."""
    op = NearSphere(
        geometry={"type": "Point", "coordinates": [-73.9667, 40.78]},
        max_distance=5000,
    )
    assert op.model_dump() == {
        "$nearSphere": {
            "$geometry": {"type": "Point", "coordinates": [-73.9667, 40.78]},
            "$maxDistance": 5000,
        }
    }


def test_near_sphere_with_min_distance() -> None:
    """$nearSphere with min_distance."""
    op = NearSphere(
        geometry={"type": "Point", "coordinates": [0, 0]},
        max_distance=10000,
        min_distance=100,
    )
    result = op.model_dump()
    assert result["$nearSphere"]["$minDistance"] == 100
    assert result["$nearSphere"]["$maxDistance"] == 10000


def test_near_sphere_no_location() -> None:
    """$nearSphere with no location returns empty nearSphere."""
    op = NearSphere()
    assert op.model_dump() == {"$nearSphere": {}}

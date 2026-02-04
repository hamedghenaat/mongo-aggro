"""Tests for grouping and bucketing aggregation stages."""

import pytest
from pydantic import ValidationError

from mongo_aggro import Pipeline
from mongo_aggro.stages import Bucket, BucketAuto, Facet, Group, SortByCount

# --- SortByCount Tests ---


def test_sort_by_count() -> None:
    """SortByCount groups and counts."""
    sbc = SortByCount(field="category")
    assert sbc.model_dump() == {"$sortByCount": "$category"}


def test_sort_by_count_with_dollar() -> None:
    """SortByCount handles $ prefix."""
    sbc = SortByCount(field="$type")
    assert sbc.model_dump() == {"$sortByCount": "$type"}


def test_sort_by_count_missing_field() -> None:
    """SortByCount requires field parameter."""
    with pytest.raises(ValidationError):
        SortByCount()  # type: ignore[call-arg]


# --- Facet Tests ---


def test_facet_with_pipelines() -> None:
    """Facet with multiple pipelines."""
    facet = Facet(
        pipelines={
            "byCategory": Pipeline(
                [Group(id="$category", accumulators={"count": {"$sum": 1}})]
            ),
            "byYear": Pipeline(
                [
                    Group(
                        id="$year", accumulators={"total": {"$sum": "$amount"}}
                    )
                ]
            ),
        }
    )
    result = facet.model_dump()
    assert "$facet" in result
    assert "byCategory" in result["$facet"]
    assert "byYear" in result["$facet"]


def test_facet_with_list_pipelines() -> None:
    """Facet with pipelines as lists."""
    facet = Facet(pipelines={"total": [{"$count": "count"}]})
    result = facet.model_dump()
    assert result["$facet"]["total"] == [{"$count": "count"}]


def test_facet_empty_pipelines() -> None:
    """Facet with empty pipelines dict."""
    facet = Facet(pipelines={})
    result = facet.model_dump()
    assert result == {"$facet": {}}


def test_facet_missing_pipelines() -> None:
    """Facet requires pipelines parameter."""
    with pytest.raises(ValidationError):
        Facet()  # type: ignore[call-arg]


# --- Bucket Tests ---


def test_bucket() -> None:
    """Bucket with boundaries."""
    bucket = Bucket(
        group_by="$price",
        boundaries=[0, 100, 500, 1000],
        default="Other",
        output={"count": {"$sum": 1}},
    )
    result = bucket.model_dump()
    assert result == {
        "$bucket": {
            "groupBy": "$price",
            "boundaries": [0, 100, 500, 1000],
            "default": "Other",
            "output": {"count": {"$sum": 1}},
        }
    }


def test_bucket_minimal() -> None:
    """Bucket with only required fields."""
    bucket = Bucket(group_by="$age", boundaries=[0, 18, 65, 100])
    result = bucket.model_dump()
    assert result == {
        "$bucket": {
            "groupBy": "$age",
            "boundaries": [0, 18, 65, 100],
        }
    }


def test_bucket_missing_group_by() -> None:
    """Bucket requires group_by parameter."""
    with pytest.raises(ValidationError):
        Bucket(boundaries=[0, 100])  # type: ignore[call-arg]


def test_bucket_missing_boundaries() -> None:
    """Bucket requires boundaries parameter."""
    with pytest.raises(ValidationError):
        Bucket(group_by="$price")  # type: ignore[call-arg]


# --- BucketAuto Tests ---


def test_bucket_auto() -> None:
    """BucketAuto with buckets count."""
    bucket_auto = BucketAuto(group_by="$age", buckets=5)
    result = bucket_auto.model_dump()
    assert result == {
        "$bucketAuto": {
            "groupBy": "$age",
            "buckets": 5,
        }
    }


def test_bucket_auto_with_granularity() -> None:
    """BucketAuto with granularity."""
    bucket_auto = BucketAuto(
        group_by="$price",
        buckets=10,
        granularity="R5",
    )
    result = bucket_auto.model_dump()
    assert result["$bucketAuto"]["granularity"] == "R5"


def test_bucket_auto_with_output() -> None:
    """BucketAuto with output specification."""
    bucket_auto = BucketAuto(
        group_by="$score",
        buckets=4,
        output={"count": {"$sum": 1}, "avg": {"$avg": "$score"}},
    )
    result = bucket_auto.model_dump()
    assert result["$bucketAuto"]["output"] == {
        "count": {"$sum": 1},
        "avg": {"$avg": "$score"},
    }


def test_bucket_auto_missing_group_by() -> None:
    """BucketAuto requires group_by parameter."""
    with pytest.raises(ValidationError):
        BucketAuto(buckets=5)  # type: ignore[call-arg]


def test_bucket_auto_missing_buckets() -> None:
    """BucketAuto requires buckets parameter."""
    with pytest.raises(ValidationError):
        BucketAuto(group_by="$age")  # type: ignore[call-arg]


def test_bucket_auto_invalid_buckets() -> None:
    """BucketAuto buckets must be positive."""
    with pytest.raises(ValidationError):
        BucketAuto(group_by="$age", buckets=0)

    with pytest.raises(ValidationError):
        BucketAuto(group_by="$age", buckets=-1)

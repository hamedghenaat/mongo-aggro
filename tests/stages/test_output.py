"""Tests for output and sampling aggregation stages."""

import pytest
from pydantic import ValidationError

from mongo_aggro.stages import Documents, Merge, Out, Sample

# --- Sample Tests ---


def test_sample() -> None:
    """Sample random documents."""
    sample = Sample(size=10)
    assert sample.model_dump() == {"$sample": {"size": 10}}


def test_sample_validation_zero() -> None:
    """Sample size must be positive (rejects zero)."""
    with pytest.raises(ValidationError):
        Sample(size=0)


def test_sample_validation_negative() -> None:
    """Sample size must be positive (rejects negative)."""
    with pytest.raises(ValidationError):
        Sample(size=-5)


def test_sample_missing_size() -> None:
    """Sample requires size parameter."""
    with pytest.raises(ValidationError):
        Sample()  # type: ignore[call-arg]


# --- Out Tests ---


def test_out_simple() -> None:
    """Out to collection."""
    out = Out(collection="results")
    assert out.model_dump() == {"$out": "results"}


def test_out_with_db() -> None:
    """Out to collection in different database."""
    out = Out(collection="results", db="analytics")
    assert out.model_dump() == {"$out": {"db": "analytics", "coll": "results"}}


def test_out_missing_collection() -> None:
    """Out requires collection parameter."""
    with pytest.raises(ValidationError):
        Out()  # type: ignore[call-arg]


# --- Merge Tests ---


def test_merge_simple() -> None:
    """Simple merge."""
    merge = Merge(into="reports")
    assert merge.model_dump() == {"$merge": {"into": "reports"}}


def test_merge_full() -> None:
    """Merge with all options."""
    merge = Merge(
        into="reports",
        on="_id",
        when_matched="merge",
        when_not_matched="insert",
    )
    result = merge.model_dump()
    assert result == {
        "$merge": {
            "into": "reports",
            "on": "_id",
            "whenMatched": "merge",
            "whenNotMatched": "insert",
        }
    }


def test_merge_with_db_and_coll() -> None:
    """Merge into different database."""
    merge = Merge(into={"db": "analytics", "coll": "reports"})
    result = merge.model_dump()
    assert result["$merge"]["into"] == {"db": "analytics", "coll": "reports"}


def test_merge_with_on_array() -> None:
    """Merge with multiple on fields."""
    merge = Merge(into="reports", on=["category", "year"])
    result = merge.model_dump()
    assert result["$merge"]["on"] == ["category", "year"]


def test_merge_with_let() -> None:
    """Merge with let variables."""
    merge = Merge(
        into="reports",
        let={"incoming": "$$ROOT"},
        when_matched=[{"$set": {"updated": True}}],
    )
    result = merge.model_dump()
    assert result["$merge"]["let"] == {"incoming": "$$ROOT"}


def test_merge_missing_into() -> None:
    """Merge requires into parameter."""
    with pytest.raises(ValidationError):
        Merge()  # type: ignore[call-arg]


# --- Documents Tests ---


def test_documents() -> None:
    """Documents stage."""
    docs = Documents(
        documents=[
            {"x": 1, "y": 2},
            {"x": 3, "y": 4},
        ]
    )
    assert docs.model_dump() == {
        "$documents": [
            {"x": 1, "y": 2},
            {"x": 3, "y": 4},
        ]
    }


def test_documents_empty() -> None:
    """Documents with empty list."""
    docs = Documents(documents=[])
    assert docs.model_dump() == {"$documents": []}


def test_documents_single() -> None:
    """Documents with single document."""
    docs = Documents(documents=[{"id": 1}])
    assert docs.model_dump() == {"$documents": [{"id": 1}]}


def test_documents_missing_documents() -> None:
    """Documents requires documents parameter."""
    with pytest.raises(ValidationError):
        Documents()  # type: ignore[call-arg]

"""Tests for core aggregation stages."""

import pytest
from pydantic import ValidationError

from mongo_aggro.stages import Count, Group, Limit, Match, Project, Skip, Sort

# --- Match Tests ---


def test_match_simple_query() -> None:
    """Match with simple query."""
    match = Match(query={"status": "active"})
    assert match.model_dump() == {"$match": {"status": "active"}}


def test_match_comparison_operators() -> None:
    """Match with comparison operators."""
    match = Match(query={"age": {"$gt": 18, "$lt": 65}})
    assert match.model_dump() == {"$match": {"age": {"$gt": 18, "$lt": 65}}}


def test_match_logical_and() -> None:
    """Match with $and operator."""
    match = Match(
        query={
            "$and": [
                {"status": "active"},
                {"age": {"$gte": 18}},
            ]
        }
    )
    result = match.model_dump()
    assert result == {
        "$match": {
            "$and": [
                {"status": "active"},
                {"age": {"$gte": 18}},
            ]
        }
    }


def test_match_logical_or() -> None:
    """Match with $or operator."""
    match = Match(
        query={
            "$or": [
                {"type": "premium"},
                {"balance": {"$gt": 1000}},
            ]
        }
    )
    result = match.model_dump()
    assert result["$match"]["$or"] == [
        {"type": "premium"},
        {"balance": {"$gt": 1000}},
    ]


def test_match_nested_logical_operators() -> None:
    """Match with nested logical operators."""
    match = Match(
        query={
            "$and": [
                {"status": "active"},
                {"$or": [{"type": "A"}, {"type": "B"}]},
            ]
        }
    )
    result = match.model_dump()
    assert "$and" in result["$match"]
    assert "$or" in result["$match"]["$and"][1]


def test_match_missing_query() -> None:
    """Match requires query parameter."""
    with pytest.raises(ValidationError):
        Match()  # type: ignore[call-arg]


def test_match_rejects_extra_fields() -> None:
    """Match rejects unknown fields."""
    with pytest.raises(ValidationError):
        Match(query={"a": 1}, unknown_field="x")  # type: ignore[call-arg]


# --- Project Tests ---


def test_project_include_fields() -> None:
    """Project with field inclusion."""
    project = Project(fields={"name": 1, "email": 1, "_id": 0})
    assert project.model_dump() == {
        "$project": {"name": 1, "email": 1, "_id": 0}
    }


def test_project_computed_fields() -> None:
    """Project with computed fields."""
    project = Project(
        fields={"fullName": {"$concat": ["$firstName", " ", "$lastName"]}}
    )
    result = project.model_dump()
    assert result["$project"]["fullName"] == {
        "$concat": ["$firstName", " ", "$lastName"]
    }


def test_project_missing_fields() -> None:
    """Project requires fields parameter."""
    with pytest.raises(ValidationError):
        Project()  # type: ignore[call-arg]


# --- Group Tests ---


def test_group_simple() -> None:
    """Group by single field."""
    group = Group(id="$category", accumulators={"count": {"$sum": 1}})
    result = group.model_dump()
    assert result == {
        "$group": {
            "_id": "$category",
            "count": {"$sum": 1},
        }
    }


def test_group_null_id() -> None:
    """Group all documents (null _id)."""
    group = Group(id=None, accumulators={"total": {"$sum": "$amount"}})
    result = group.model_dump()
    assert result["$group"]["_id"] is None


def test_group_compound_id() -> None:
    """Group by compound key."""
    group = Group(
        id={"region": "$region", "year": "$year"},
        accumulators={"total": {"$sum": "$sales"}},
    )
    result = group.model_dump()
    assert result["$group"]["_id"] == {"region": "$region", "year": "$year"}


def test_group_multiple_accumulators() -> None:
    """Group with multiple accumulators."""
    group = Group(
        id="$category",
        accumulators={
            "count": {"$sum": 1},
            "total": {"$sum": "$amount"},
            "avg": {"$avg": "$amount"},
        },
    )
    result = group.model_dump()
    assert "count" in result["$group"]
    assert "total" in result["$group"]
    assert "avg" in result["$group"]


def test_group_missing_id() -> None:
    """Group requires id parameter."""
    with pytest.raises(ValidationError):
        Group(accumulators={"count": {"$sum": 1}})  # type: ignore[call-arg]


# --- Sort Tests ---


def test_sort_ascending() -> None:
    """Sort ascending."""
    sort = Sort(fields={"name": 1})
    assert sort.model_dump() == {"$sort": {"name": 1}}


def test_sort_descending() -> None:
    """Sort descending."""
    sort = Sort(fields={"createdAt": -1})
    assert sort.model_dump() == {"$sort": {"createdAt": -1}}


def test_sort_multiple_fields() -> None:
    """Sort by multiple fields."""
    sort = Sort(fields={"category": 1, "price": -1})
    assert sort.model_dump() == {"$sort": {"category": 1, "price": -1}}


def test_sort_invalid_direction() -> None:
    """Sort direction must be 1 or -1."""
    with pytest.raises(ValidationError):
        Sort(fields={"name": 2})  # type: ignore[dict-item]


def test_sort_missing_fields() -> None:
    """Sort requires fields parameter."""
    with pytest.raises(ValidationError):
        Sort()  # type: ignore[call-arg]


# --- Limit Tests ---


def test_limit() -> None:
    """Limit number of documents."""
    limit = Limit(count=10)
    assert limit.model_dump() == {"$limit": 10}


def test_limit_validation_zero() -> None:
    """Limit must be positive (rejects zero)."""
    with pytest.raises(ValidationError):
        Limit(count=0)


def test_limit_validation_negative() -> None:
    """Limit must be positive (rejects negative)."""
    with pytest.raises(ValidationError):
        Limit(count=-5)


def test_limit_missing_count() -> None:
    """Limit requires count parameter."""
    with pytest.raises(ValidationError):
        Limit()  # type: ignore[call-arg]


# --- Skip Tests ---


def test_skip() -> None:
    """Skip documents."""
    skip = Skip(count=5)
    assert skip.model_dump() == {"$skip": 5}


def test_skip_zero() -> None:
    """Skip zero is valid."""
    skip = Skip(count=0)
    assert skip.model_dump() == {"$skip": 0}


def test_skip_validation() -> None:
    """Skip must be non-negative."""
    with pytest.raises(ValidationError):
        Skip(count=-1)


def test_skip_missing_count() -> None:
    """Skip requires count parameter."""
    with pytest.raises(ValidationError):
        Skip()  # type: ignore[call-arg]


# --- Count Tests ---


def test_count() -> None:
    """Count documents."""
    count = Count(field="total")
    assert count.model_dump() == {"$count": "total"}


def test_count_missing_field() -> None:
    """Count requires field parameter."""
    with pytest.raises(ValidationError):
        Count()  # type: ignore[call-arg]

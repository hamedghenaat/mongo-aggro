"""Tests for join-related aggregation stages."""

import pytest
from pydantic import ValidationError

from mongo_aggro import Pipeline
from mongo_aggro.stages import GraphLookup, Lookup, Match, UnionWith

# --- Lookup Tests ---


def test_lookup_simple() -> None:
    """Simple equality lookup."""
    lookup = Lookup(
        from_collection="products",
        local_field="productId",
        foreign_field="_id",
        as_field="product",
    )
    result = lookup.model_dump()
    assert result == {
        "$lookup": {
            "from": "products",
            "localField": "productId",
            "foreignField": "_id",
            "as": "product",
        }
    }


def test_lookup_with_pipeline() -> None:
    """Lookup with nested pipeline."""
    lookup = Lookup(
        from_collection="orders",
        let={"customerId": "$_id"},
        pipeline=Pipeline(
            [Match(query={"$expr": {"$eq": ["$customerId", "$$customerId"]}})]
        ),
        as_field="orders",
    )
    result = lookup.model_dump()
    assert result["$lookup"]["from"] == "orders"
    assert result["$lookup"]["let"] == {"customerId": "$_id"}
    assert "pipeline" in result["$lookup"]
    assert result["$lookup"]["as"] == "orders"


def test_lookup_pipeline_as_list() -> None:
    """Lookup with pipeline as list of dicts."""
    lookup = Lookup(
        from_collection="orders",
        pipeline=[{"$match": {"status": "active"}}],
        as_field="activeOrders",
    )
    result = lookup.model_dump()
    assert result["$lookup"]["pipeline"] == [{"$match": {"status": "active"}}]


def test_lookup_missing_required_fields() -> None:
    """Lookup requires from_collection and as_field."""
    with pytest.raises(ValidationError):
        Lookup(from_collection="orders")  # type: ignore[call-arg]

    with pytest.raises(ValidationError):
        Lookup(as_field="result")  # type: ignore[call-arg]


def test_lookup_rejects_extra_fields() -> None:
    """Lookup rejects unknown fields."""
    with pytest.raises(ValidationError):
        Lookup(
            from_collection="products",
            as_field="product",
            unknown="x",  # type: ignore[call-arg]
        )


# --- UnionWith Tests ---


def test_union_simple() -> None:
    """Simple union."""
    union = UnionWith(collection="archive")
    assert union.model_dump() == {"$unionWith": "archive"}


def test_union_with_pipeline() -> None:
    """Union with pipeline."""
    union = UnionWith(
        collection="archive",
        pipeline=Pipeline([Match(query={"year": 2023})]),
    )
    result = union.model_dump()
    assert result == {
        "$unionWith": {
            "coll": "archive",
            "pipeline": [{"$match": {"year": 2023}}],
        }
    }


def test_union_with_list_pipeline() -> None:
    """Union with pipeline as list of dicts."""
    union = UnionWith(
        collection="archive",
        pipeline=[{"$match": {"status": "complete"}}],
    )
    result = union.model_dump()
    assert result["$unionWith"]["pipeline"] == [
        {"$match": {"status": "complete"}}
    ]


def test_union_missing_collection() -> None:
    """UnionWith requires collection parameter."""
    with pytest.raises(ValidationError):
        UnionWith()  # type: ignore[call-arg]


# --- GraphLookup Tests ---


def test_graph_lookup() -> None:
    """GraphLookup stage."""
    graph = GraphLookup(
        from_collection="employees",
        start_with="$reportsTo",
        connect_from_field="reportsTo",
        connect_to_field="name",
        as_field="hierarchy",
        max_depth=5,
    )
    result = graph.model_dump()
    assert result == {
        "$graphLookup": {
            "from": "employees",
            "startWith": "$reportsTo",
            "connectFromField": "reportsTo",
            "connectToField": "name",
            "as": "hierarchy",
            "maxDepth": 5,
        }
    }


def test_graph_lookup_with_depth_field() -> None:
    """GraphLookup with depth field."""
    graph = GraphLookup(
        from_collection="categories",
        start_with="$parent",
        connect_from_field="parent",
        connect_to_field="_id",
        as_field="ancestors",
        depth_field="level",
    )
    result = graph.model_dump()
    assert result["$graphLookup"]["depthField"] == "level"


def test_graph_lookup_with_restrict_match() -> None:
    """GraphLookup with restrictSearchWithMatch."""
    graph = GraphLookup(
        from_collection="nodes",
        start_with="$start",
        connect_from_field="next",
        connect_to_field="_id",
        as_field="path",
        restrict_search_with_match={"active": True},
    )
    result = graph.model_dump()
    assert result["$graphLookup"]["restrictSearchWithMatch"] == {
        "active": True
    }


def test_graph_lookup_missing_required() -> None:
    """GraphLookup requires all mandatory fields."""
    with pytest.raises(ValidationError):
        GraphLookup(
            from_collection="nodes",
            start_with="$x",
            connect_from_field="a",
            # missing connect_to_field and as_field
        )  # type: ignore[call-arg]

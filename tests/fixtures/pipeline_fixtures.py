"""Pipeline-related test fixtures."""

import pytest

from mongo_aggro import (
    Avg,
    Facet,
    Group,
    Limit,
    Lookup,
    Match,
    Pipeline,
    Project,
    Sort,
    Sum,
    Unwind,
    merge_accumulators,
)


@pytest.fixture
def empty_pipeline() -> Pipeline:
    """Return an empty pipeline."""
    return Pipeline()


@pytest.fixture
def sample_match_stage() -> Match:
    """Return a sample Match stage."""
    return Match(query={"status": "active"})


@pytest.fixture
def sample_stages() -> list:
    """Return a list of sample stages."""
    return [
        Match(query={"status": "active"}),
        Unwind(path="items"),
        Group(id="$category", accumulators={"count": {"$sum": 1}}),
        Sort(fields={"count": -1}),
        Limit(count=10),
    ]


@pytest.fixture
def basic_pipeline(sample_stages: list) -> Pipeline:
    """Return a basic pipeline with common stages."""
    return Pipeline(sample_stages)


@pytest.fixture
def complex_pipeline() -> Pipeline:
    """Return a complex pipeline with accumulators."""
    return Pipeline(
        [
            Match(
                query={
                    "$and": [
                        {"status": {"$in": ["active", "pending"]}},
                        {"createdAt": {"$gte": "2024-01-01"}},
                    ]
                }
            ),
            Unwind(path="items"),
            Group(
                id={"category": "$category", "region": "$region"},
                accumulators=merge_accumulators(
                    Sum(name="totalQuantity", field="items.quantity"),
                    Sum(name="totalRevenue", field="items.subtotal"),
                    Avg(name="avgPrice", field="items.price"),
                    Sum(name="orderCount", value=1),
                ),
            ),
            Match(query={"totalRevenue": {"$gt": 1000}}),
            Sort(fields={"totalRevenue": -1}),
            Limit(count=20),
            Project(
                fields={
                    "_id": 0,
                    "category": "$_id.category",
                    "region": "$_id.region",
                    "totalRevenue": 1,
                    "orderCount": 1,
                }
            ),
        ]
    )


@pytest.fixture
def lookup_pipeline() -> Pipeline:
    """Return a pipeline with lookup stage."""
    return Pipeline(
        [
            Match(query={"type": "customer"}),
            Lookup(
                from_collection="orders",
                let={"customerId": "$_id"},
                pipeline=Pipeline(
                    [
                        Match(
                            query={
                                "$expr": {
                                    "$eq": ["$customerId", "$$customerId"]
                                },
                            }
                        ),
                        Sort(fields={"orderDate": -1}),
                        Limit(count=5),
                    ]
                ),
                as_field="recentOrders",
            ),
            Project(fields={"name": 1, "email": 1, "recentOrders": 1}),
        ]
    )


@pytest.fixture
def facet_pipeline() -> Pipeline:
    """Return a pipeline with facet stage."""
    return Pipeline(
        [
            Match(query={"status": "active"}),
            Facet(
                pipelines={
                    "byCategory": Pipeline(
                        [
                            Group(
                                id="$category",
                                accumulators=merge_accumulators(
                                    Sum(name="count", value=1),
                                ),
                            ),
                            Sort(fields={"count": -1}),
                        ]
                    ),
                    "byRegion": Pipeline(
                        [
                            Group(
                                id="$region",
                                accumulators=merge_accumulators(
                                    Sum(name="count", value=1),
                                    Avg(name="avgAmount", field="amount"),
                                ),
                            ),
                        ]
                    ),
                }
            ),
        ]
    )

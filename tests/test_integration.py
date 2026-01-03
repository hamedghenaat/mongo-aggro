"""Integration tests for complete pipelines."""

from mongo_aggro import (
    Avg,
    Count,
    Group,
    Limit,
    Lookup,
    Match,
    Pipeline,
    Project,
    Skip,
    Sort,
    Sum,
    Unwind,
    merge_accumulators,
)


def test_basic_aggregation_pipeline(basic_pipeline: Pipeline) -> None:
    """Basic match -> group -> sort -> limit pipeline."""
    stages = basic_pipeline.to_list()
    assert len(stages) == 5
    assert "$match" in stages[0]
    assert "$unwind" in stages[1]
    assert "$group" in stages[2]
    assert "$sort" in stages[3]
    assert "$limit" in stages[4]


def test_complex_pipeline_structure(complex_pipeline: Pipeline) -> None:
    """Complex pipeline with accumulators."""
    stages = complex_pipeline.to_list()
    assert len(stages) == 7

    # Verify first stage has complex match
    assert "$and" in stages[0]["$match"]

    # Verify group stage has accumulators
    group_stage = stages[2]["$group"]
    assert "totalQuantity" in group_stage
    assert "totalRevenue" in group_stage
    assert "avgPrice" in group_stage
    assert "orderCount" in group_stage


def test_lookup_pipeline_structure(lookup_pipeline: Pipeline) -> None:
    """Pipeline with lookup stage."""
    stages = lookup_pipeline.to_list()
    assert len(stages) == 3

    lookup_stage = stages[1]["$lookup"]
    assert lookup_stage["from"] == "orders"
    assert "let" in lookup_stage
    assert "pipeline" in lookup_stage
    assert len(lookup_stage["pipeline"]) == 3


def test_facet_pipeline_structure(facet_pipeline: Pipeline) -> None:
    """Pipeline with facet stage."""
    stages = facet_pipeline.to_list()
    assert len(stages) == 2

    facet_stage = stages[1]["$facet"]
    assert "byCategory" in facet_stage
    assert "byRegion" in facet_stage


def test_pagination_pipeline() -> None:
    """Pipeline with skip and limit for pagination."""
    page = 3
    page_size = 20
    skip_count = (page - 1) * page_size

    pipeline = Pipeline(
        [
            Match(query={"active": True}),
            Sort(fields={"createdAt": -1}),
            Skip(count=skip_count),
            Limit(count=page_size),
        ]
    )

    stages = pipeline.to_list()
    assert stages[2] == {"$skip": 40}
    assert stages[3] == {"$limit": 20}


def test_method_chaining_pipeline() -> None:
    """Pipeline built using method chaining."""
    pipeline = (
        Pipeline()
        .add_stage(Match(query={"status": "active"}))
        .add_stage(
            Group(
                id="$category",
                accumulators=merge_accumulators(
                    Sum(name="count", value=1),
                ),
            )
        )
        .add_stage(Sort(fields={"count": -1}))
        .add_stage(Limit(count=5))
    )

    assert len(pipeline) == 4
    stages = pipeline.to_list()
    assert stages[0] == {"$match": {"status": "active"}}
    assert stages[3] == {"$limit": 5}


def test_complex_match_conditions() -> None:
    """Pipeline with complex match conditions."""
    pipeline = Pipeline(
        [
            Match(
                query={
                    "$and": [
                        {"status": {"$in": ["active", "pending"]}},
                        {"createdAt": {"$gte": "2024-01-01"}},
                        {
                            "$or": [
                                {"priority": "high"},
                                {"amount": {"$gt": 1000}},
                            ]
                        },
                    ]
                }
            ),
            Count(field="matchingCount"),
        ]
    )

    stages = pipeline.to_list()
    match_query = stages[0]["$match"]
    assert "$and" in match_query
    assert len(match_query["$and"]) == 3


# --- Pipeline Iterability Tests ---


def test_pipeline_is_iterable(basic_pipeline: Pipeline) -> None:
    """Pipeline can be iterated like a list."""
    stages_list = []
    for stage in basic_pipeline:
        stages_list.append(stage)

    assert len(stages_list) == 5
    assert all(isinstance(s, dict) for s in stages_list)


def test_pipeline_multiple_iterations() -> None:
    """Pipeline can be iterated multiple times."""
    pipeline = Pipeline([Match(query={"x": 1})])

    first = list(pipeline)
    second = list(pipeline)
    third = list(pipeline)

    assert first == second == third


def test_empty_pipeline_iteration(empty_pipeline: Pipeline) -> None:
    """Empty pipeline iteration works."""
    stages = list(empty_pipeline)
    assert stages == []

    # Can still add stages after iteration
    empty_pipeline.add_stage(Match(query={"a": 1}))
    assert list(empty_pipeline) == [{"$match": {"a": 1}}]


def test_ecommerce_analytics_pipeline() -> None:
    """E-commerce order analytics pipeline."""
    pipeline = Pipeline(
        [
            Match(
                query={
                    "orderDate": {"$gte": "2024-01-01"},
                    "status": {"$ne": "cancelled"},
                }
            ),
            Unwind(path="items"),
            Group(
                id="$items.productId",
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
                    "productId": "$_id",
                    "totalQuantity": 1,
                    "totalRevenue": 1,
                    "avgPrice": {"$round": ["$avgPrice", 2]},
                    "orderCount": 1,
                }
            ),
        ]
    )

    stages = pipeline.to_list()
    assert len(stages) == 7

    # Verify group stage
    group_stage = stages[2]["$group"]
    assert group_stage["_id"] == "$items.productId"
    assert "totalQuantity" in group_stage
    assert "totalRevenue" in group_stage


def test_lookup_with_unwind_pipeline() -> None:
    """Pipeline with lookup and unwind."""
    pipeline = Pipeline(
        [
            Match(query={"status": "active"}),
            Lookup(
                from_collection="customers",
                local_field="customerId",
                foreign_field="_id",
                as_field="customer",
            ),
            Unwind(path="customer"),
            Project(
                fields={
                    "orderId": 1,
                    "customerName": "$customer.name",
                    "customerEmail": "$customer.email",
                    "total": 1,
                }
            ),
        ]
    )

    stages = pipeline.to_list()
    assert len(stages) == 4

    lookup_stage = stages[1]["$lookup"]
    assert lookup_stage["from"] == "customers"
    assert lookup_stage["localField"] == "customerId"
    assert lookup_stage["foreignField"] == "_id"
    assert lookup_stage["as"] == "customer"

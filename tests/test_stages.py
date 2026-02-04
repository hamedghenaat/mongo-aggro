"""Tests for aggregation stage classes."""

import pytest

from mongo_aggro import (
    AddFields,
    Bucket,
    BucketAuto,
    Count,
    Densify,
    Documents,
    Facet,
    Fill,
    GeoNear,
    GraphLookup,
    Group,
    Limit,
    Lookup,
    Match,
    Merge,
    Out,
    Pipeline,
    Project,
    Redact,
    ReplaceRoot,
    ReplaceWith,
    Sample,
    Set,
    SetWindowFields,
    Skip,
    Sort,
    SortByCount,
    UnionWith,
    Unset,
    Unwind,
)

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


# --- Limit Tests ---


def test_limit() -> None:
    """Limit number of documents."""
    limit = Limit(count=10)
    assert limit.model_dump() == {"$limit": 10}


def test_limit_validation() -> None:
    """Limit must be positive."""
    with pytest.raises(ValueError):
        Limit(count=0)
    with pytest.raises(ValueError):
        Limit(count=-5)


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
    with pytest.raises(ValueError):
        Skip(count=-1)


# --- Unwind Tests ---


def test_unwind_simple() -> None:
    """Simple unwind without options."""
    unwind = Unwind(path="items")
    assert unwind.model_dump() == {"$unwind": "$items"}


def test_unwind_with_dollar() -> None:
    """Unwind path already has $."""
    unwind = Unwind(path="$items")
    assert unwind.model_dump() == {"$unwind": "$items"}


def test_unwind_with_index() -> None:
    """Unwind with includeArrayIndex."""
    unwind = Unwind(path="items", include_array_index="idx")
    result = unwind.model_dump()
    assert result == {
        "$unwind": {
            "path": "$items",
            "includeArrayIndex": "idx",
        }
    }


def test_unwind_preserve_null() -> None:
    """Unwind with preserveNullAndEmptyArrays."""
    unwind = Unwind(path="items", preserve_null_and_empty=True)
    result = unwind.model_dump()
    assert result["$unwind"]["preserveNullAndEmptyArrays"] is True


def test_unwind_all_options() -> None:
    """Unwind with all options."""
    unwind = Unwind(
        path="items",
        include_array_index="itemIndex",
        preserve_null_and_empty=True,
    )
    result = unwind.model_dump()
    assert result == {
        "$unwind": {
            "path": "$items",
            "includeArrayIndex": "itemIndex",
            "preserveNullAndEmptyArrays": True,
        }
    }


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


# --- AddFields and Set Tests ---


def test_add_fields() -> None:
    """AddFields adds new fields."""
    add_fields = AddFields(fields={"isActive": True, "score": 100})
    assert add_fields.model_dump() == {
        "$addFields": {"isActive": True, "score": 100}
    }


def test_set_fields() -> None:
    """Set is alias for AddFields."""
    set_stage = Set(fields={"status": "processed"})
    assert set_stage.model_dump() == {"$set": {"status": "processed"}}


# --- Unset Tests ---


def test_unset_single() -> None:
    """Unset single field."""
    unset = Unset(fields="password")
    assert unset.model_dump() == {"$unset": "password"}


def test_unset_multiple() -> None:
    """Unset multiple fields."""
    unset = Unset(fields=["password", "secret", "token"])
    assert unset.model_dump() == {"$unset": ["password", "secret", "token"]}


# --- Count Tests ---


def test_count() -> None:
    """Count documents."""
    count = Count(field="total")
    assert count.model_dump() == {"$count": "total"}


# --- SortByCount Tests ---


def test_sort_by_count() -> None:
    """SortByCount groups and counts."""
    sbc = SortByCount(field="category")
    assert sbc.model_dump() == {"$sortByCount": "$category"}


def test_sort_by_count_with_dollar() -> None:
    """SortByCount handles $ prefix."""
    sbc = SortByCount(field="$type")
    assert sbc.model_dump() == {"$sortByCount": "$type"}


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


# --- ReplaceRoot Tests ---


def test_replace_root() -> None:
    """ReplaceRoot with field path."""
    rr = ReplaceRoot(new_root="$nested")
    assert rr.model_dump() == {"$replaceRoot": {"newRoot": "$nested"}}


def test_replace_root_expression() -> None:
    """ReplaceRoot with expression."""
    rr = ReplaceRoot(new_root={"$mergeObjects": ["$defaults", "$doc"]})
    result = rr.model_dump()
    assert result["$replaceRoot"]["newRoot"] == {
        "$mergeObjects": ["$defaults", "$doc"]
    }


# --- ReplaceWith Tests ---


def test_replace_with() -> None:
    """ReplaceWith stage."""
    rw = ReplaceWith(expression="$embedded")
    assert rw.model_dump() == {"$replaceWith": "$embedded"}


# --- Sample Tests ---


def test_sample() -> None:
    """Sample random documents."""
    sample = Sample(size=10)
    assert sample.model_dump() == {"$sample": {"size": 10}}


def test_sample_validation() -> None:
    """Sample size must be positive."""
    with pytest.raises(ValueError):
        Sample(size=0)


# --- Out Tests ---


def test_out_simple() -> None:
    """Out to collection."""
    out = Out(collection="results")
    assert out.model_dump() == {"$out": "results"}


def test_out_with_db() -> None:
    """Out to collection in different database."""
    out = Out(collection="results", db="analytics")
    assert out.model_dump() == {"$out": {"db": "analytics", "coll": "results"}}


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


# --- Redact Tests ---


def test_redact() -> None:
    """Redact stage."""
    redact = Redact(
        expression={
            "$cond": {
                "if": {"$eq": ["$level", 5]},
                "then": "$$PRUNE",
                "else": "$$DESCEND",
            }
        }
    )
    result = redact.model_dump()
    assert "$redact" in result
    assert "$cond" in result["$redact"]


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


# --- GeoNear Tests ---


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


# --- SetWindowFields Tests ---


def test_set_window_fields() -> None:
    """SetWindowFields stage."""
    swf = SetWindowFields(
        partition_by="$state",
        sort_by={"date": 1},
        output={
            "cumulative": {
                "$sum": "$quantity",
                "window": {"documents": ["unbounded", "current"]},
            }
        },
    )
    result = swf.model_dump()
    assert result["$setWindowFields"]["partitionBy"] == "$state"
    assert result["$setWindowFields"]["sortBy"] == {"date": 1}
    assert "cumulative" in result["$setWindowFields"]["output"]


# --- Densify Tests ---


def test_densify() -> None:
    """Densify stage."""
    densify = Densify(
        field="date",
        range={"step": 1, "unit": "day", "bounds": "full"},
    )
    result = densify.model_dump()
    assert result == {
        "$densify": {
            "field": "date",
            "range": {"step": 1, "unit": "day", "bounds": "full"},
        }
    }


# --- Fill Tests ---


def test_fill() -> None:
    """Fill stage."""
    fill = Fill(
        sort_by={"date": 1},
        output={
            "score": {"method": "linear"},
            "status": {"value": "unknown"},
        },
    )
    result = fill.model_dump()
    assert result["$fill"]["sortBy"] == {"date": 1}
    assert "score" in result["$fill"]["output"]


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


# --- Statistics Stage Tests ---


def test_coll_stats_latency() -> None:
    """CollStats with latency stats."""
    from mongo_aggro import CollStats

    stats = CollStats(lat_stats={"histograms": True})
    assert stats.model_dump() == {
        "$collStats": {"latencyStats": {"histograms": True}}
    }


def test_coll_stats_storage() -> None:
    """CollStats with storage stats."""
    from mongo_aggro import CollStats

    stats = CollStats(storage_stats={})
    assert stats.model_dump() == {"$collStats": {"storageStats": {}}}


def test_coll_stats_count() -> None:
    """CollStats with count."""
    from mongo_aggro import CollStats

    stats = CollStats(count={})
    assert stats.model_dump() == {"$collStats": {"count": {}}}


def test_coll_stats_multiple() -> None:
    """CollStats with multiple options."""
    from mongo_aggro import CollStats

    stats = CollStats(
        lat_stats={"histograms": True},
        storage_stats={},
        count={},
    )
    result = stats.model_dump()
    assert result == {
        "$collStats": {
            "latencyStats": {"histograms": True},
            "storageStats": {},
            "count": {},
        }
    }


def test_index_stats() -> None:
    """IndexStats stage."""
    from mongo_aggro import IndexStats

    stats = IndexStats()
    assert stats.model_dump() == {"$indexStats": {}}


def test_plan_cache_stats() -> None:
    """PlanCacheStats stage."""
    from mongo_aggro import PlanCacheStats

    stats = PlanCacheStats()
    assert stats.model_dump() == {"$planCacheStats": {}}


# --- Session Stage Tests ---


def test_list_sessions_empty() -> None:
    """ListSessions with no filters."""
    from mongo_aggro import ListSessions

    sessions = ListSessions()
    assert sessions.model_dump() == {"$listSessions": {}}


def test_list_sessions_users() -> None:
    """ListSessions with users filter."""
    from mongo_aggro import ListSessions

    sessions = ListSessions(users=[{"user": "admin", "db": "admin"}])
    assert sessions.model_dump() == {
        "$listSessions": {"users": [{"user": "admin", "db": "admin"}]}
    }


def test_list_sessions_all_users() -> None:
    """ListSessions with allUsers."""
    from mongo_aggro import ListSessions

    sessions = ListSessions(all_users=True)
    assert sessions.model_dump() == {"$listSessions": {"allUsers": True}}


def test_list_local_sessions() -> None:
    """ListLocalSessions stage."""
    from mongo_aggro import ListLocalSessions

    sessions = ListLocalSessions(all_users=True)
    assert sessions.model_dump() == {"$listLocalSessions": {"allUsers": True}}


def test_list_sampled_queries() -> None:
    """ListSampledQueries stage."""
    from mongo_aggro import ListSampledQueries

    queries = ListSampledQueries(namespace="test.users")
    assert queries.model_dump() == {
        "$listSampledQueries": {"namespace": "test.users"}
    }


# --- Change Stream Stage Tests ---


def test_change_stream_empty() -> None:
    """ChangeStream with no options."""
    from mongo_aggro import ChangeStream

    stream = ChangeStream()
    assert stream.model_dump() == {"$changeStream": {}}


def test_change_stream_full_document() -> None:
    """ChangeStream with fullDocument option."""
    from mongo_aggro import ChangeStream

    stream = ChangeStream(full_document="updateLookup")
    assert stream.model_dump() == {
        "$changeStream": {"fullDocument": "updateLookup"}
    }


def test_change_stream_options() -> None:
    """ChangeStream with multiple options."""
    from mongo_aggro import ChangeStream

    stream = ChangeStream(
        full_document="whenAvailable",
        full_document_before_change="required",
        show_expanded_events=True,
    )
    assert stream.model_dump() == {
        "$changeStream": {
            "fullDocument": "whenAvailable",
            "fullDocumentBeforeChange": "required",
            "showExpandedEvents": True,
        }
    }


def test_change_stream_split_large_event() -> None:
    """ChangeStreamSplitLargeEvent stage."""
    from mongo_aggro import ChangeStreamSplitLargeEvent

    split = ChangeStreamSplitLargeEvent()
    assert split.model_dump() == {"$changeStreamSplitLargeEvent": {}}


# --- Admin Stage Tests ---


def test_current_op_empty() -> None:
    """CurrentOp with no options."""
    from mongo_aggro import CurrentOp

    op = CurrentOp()
    assert op.model_dump() == {"$currentOp": {}}


def test_current_op_options() -> None:
    """CurrentOp with options."""
    from mongo_aggro import CurrentOp

    op = CurrentOp(all_users=True, idle_connections=True)
    assert op.model_dump() == {
        "$currentOp": {"allUsers": True, "idleConnections": True}
    }


def test_list_cluster_catalog() -> None:
    """ListClusterCatalog stage."""
    from mongo_aggro import ListClusterCatalog

    catalog = ListClusterCatalog()
    assert catalog.model_dump() == {"$listClusterCatalog": {}}


def test_list_search_indexes_empty() -> None:
    """ListSearchIndexes with no filter."""
    from mongo_aggro import ListSearchIndexes

    indexes = ListSearchIndexes()
    assert indexes.model_dump() == {"$listSearchIndexes": {}}


def test_list_search_indexes_by_name() -> None:
    """ListSearchIndexes by name."""
    from mongo_aggro import ListSearchIndexes

    indexes = ListSearchIndexes(name="my_index")
    assert indexes.model_dump() == {"$listSearchIndexes": {"name": "my_index"}}


# --- Atlas Search Stage Tests ---


def test_search_text() -> None:
    """Search with text operator."""
    from mongo_aggro import Search

    search = Search(index="default", text={"query": "coffee", "path": "title"})
    assert search.model_dump() == {
        "$search": {
            "index": "default",
            "text": {"query": "coffee", "path": "title"},
        }
    }


def test_search_compound() -> None:
    """Search with compound operator."""
    from mongo_aggro import Search

    search = Search(
        index="default",
        compound={
            "must": [{"text": {"query": "coffee", "path": "title"}}],
            "should": [{"text": {"query": "organic", "path": "description"}}],
        },
    )
    assert search.model_dump() == {
        "$search": {
            "index": "default",
            "compound": {
                "must": [{"text": {"query": "coffee", "path": "title"}}],
                "should": [
                    {"text": {"query": "organic", "path": "description"}}
                ],
            },
        }
    }


def test_search_meta() -> None:
    """SearchMeta stage."""
    from mongo_aggro import SearchMeta

    meta = SearchMeta(index="default", count={"type": "total"})
    assert meta.model_dump() == {
        "$searchMeta": {"index": "default", "count": {"type": "total"}}
    }


def test_vector_search() -> None:
    """VectorSearch stage."""
    from mongo_aggro import VectorSearch

    search = VectorSearch(
        index="vector_index",
        path="embedding",
        query_vector=[0.1, 0.2, 0.3],
        num_candidates=100,
        limit=10,
    )
    assert search.model_dump() == {
        "$vectorSearch": {
            "index": "vector_index",
            "path": "embedding",
            "queryVector": [0.1, 0.2, 0.3],
            "numCandidates": 100,
            "limit": 10,
        }
    }


def test_vector_search_with_filter() -> None:
    """VectorSearch with filter."""
    from mongo_aggro import VectorSearch

    search = VectorSearch(
        index="vector_index",
        path="embedding",
        query_vector=[0.1, 0.2, 0.3],
        num_candidates=100,
        limit=10,
        filter={"category": "tech"},
    )
    assert search.model_dump() == {
        "$vectorSearch": {
            "index": "vector_index",
            "path": "embedding",
            "queryVector": [0.1, 0.2, 0.3],
            "numCandidates": 100,
            "limit": 10,
            "filter": {"category": "tech"},
        }
    }


# --- Advanced Stage Tests ---


def test_query_settings() -> None:
    """QuerySettings stage."""
    from mongo_aggro import QuerySettings

    settings = QuerySettings()
    assert settings.model_dump() == {"$querySettings": {}}


def test_rank_fusion() -> None:
    """RankFusion stage."""
    from mongo_aggro import RankFusion

    fusion = RankFusion(
        input={
            "search": [{"$match": {"status": "active"}}],
            "vector": [{"$match": {"category": "tech"}}],
        },
        combination={"weights": {"search": 0.7, "vector": 0.3}},
    )
    assert fusion.model_dump() == {
        "$rankFusion": {
            "input": {
                "search": [{"$match": {"status": "active"}}],
                "vector": [{"$match": {"category": "tech"}}],
            },
            "combination": {"weights": {"search": 0.7, "vector": 0.3}},
        }
    }

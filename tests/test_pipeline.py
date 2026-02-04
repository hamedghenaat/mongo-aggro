"""Tests for Pipeline class."""

import pytest

from mongo_aggro import ASCENDING, DESCENDING, Match, Pipeline, Sort, Unwind

# --- Initialization Tests ---


def test_pipeline_init_empty() -> None:
    """Pipeline can be initialized without stages."""
    pipeline = Pipeline()
    assert len(pipeline) == 0


def test_pipeline_init_with_stages() -> None:
    """Pipeline can be initialized with a list of stages."""
    pipeline = Pipeline(
        [
            Match(query={"status": "active"}),
            Unwind(path="items"),
        ]
    )
    assert len(pipeline) == 2


def test_pipeline_init_with_none() -> None:
    """Pipeline handles None as empty list."""
    pipeline = Pipeline(None)
    assert len(pipeline) == 0


# --- Sort Direction Constants Tests ---


def test_sort_with_constants() -> None:
    """Sort stage works with direction constants."""
    sort_stage = Sort(fields={"created_at": DESCENDING, "name": ASCENDING})
    result = sort_stage.model_dump()
    assert result == {"$sort": {"created_at": -1, "name": 1}}


def test_with_sort_using_constants() -> None:
    """with_sort works with direction constants."""
    pipeline = Pipeline([Match(query={"status": "active"})])
    result = pipeline.with_sort({"total": DESCENDING, "name": ASCENDING})
    assert result[1] == {"total": -1, "name": 1}


# --- add_stage Tests ---


def test_add_stage_returns_pipeline(empty_pipeline: Pipeline) -> None:
    """add_stage returns the pipeline for chaining."""
    result = empty_pipeline.add_stage(Match(query={"a": 1}))
    assert result is empty_pipeline


def test_add_stage_appends_to_end(empty_pipeline: Pipeline) -> None:
    """add_stage appends stages to the end."""
    empty_pipeline.add_stage(Match(query={"first": True}))
    empty_pipeline.add_stage(Match(query={"second": True}))
    assert len(empty_pipeline) == 2
    stages = list(empty_pipeline)
    assert stages[0] == {"$match": {"first": True}}
    assert stages[1] == {"$match": {"second": True}}


def test_method_chaining() -> None:
    """Multiple add_stage calls can be chained."""
    pipeline = (
        Pipeline()
        .add_stage(Match(query={"a": 1}))
        .add_stage(Unwind(path="items"))
        .add_stage(Match(query={"b": 2}))
    )
    assert len(pipeline) == 3


# --- Iteration Tests ---


def test_iter_empty_pipeline(empty_pipeline: Pipeline) -> None:
    """Empty pipeline yields no items."""
    stages = list(empty_pipeline)
    assert stages == []


def test_iter_yields_dicts(basic_pipeline: Pipeline) -> None:
    """Iteration yields dictionary representations."""
    stages = list(basic_pipeline)
    assert len(stages) == 5
    assert all(isinstance(s, dict) for s in stages)
    assert "$match" in stages[0]
    assert "$unwind" in stages[1]


def test_iter_multiple_times() -> None:
    """Pipeline can be iterated multiple times."""
    pipeline = Pipeline([Match(query={"a": 1})])
    first = list(pipeline)
    second = list(pipeline)
    assert first == second == [{"$match": {"a": 1}}]


# --- __len__ Tests ---


def test_len_empty(empty_pipeline: Pipeline) -> None:
    """Empty pipeline has length 0."""
    assert len(empty_pipeline) == 0


def test_len_with_stages(basic_pipeline: Pipeline) -> None:
    """Pipeline length equals number of stages."""
    assert len(basic_pipeline) == 5


# --- __getitem__ Tests ---


def test_getitem_returns_stage(sample_match_stage: Match) -> None:
    """Indexing returns the stage object."""
    pipeline = Pipeline([sample_match_stage])
    assert pipeline[0] is sample_match_stage


def test_getitem_negative_index() -> None:
    """Negative indexing works."""
    match1 = Match(query={"a": 1})
    match2 = Match(query={"b": 2})
    pipeline = Pipeline([match1, match2])
    assert pipeline[-1] is match2


def test_getitem_out_of_range() -> None:
    """Out of range index raises IndexError."""
    pipeline = Pipeline([Match(query={"a": 1})])
    with pytest.raises(IndexError):
        _ = pipeline[5]


# --- to_list Tests ---


def test_to_list_empty(empty_pipeline: Pipeline) -> None:
    """Empty pipeline returns empty list."""
    assert empty_pipeline.to_list() == []


def test_to_list_returns_dicts(basic_pipeline: Pipeline) -> None:
    """to_list returns list of dictionaries."""
    result = basic_pipeline.to_list()
    assert isinstance(result, list)
    assert len(result) == 5
    assert all(isinstance(s, dict) for s in result)


def test_to_list_is_new_list() -> None:
    """to_list returns a new list each time."""
    pipeline = Pipeline([Match(query={"a": 1})])
    list1 = pipeline.to_list()
    list2 = pipeline.to_list()
    assert list1 == list2
    assert list1 is not list2


# --- with_sort Tests ---


def test_with_sort_returns_tuple() -> None:
    """with_sort returns a tuple of (list, dict)."""
    pipeline = Pipeline([Match(query={"status": "active"})])
    result = pipeline.with_sort({"created_at": -1})
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert isinstance(result[0], list)
    assert isinstance(result[1], dict)


def test_with_sort_pipeline_list() -> None:
    """with_sort tuple contains correct pipeline list."""
    pipeline = Pipeline(
        [
            Match(query={"a": 1}),
            Unwind(path="items"),
        ]
    )
    result = pipeline.with_sort({"total": -1})
    assert result[0] == [
        {"$match": {"a": 1}},
        {"$unwind": "$items"},
    ]


def test_with_sort_sort_spec() -> None:
    """with_sort tuple contains correct sort spec."""
    pipeline = Pipeline([Match(query={"a": 1})])
    sort_spec = {"total": -1, "name": 1}
    result = pipeline.with_sort(sort_spec)
    assert result[1] == sort_spec


def test_with_sort_empty_pipeline() -> None:
    """with_sort works with empty pipeline."""
    pipeline = Pipeline()
    result = pipeline.with_sort({"_id": 1})
    assert result == ([], {"_id": 1})


# --- extend Tests ---


def test_extend_adds_stages() -> None:
    """extend adds multiple stages."""
    pipeline = Pipeline([Match(query={"a": 1})])
    pipeline.extend(
        [
            Unwind(path="items"),
            Match(query={"b": 2}),
        ]
    )
    assert len(pipeline) == 3


def test_extend_returns_pipeline() -> None:
    """extend returns self for chaining."""
    pipeline = Pipeline()
    result = pipeline.extend([Match(query={"a": 1})])
    assert result is pipeline


def test_extend_empty_list() -> None:
    """extend with empty list doesn't change pipeline."""
    pipeline = Pipeline([Match(query={"a": 1})])
    pipeline.extend([])
    assert len(pipeline) == 1


def test_extend_chaining() -> None:
    """extend can be chained."""
    pipeline = (
        Pipeline()
        .extend([Match(query={"a": 1})])
        .extend([Unwind(path="items")])
    )
    assert len(pipeline) == 2


# --- extend_raw Tests ---


def test_extend_raw_adds_dict_stages() -> None:
    """extend_raw adds raw dictionary stages."""
    pipeline = Pipeline([Match(query={"a": 1})])
    pipeline.extend_raw(
        [
            {"$addFields": {"computed": {"$sum": ["$x", "$y"]}}},
            {"$project": {"_id": 0, "result": "$computed"}},
        ]
    )
    assert len(pipeline) == 3
    stages = pipeline.to_list()
    assert stages[1] == {"$addFields": {"computed": {"$sum": ["$x", "$y"]}}}
    assert stages[2] == {"$project": {"_id": 0, "result": "$computed"}}


def test_extend_raw_returns_pipeline() -> None:
    """extend_raw returns self for chaining."""
    pipeline = Pipeline()
    result = pipeline.extend_raw([{"$match": {"a": 1}}])
    assert result is pipeline


def test_extend_raw_with_typed_stages() -> None:
    """extend_raw works alongside typed stages."""
    pipeline = Pipeline([Match(query={"status": "active"})])
    pipeline.add_stage(Unwind(path="items"))
    pipeline.extend_raw(
        [
            {
                "$lookup": {
                    "from": "other",
                    "localField": "id",
                    "foreignField": "_id",
                    "as": "joined",
                }
            }
        ]
    )
    pipeline.add_stage(Match(query={"joined": {"$ne": []}}))

    stages = pipeline.to_list()
    assert len(stages) == 4
    assert "$match" in stages[0]
    assert "$unwind" in stages[1]
    assert "$lookup" in stages[2]
    assert "$match" in stages[3]


def test_extend_raw_empty_list() -> None:
    """extend_raw with empty list doesn't change pipeline."""
    pipeline = Pipeline([Match(query={"a": 1})])
    pipeline.extend_raw([])
    assert len(pipeline) == 1


def test_extend_raw_complex_stage() -> None:
    """extend_raw handles complex nested stages."""
    pipeline = Pipeline()
    pipeline.extend_raw(
        [
            {
                "$lookup": {
                    "from": "targets",
                    "let": {"agency_id": "$agency_id"},
                    "pipeline": [
                        {
                            "$match": {
                                "$expr": {"$eq": ["$AgencyId", "$$agency_id"]}
                            }
                        },
                        {
                            "$group": {
                                "_id": None,
                                "total": {"$sum": "$amount"},
                            }
                        },
                    ],
                    "as": "target",
                }
            }
        ]
    )
    stages = pipeline.to_list()
    assert len(stages) == 1
    assert stages[0]["$lookup"]["let"] == {"agency_id": "$agency_id"}
    assert len(stages[0]["$lookup"]["pipeline"]) == 2

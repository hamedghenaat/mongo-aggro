"""Tests for Pipeline class."""

import pytest

from mongo_aggro import Match, Pipeline, Unwind

# --- Initialization Tests ---


def test_pipeline_init_empty() -> None:
    """Pipeline can be initialized without stages."""
    pipeline = Pipeline()
    assert len(pipeline) == 0


def test_pipeline_init_with_stages() -> None:
    """Pipeline can be initialized with a list of stages."""
    stages = [
        Match(query={"status": "active"}),
        Unwind(path="items"),
    ]
    pipeline = Pipeline(stages)
    assert len(pipeline) == 2


def test_pipeline_init_with_none() -> None:
    """Pipeline handles None as empty list."""
    pipeline = Pipeline(None)
    assert len(pipeline) == 0


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

"""Tests for change stream aggregation stages."""

import pytest
from pydantic import ValidationError

from mongo_aggro.stages import ChangeStream, ChangeStreamSplitLargeEvent

# --- ChangeStream Tests ---


def test_change_stream_empty() -> None:
    """ChangeStream with no options."""
    stream = ChangeStream()
    assert stream.model_dump() == {"$changeStream": {}}


def test_change_stream_full_document() -> None:
    """ChangeStream with fullDocument option."""
    stream = ChangeStream(full_document="updateLookup")
    assert stream.model_dump() == {
        "$changeStream": {"fullDocument": "updateLookup"}
    }


def test_change_stream_options() -> None:
    """ChangeStream with multiple options."""
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


def test_change_stream_resume_after() -> None:
    """ChangeStream with resumeAfter token."""
    stream = ChangeStream(resume_after={"_data": "some_token"})
    result = stream.model_dump()
    assert result["$changeStream"]["resumeAfter"] == {"_data": "some_token"}


def test_change_stream_start_after() -> None:
    """ChangeStream with startAfter token."""
    stream = ChangeStream(start_after={"_data": "some_token"})
    result = stream.model_dump()
    assert result["$changeStream"]["startAfter"] == {"_data": "some_token"}


def test_change_stream_all_changes_for_cluster() -> None:
    """ChangeStream with allChangesForCluster."""
    stream = ChangeStream(all_changes_for_cluster=True)
    result = stream.model_dump()
    assert result["$changeStream"]["allChangesForCluster"] is True


def test_change_stream_invalid_full_document() -> None:
    """ChangeStream with invalid fullDocument value."""
    with pytest.raises(ValidationError):
        ChangeStream(full_document="invalid")  # type: ignore[arg-type]


def test_change_stream_invalid_before_change() -> None:
    """ChangeStream with invalid fullDocumentBeforeChange value."""
    with pytest.raises(ValidationError):
        ChangeStream(
            full_document_before_change="invalid"  # type: ignore[arg-type]
        )


def test_change_stream_rejects_extra() -> None:
    """ChangeStream rejects unknown fields."""
    with pytest.raises(ValidationError):
        ChangeStream(extra="value")  # type: ignore[call-arg]


# --- ChangeStreamSplitLargeEvent Tests ---


def test_change_stream_split_large_event() -> None:
    """ChangeStreamSplitLargeEvent stage."""
    split = ChangeStreamSplitLargeEvent()
    assert split.model_dump() == {"$changeStreamSplitLargeEvent": {}}


def test_change_stream_split_large_event_rejects_extra() -> None:
    """ChangeStreamSplitLargeEvent rejects unknown fields."""
    with pytest.raises(ValidationError):
        ChangeStreamSplitLargeEvent(extra="value")  # type: ignore[call-arg]

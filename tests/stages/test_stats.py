"""Tests for statistics and diagnostics aggregation stages."""

import pytest
from pydantic import ValidationError

from mongo_aggro.stages import CollStats, CurrentOp, IndexStats, PlanCacheStats

# --- CollStats Tests ---


def test_coll_stats_latency() -> None:
    """CollStats with latency stats."""
    stats = CollStats(lat_stats={"histograms": True})
    assert stats.model_dump() == {
        "$collStats": {"latencyStats": {"histograms": True}}
    }


def test_coll_stats_storage() -> None:
    """CollStats with storage stats."""
    stats = CollStats(storage_stats={})
    assert stats.model_dump() == {"$collStats": {"storageStats": {}}}


def test_coll_stats_count() -> None:
    """CollStats with count."""
    stats = CollStats(count={})
    assert stats.model_dump() == {"$collStats": {"count": {}}}


def test_coll_stats_multiple() -> None:
    """CollStats with multiple options."""
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


def test_coll_stats_query_exec() -> None:
    """CollStats with queryExecStats."""
    stats = CollStats(query_exec_stats={})
    result = stats.model_dump()
    assert result == {"$collStats": {"queryExecStats": {}}}


def test_coll_stats_empty() -> None:
    """CollStats with no options."""
    stats = CollStats()
    assert stats.model_dump() == {"$collStats": {}}


def test_coll_stats_rejects_extra() -> None:
    """CollStats rejects unknown fields."""
    with pytest.raises(ValidationError):
        CollStats(unknown_field={})  # type: ignore[call-arg]


# --- IndexStats Tests ---


def test_index_stats() -> None:
    """IndexStats stage."""
    stats = IndexStats()
    assert stats.model_dump() == {"$indexStats": {}}


def test_index_stats_rejects_extra() -> None:
    """IndexStats rejects unknown fields."""
    with pytest.raises(ValidationError):
        IndexStats(extra="value")  # type: ignore[call-arg]


# --- PlanCacheStats Tests ---


def test_plan_cache_stats() -> None:
    """PlanCacheStats stage."""
    stats = PlanCacheStats()
    assert stats.model_dump() == {"$planCacheStats": {}}


def test_plan_cache_stats_rejects_extra() -> None:
    """PlanCacheStats rejects unknown fields."""
    with pytest.raises(ValidationError):
        PlanCacheStats(extra="value")  # type: ignore[call-arg]


# --- CurrentOp Tests ---


def test_current_op_empty() -> None:
    """CurrentOp with no options."""
    op = CurrentOp()
    assert op.model_dump() == {"$currentOp": {}}


def test_current_op_options() -> None:
    """CurrentOp with options."""
    op = CurrentOp(all_users=True, idle_connections=True)
    assert op.model_dump() == {
        "$currentOp": {"allUsers": True, "idleConnections": True}
    }


def test_current_op_all_options() -> None:
    """CurrentOp with all options."""
    op = CurrentOp(
        all_users=True,
        idle_connections=True,
        idle_cursors=True,
        idle_sessions=True,
        local_ops=False,
    )
    result = op.model_dump()
    assert result["$currentOp"]["allUsers"] is True
    assert result["$currentOp"]["idleConnections"] is True
    assert result["$currentOp"]["idleCursors"] is True
    assert result["$currentOp"]["idleSessions"] is True
    assert result["$currentOp"]["localOps"] is False


def test_current_op_rejects_extra() -> None:
    """CurrentOp rejects unknown fields."""
    with pytest.raises(ValidationError):
        CurrentOp(unknown=True)  # type: ignore[call-arg]

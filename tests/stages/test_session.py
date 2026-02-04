"""Tests for session-related aggregation stages."""

import pytest
from pydantic import ValidationError

from mongo_aggro.stages import (
    ListLocalSessions,
    ListSampledQueries,
    ListSessions,
)

# --- ListSessions Tests ---


def test_list_sessions_empty() -> None:
    """ListSessions with no filters."""
    sessions = ListSessions()
    assert sessions.model_dump() == {"$listSessions": {}}


def test_list_sessions_users() -> None:
    """ListSessions with users filter."""
    sessions = ListSessions(users=[{"user": "admin", "db": "admin"}])
    assert sessions.model_dump() == {
        "$listSessions": {"users": [{"user": "admin", "db": "admin"}]}
    }


def test_list_sessions_multiple_users() -> None:
    """ListSessions with multiple users."""
    sessions = ListSessions(
        users=[
            {"user": "admin", "db": "admin"},
            {"user": "app", "db": "myapp"},
        ]
    )
    result = sessions.model_dump()
    assert len(result["$listSessions"]["users"]) == 2


def test_list_sessions_all_users() -> None:
    """ListSessions with allUsers."""
    sessions = ListSessions(all_users=True)
    assert sessions.model_dump() == {"$listSessions": {"allUsers": True}}


def test_list_sessions_rejects_extra() -> None:
    """ListSessions rejects unknown fields."""
    with pytest.raises(ValidationError):
        ListSessions(unknown=True)  # type: ignore[call-arg]


# --- ListLocalSessions Tests ---


def test_list_local_sessions_empty() -> None:
    """ListLocalSessions with no options."""
    sessions = ListLocalSessions()
    assert sessions.model_dump() == {"$listLocalSessions": {}}


def test_list_local_sessions_all_users() -> None:
    """ListLocalSessions with allUsers."""
    sessions = ListLocalSessions(all_users=True)
    assert sessions.model_dump() == {"$listLocalSessions": {"allUsers": True}}


def test_list_local_sessions_users() -> None:
    """ListLocalSessions with users filter."""
    sessions = ListLocalSessions(users=[{"user": "test", "db": "test"}])
    result = sessions.model_dump()
    assert result["$listLocalSessions"]["users"] == [
        {"user": "test", "db": "test"}
    ]


def test_list_local_sessions_rejects_extra() -> None:
    """ListLocalSessions rejects unknown fields."""
    with pytest.raises(ValidationError):
        ListLocalSessions(extra="value")  # type: ignore[call-arg]


# --- ListSampledQueries Tests ---


def test_list_sampled_queries_empty() -> None:
    """ListSampledQueries with no namespace."""
    queries = ListSampledQueries()
    assert queries.model_dump() == {"$listSampledQueries": {}}


def test_list_sampled_queries() -> None:
    """ListSampledQueries stage."""
    queries = ListSampledQueries(namespace="test.users")
    assert queries.model_dump() == {
        "$listSampledQueries": {"namespace": "test.users"}
    }


def test_list_sampled_queries_rejects_extra() -> None:
    """ListSampledQueries rejects unknown fields."""
    with pytest.raises(ValidationError):
        ListSampledQueries(extra="value")  # type: ignore[call-arg]

"""Session-related MongoDB aggregation pipeline stages.

This module contains stages for listing sessions and sampled queries:
ListSessions, ListLocalSessions, and ListSampledQueries.
"""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ListSessions(BaseModel):
    """
    $listSessions stage - lists all sessions in system.sessions.

    Example:
        >>> ListSessions().model_dump()
        {"$listSessions": {}}

        >>> ListSessions(users=[{"user": "admin", "db": "admin"}]).model_dump()
        {"$listSessions": {"users": [{"user": "admin", "db": "admin"}]}}

        >>> ListSessions(all_users=True).model_dump()
        {"$listSessions": {"allUsers": True}}
    """

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    users: list[dict[str, str]] | None = Field(
        default=None,
        description="List of users to filter sessions",
    )
    all_users: bool | None = Field(
        default=None,
        serialization_alias="allUsers",
        description="Return sessions for all users",
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        result: dict[str, Any] = {}
        if self.users is not None:
            result["users"] = self.users
        if self.all_users is not None:
            result["allUsers"] = self.all_users
        return {"$listSessions": result}


class ListLocalSessions(BaseModel):
    """
    $listLocalSessions stage - lists local sessions (db.aggregate only).

    Example:
        >>> ListLocalSessions().model_dump()
        {"$listLocalSessions": {}}

        >>> ListLocalSessions(all_users=True).model_dump()
        {"$listLocalSessions": {"allUsers": True}}
    """

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    users: list[dict[str, str]] | None = Field(
        default=None,
        description="List of users to filter sessions",
    )
    all_users: bool | None = Field(
        default=None,
        serialization_alias="allUsers",
        description="Return sessions for all users",
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        result: dict[str, Any] = {}
        if self.users is not None:
            result["users"] = self.users
        if self.all_users is not None:
            result["allUsers"] = self.all_users
        return {"$listLocalSessions": result}


class ListSampledQueries(BaseModel):
    """
    $listSampledQueries stage - lists sampled queries.

    Example:
        >>> ListSampledQueries().model_dump()
        {"$listSampledQueries": {}}

        >>> ListSampledQueries(namespace="db.collection").model_dump()
        {"$listSampledQueries": {"namespace": "db.collection"}}
    """

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    namespace: str | None = Field(
        default=None,
        description="Namespace to filter sampled queries",
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        result: dict[str, Any] = {}
        if self.namespace is not None:
            result["namespace"] = self.namespace
        return {"$listSampledQueries": result}


__all__ = [
    "ListSessions",
    "ListLocalSessions",
    "ListSampledQueries",
]

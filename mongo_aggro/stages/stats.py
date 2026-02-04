"""Statistics and diagnostics MongoDB aggregation pipeline stages.

This module contains stages for collection/index statistics and operations:
CollStats, IndexStats, PlanCacheStats, and CurrentOp.
"""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from mongo_aggro.base import BaseStage


class CollStats(BaseModel, BaseStage):
    """
    $collStats stage - returns collection statistics.

    Example:
        >>> CollStats(lat_stats={"histograms": True}).model_dump()
        {"$collStats": {"latencyStats": {"histograms": True}}}

        >>> CollStats(storage_stats={}).model_dump()
        {"$collStats": {"storageStats": {}}}

        >>> CollStats(count={}).model_dump()
        {"$collStats": {"count": {}}}
    """

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    lat_stats: dict[str, Any] | None = Field(
        default=None,
        serialization_alias="latencyStats",
        description="Latency statistics options",
    )
    storage_stats: dict[str, Any] | None = Field(
        default=None,
        serialization_alias="storageStats",
        description="Storage statistics options",
    )
    count: dict[str, Any] | None = Field(
        default=None,
        description="Document count options",
    )
    query_exec_stats: dict[str, Any] | None = Field(
        default=None,
        serialization_alias="queryExecStats",
        description="Query execution statistics options",
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        result: dict[str, Any] = {}
        if self.lat_stats is not None:
            result["latencyStats"] = self.lat_stats
        if self.storage_stats is not None:
            result["storageStats"] = self.storage_stats
        if self.count is not None:
            result["count"] = self.count
        if self.query_exec_stats is not None:
            result["queryExecStats"] = self.query_exec_stats
        return {"$collStats": result}


class IndexStats(BaseModel, BaseStage):
    """
    $indexStats stage - returns index usage statistics.

    Example:
        >>> IndexStats().model_dump()
        {"$indexStats": {}}
    """

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return {"$indexStats": {}}


class PlanCacheStats(BaseModel, BaseStage):
    """
    $planCacheStats stage - returns plan cache information.

    Example:
        >>> PlanCacheStats().model_dump()
        {"$planCacheStats": {}}
    """

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return {"$planCacheStats": {}}


class CurrentOp(BaseModel, BaseStage):
    """
    $currentOp stage - returns current operations (db.aggregate only).

    Example:
        >>> CurrentOp().model_dump()
        {"$currentOp": {}}

        >>> CurrentOp(all_users=True, idle_connections=True).model_dump()
        {"$currentOp": {"allUsers": True, "idleConnections": True}}
    """

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    all_users: bool | None = Field(
        default=None,
        serialization_alias="allUsers",
        description="Return operations for all users",
    )
    idle_connections: bool | None = Field(
        default=None,
        serialization_alias="idleConnections",
        description="Include idle connections",
    )
    idle_cursors: bool | None = Field(
        default=None,
        serialization_alias="idleCursors",
        description="Include idle cursors",
    )
    idle_sessions: bool | None = Field(
        default=None,
        serialization_alias="idleSessions",
        description="Include idle sessions",
    )
    local_ops: bool | None = Field(
        default=None,
        serialization_alias="localOps",
        description="Return local operations only",
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        result: dict[str, Any] = {}
        if self.all_users is not None:
            result["allUsers"] = self.all_users
        if self.idle_connections is not None:
            result["idleConnections"] = self.idle_connections
        if self.idle_cursors is not None:
            result["idleCursors"] = self.idle_cursors
        if self.idle_sessions is not None:
            result["idleSessions"] = self.idle_sessions
        if self.local_ops is not None:
            result["localOps"] = self.local_ops
        return {"$currentOp": result}


__all__ = [
    "CollStats",
    "IndexStats",
    "PlanCacheStats",
    "CurrentOp",
]

"""Miscellaneous MongoDB aggregation pipeline stages.

This module contains less commonly used stages:
ListClusterCatalog and QuerySettings.
"""

from typing import Any

from pydantic import BaseModel, ConfigDict

from mongo_aggro.base import BaseStage


class ListClusterCatalog(BaseModel, BaseStage):
    """
    $listClusterCatalog stage - lists collections in a cluster.

    Example:
        >>> ListClusterCatalog().model_dump()
        {"$listClusterCatalog": {}}
    """

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return {"$listClusterCatalog": {}}


class QuerySettings(BaseModel, BaseStage):
    """
    $querySettings stage - returns query settings (MongoDB 8.0+).

    Example:
        >>> QuerySettings().model_dump()
        {"$querySettings": {}}
    """

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return {"$querySettings": {}}


__all__ = [
    "ListClusterCatalog",
    "QuerySettings",
]

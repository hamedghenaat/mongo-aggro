"""MongoDB aggregation pipeline stages.

This package provides typed stage classes for building MongoDB aggregation
pipelines. All stages are re-exported here for convenient access.
"""

from mongo_aggro.stages.array import Unwind
from mongo_aggro.stages.change import ChangeStream, ChangeStreamSplitLargeEvent
from mongo_aggro.stages.core import (
    Count,
    Group,
    Limit,
    Match,
    Project,
    Skip,
    Sort,
)
from mongo_aggro.stages.geo import GeoNear
from mongo_aggro.stages.group import Bucket, BucketAuto, Facet, SortByCount
from mongo_aggro.stages.join import GraphLookup, Lookup, UnionWith
from mongo_aggro.stages.misc import ListClusterCatalog, QuerySettings
from mongo_aggro.stages.output import Documents, Merge, Out, Sample
from mongo_aggro.stages.search import (
    ListSearchIndexes,
    RankFusion,
    Search,
    SearchMeta,
    VectorSearch,
)
from mongo_aggro.stages.session import (
    ListLocalSessions,
    ListSampledQueries,
    ListSessions,
)
from mongo_aggro.stages.stats import (
    CollStats,
    CurrentOp,
    IndexStats,
    PlanCacheStats,
)
from mongo_aggro.stages.transform import (
    AddFields,
    Redact,
    ReplaceRoot,
    ReplaceWith,
    Set,
    Unset,
)
from mongo_aggro.stages.window import Densify, Fill, SetWindowFields

__all__ = [
    # core
    "Match",
    "Project",
    "Group",
    "Sort",
    "Limit",
    "Skip",
    "Count",
    # array
    "Unwind",
    # join
    "Lookup",
    "UnionWith",
    "GraphLookup",
    # transform
    "AddFields",
    "Set",
    "Unset",
    "ReplaceRoot",
    "ReplaceWith",
    "Redact",
    # group
    "Facet",
    "Bucket",
    "BucketAuto",
    "SortByCount",
    # output
    "Out",
    "Merge",
    "Sample",
    "Documents",
    # window
    "SetWindowFields",
    "Densify",
    "Fill",
    # geo
    "GeoNear",
    # stats
    "CollStats",
    "IndexStats",
    "PlanCacheStats",
    "CurrentOp",
    # session
    "ListSessions",
    "ListLocalSessions",
    "ListSampledQueries",
    # change
    "ChangeStream",
    "ChangeStreamSplitLargeEvent",
    # search
    "Search",
    "SearchMeta",
    "VectorSearch",
    "ListSearchIndexes",
    "RankFusion",
    # misc
    "ListClusterCatalog",
    "QuerySettings",
]

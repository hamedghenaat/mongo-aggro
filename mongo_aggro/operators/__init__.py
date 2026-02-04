"""Query and expression operators for MongoDB aggregation."""

from mongo_aggro.operators.array import All, ElemMatch, Size
from mongo_aggro.operators.base import QueryOperator
from mongo_aggro.operators.bitwise import (
    BitsAllClear,
    BitsAllSet,
    BitsAnyClear,
    BitsAnySet,
)
from mongo_aggro.operators.comparison import Eq, Gt, Gte, In, Lt, Lte, Ne, Nin
from mongo_aggro.operators.element import Exists, Type
from mongo_aggro.operators.geo import (
    GeoIntersects,
    GeoWithin,
    Near,
    NearSphere,
)
from mongo_aggro.operators.logical import And, Expr, Nor, Not, Or
from mongo_aggro.operators.misc import JsonSchema, Mod, Text, Where
from mongo_aggro.operators.regex import Regex

__all__ = [
    # Base
    "QueryOperator",
    # Logical
    "And",
    "Or",
    "Not",
    "Nor",
    "Expr",
    # Comparison
    "Eq",
    "Ne",
    "Gt",
    "Gte",
    "Lt",
    "Lte",
    "In",
    "Nin",
    # Element
    "Exists",
    "Type",
    # Array
    "ElemMatch",
    "Size",
    "All",
    # Regex
    "Regex",
    # Bitwise
    "BitsAllClear",
    "BitsAllSet",
    "BitsAnyClear",
    "BitsAnySet",
    # Geospatial
    "GeoIntersects",
    "GeoWithin",
    "Near",
    "NearSphere",
    # Miscellaneous
    "Mod",
    "JsonSchema",
    "Where",
    "Text",
]

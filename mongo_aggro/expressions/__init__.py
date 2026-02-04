"""MongoDB expression operators for aggregation pipelines.

This package provides expression operators organized by category:
- arithmetic: Math operators ($add, $subtract, $multiply, etc.)
- array: Array manipulation ($size, $slice, $filter, $map, etc.)
- bitwise: Bitwise operations ($bitAnd, $bitOr, $bitXor, $bitNot)
- comparison: Comparisons ($eq, $ne, $gt, $gte, $lt, $lte, $cmp)
- conditional: Conditionals ($cond, $ifNull, $switch)
- date: Date operations ($dateAdd, $year, $month, etc.)
- encrypted: Encrypted string operations
- logical: Boolean logic ($and, $or, $not)
- object: Object manipulation ($mergeObjects, $getField, etc.)
- set: Set operations ($setUnion, $setIntersection, etc.)
- size: Data size ($bsonSize, $binarySize)
- string: String operations ($concat, $split, $toLower, etc.)
- trigonometry: Trig functions ($sin, $cos, $tan, etc.)
- type: Type conversion ($toString, $toInt, $type, etc.)
- variable: Variables ($let, $literal, $rand)
- window: Window functions ($rank, $shift, etc.)
"""

# Base classes
# Arithmetic operators
from mongo_aggro.expressions.arithmetic import (
    AbsExpr,
    AddExpr,
    CeilExpr,
    DivideExpr,
    ExpExpr,
    FloorExpr,
    LnExpr,
    Log10Expr,
    LogExpr,
    ModExpr,
    MultiplyExpr,
    PowExpr,
    RoundExpr,
    SqrtExpr,
    SubtractExpr,
    TruncExpr,
)

# Array operators
from mongo_aggro.expressions.array import (
    ArrayElemAtExpr,
    ArraySizeExpr,
    ConcatArraysExpr,
    FilterExpr,
    FirstNExpr,
    InArrayExpr,
    IndexOfArrayExpr,
    IsArrayExpr,
    LastNExpr,
    MapExpr,
    MaxNExpr,
    MinNExpr,
    RangeExpr,
    ReduceExpr,
    ReverseArrayExpr,
    SliceExpr,
    SortArrayExpr,
)
from mongo_aggro.expressions.base import (
    ExpressionBase,
    F,
    Field,
)

# Bitwise operators
from mongo_aggro.expressions.bitwise import (
    BitAndExpr,
    BitNotExpr,
    BitOrExpr,
    BitXorExpr,
)

# Comparison operators
from mongo_aggro.expressions.comparison import (
    CmpExpr,
    EqExpr,
    GteExpr,
    GtExpr,
    LteExpr,
    LtExpr,
    NeExpr,
)

# Conditional operators
from mongo_aggro.expressions.conditional import (
    CondExpr,
    IfNullExpr,
    SwitchBranch,
    SwitchExpr,
)

# Date operators
from mongo_aggro.expressions.date import (
    DateAddExpr,
    DateDiffExpr,
    DateFromPartsExpr,
    DateFromStringExpr,
    DateSubtractExpr,
    DateToPartsExpr,
    DateToStringExpr,
    DateTruncExpr,
    DayOfMonthExpr,
    DayOfWeekExpr,
    DayOfYearExpr,
    HourExpr,
    IsoDayOfWeekExpr,
    IsoWeekExpr,
    IsoWeekYearExpr,
    MillisecondExpr,
    MinuteExpr,
    MonthExpr,
    SecondExpr,
    ToDateExpr,
    WeekExpr,
    YearExpr,
)

# Encrypted string operators
from mongo_aggro.expressions.encrypted import (
    EncStrContainsExpr,
    EncStrEndsWithExpr,
    EncStrNormalizedEqExpr,
    EncStrStartsWithExpr,
)

# Logical operators
from mongo_aggro.expressions.logical import (
    AndExpr,
    NotExpr,
    OrExpr,
)

# Object operators
from mongo_aggro.expressions.object import (
    ArrayToObjectExpr,
    GetFieldExpr,
    MergeObjectsExpr,
    ObjectToArrayExpr,
    SetFieldExpr,
)

# Set operators
from mongo_aggro.expressions.set import (
    AllElementsTrueExpr,
    AnyElementTrueExpr,
    SetDifferenceExpr,
    SetEqualsExpr,
    SetIntersectionExpr,
    SetIsSubsetExpr,
    SetUnionExpr,
)

# Size operators
from mongo_aggro.expressions.size import (
    BinarySizeExpr,
    BsonSizeExpr,
)

# String operators
from mongo_aggro.expressions.string import (
    ConcatExpr,
    LTrimExpr,
    RegexFindAllExpr,
    RegexFindExpr,
    RegexMatchExpr,
    ReplaceAllExpr,
    ReplaceOneExpr,
    RTrimExpr,
    SplitExpr,
    StrCaseCmpExpr,
    StrLenCPExpr,
    SubstrCPExpr,
    ToLowerExpr,
    ToUpperExpr,
    TrimExpr,
)

# Trigonometry operators
from mongo_aggro.expressions.trigonometry import (
    AcosExpr,
    AcoshExpr,
    AsinExpr,
    AsinhExpr,
    Atan2Expr,
    AtanExpr,
    AtanhExpr,
    CosExpr,
    CoshExpr,
    DegreesToRadiansExpr,
    RadiansToDegreesExpr,
    SinExpr,
    SinhExpr,
    TanExpr,
    TanhExpr,
)

# Type operators
from mongo_aggro.expressions.type import (
    ConvertExpr,
    IsNumberExpr,
    ToBoolExpr,
    ToDecimalExpr,
    ToDoubleExpr,
    ToIntExpr,
    ToLongExpr,
    ToObjectIdExpr,
    ToStringExpr,
    TypeExpr,
)

# Variable operators
from mongo_aggro.expressions.variable import (
    LetExpr,
    LiteralExpr,
    RandExpr,
)

# Window operators
from mongo_aggro.expressions.window import (
    BottomExpr,
    BottomNWindowExpr,
    CovariancePopExpr,
    CovarianceSampExpr,
    DenseRankExpr,
    DerivativeExpr,
    DocumentNumberExpr,
    ExpMovingAvgExpr,
    IntegralExpr,
    LinearFillExpr,
    LocfExpr,
    RankExpr,
    ShiftExpr,
    TopExpr,
    TopNWindowExpr,
)

__all__ = [
    # Base
    "Field",
    "F",
    "ExpressionBase",
    # Comparison
    "EqExpr",
    "NeExpr",
    "GtExpr",
    "GteExpr",
    "LtExpr",
    "LteExpr",
    "CmpExpr",
    # Logical
    "AndExpr",
    "OrExpr",
    "NotExpr",
    # Arithmetic
    "AddExpr",
    "SubtractExpr",
    "MultiplyExpr",
    "DivideExpr",
    "AbsExpr",
    "ModExpr",
    "CeilExpr",
    "FloorExpr",
    "RoundExpr",
    "TruncExpr",
    "SqrtExpr",
    "PowExpr",
    "ExpExpr",
    "LnExpr",
    "Log10Expr",
    "LogExpr",
    # Conditional
    "CondExpr",
    "IfNullExpr",
    "SwitchBranch",
    "SwitchExpr",
    # String
    "ConcatExpr",
    "SplitExpr",
    "ToLowerExpr",
    "ToUpperExpr",
    "TrimExpr",
    "LTrimExpr",
    "RTrimExpr",
    "ReplaceOneExpr",
    "ReplaceAllExpr",
    "RegexMatchExpr",
    "RegexFindExpr",
    "RegexFindAllExpr",
    "SubstrCPExpr",
    "StrLenCPExpr",
    "StrCaseCmpExpr",
    # Array
    "ArraySizeExpr",
    "SliceExpr",
    "FilterExpr",
    "MapExpr",
    "ReduceExpr",
    "ArrayElemAtExpr",
    "ConcatArraysExpr",
    "InArrayExpr",
    "IndexOfArrayExpr",
    "IsArrayExpr",
    "ReverseArrayExpr",
    "SortArrayExpr",
    "RangeExpr",
    "FirstNExpr",
    "LastNExpr",
    "MaxNExpr",
    "MinNExpr",
    # Date
    "DateAddExpr",
    "DateSubtractExpr",
    "DateDiffExpr",
    "DateToStringExpr",
    "DateFromStringExpr",
    "ToDateExpr",
    "YearExpr",
    "MonthExpr",
    "DayOfMonthExpr",
    "DayOfWeekExpr",
    "DayOfYearExpr",
    "HourExpr",
    "MinuteExpr",
    "SecondExpr",
    "MillisecondExpr",
    "WeekExpr",
    "IsoWeekExpr",
    "IsoWeekYearExpr",
    "IsoDayOfWeekExpr",
    "DateFromPartsExpr",
    "DateToPartsExpr",
    "DateTruncExpr",
    # Type
    "ToStringExpr",
    "ToIntExpr",
    "ToDoubleExpr",
    "ToBoolExpr",
    "ToObjectIdExpr",
    "ToLongExpr",
    "ToDecimalExpr",
    "ConvertExpr",
    "TypeExpr",
    "IsNumberExpr",
    # Set
    "SetUnionExpr",
    "SetIntersectionExpr",
    "SetDifferenceExpr",
    "SetEqualsExpr",
    "SetIsSubsetExpr",
    "AnyElementTrueExpr",
    "AllElementsTrueExpr",
    # Object
    "MergeObjectsExpr",
    "ObjectToArrayExpr",
    "ArrayToObjectExpr",
    "GetFieldExpr",
    "SetFieldExpr",
    # Variable
    "LetExpr",
    "LiteralExpr",
    "RandExpr",
    # Trigonometry
    "SinExpr",
    "CosExpr",
    "TanExpr",
    "AsinExpr",
    "AcosExpr",
    "AtanExpr",
    "Atan2Expr",
    "SinhExpr",
    "CoshExpr",
    "TanhExpr",
    "AsinhExpr",
    "AcoshExpr",
    "AtanhExpr",
    "DegreesToRadiansExpr",
    "RadiansToDegreesExpr",
    # Bitwise
    "BitAndExpr",
    "BitOrExpr",
    "BitXorExpr",
    "BitNotExpr",
    # Size
    "BsonSizeExpr",
    "BinarySizeExpr",
    # Window
    "RankExpr",
    "DenseRankExpr",
    "DocumentNumberExpr",
    "ShiftExpr",
    "ExpMovingAvgExpr",
    "DerivativeExpr",
    "IntegralExpr",
    "CovariancePopExpr",
    "CovarianceSampExpr",
    "LinearFillExpr",
    "LocfExpr",
    "TopExpr",
    "BottomExpr",
    "TopNWindowExpr",
    "BottomNWindowExpr",
    # Encrypted
    "EncStrContainsExpr",
    "EncStrStartsWithExpr",
    "EncStrEndsWithExpr",
    "EncStrNormalizedEqExpr",
]

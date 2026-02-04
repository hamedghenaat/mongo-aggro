"""Window expression operators for MongoDB aggregation."""

from typing import Any

from pydantic import model_serializer

from mongo_aggro.base import serialize_value
from mongo_aggro.expressions.base import ExpressionBase


class RankExpr(ExpressionBase):
    """
    $rank window operator - returns document rank in partition.

    Example:
        >>> RankExpr().model_dump()
        {"$rank": {}}
    """

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $rank expression."""
        return {"$rank": {}}


class DenseRankExpr(ExpressionBase):
    """
    $denseRank window operator - returns dense rank (no gaps).

    Example:
        >>> DenseRankExpr().model_dump()
        {"$denseRank": {}}
    """

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $denseRank expression."""
        return {"$denseRank": {}}


class DocumentNumberExpr(ExpressionBase):
    """
    $documentNumber window operator - returns position in partition.

    Example:
        >>> DocumentNumberExpr().model_dump()
        {"$documentNumber": {}}
    """

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $documentNumber expression."""
        return {"$documentNumber": {}}


class ShiftExpr(ExpressionBase):
    """
    $shift window operator - accesses value from different position.

    Example:
        >>> ShiftExpr(output=F("value"), by=1, default=0).model_dump()
        {"$shift": {"output": "$value", "by": 1, "default": 0}}
    """

    output: Any
    by: int
    default: Any = None

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $shift expression."""
        result: dict[str, Any] = {
            "output": serialize_value(self.output),
            "by": self.by,
        }
        if self.default is not None:
            result["default"] = serialize_value(self.default)
        return {"$shift": result}


class ExpMovingAvgExpr(ExpressionBase):
    """
    $expMovingAvg window operator - exponential moving average.

    Example:
        >>> ExpMovingAvgExpr(input=F("price"), n=5).model_dump()
        {"$expMovingAvg": {"input": "$price", "N": 5}}
    """

    input: Any
    n: int | None = None
    alpha: float | None = None

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $expMovingAvg expression."""
        result: dict[str, Any] = {"input": serialize_value(self.input)}
        if self.n is not None:
            result["N"] = self.n
        elif self.alpha is not None:
            result["alpha"] = self.alpha
        return {"$expMovingAvg": result}


class DerivativeExpr(ExpressionBase):
    """
    $derivative window operator - calculates rate of change.

    Example:
        >>> DerivativeExpr(input=F("value"), unit="second").model_dump()
        {"$derivative": {"input": "$value", "unit": "second"}}
    """

    input: Any
    unit: str | None = None

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $derivative expression."""
        result: dict[str, Any] = {"input": serialize_value(self.input)}
        if self.unit is not None:
            result["unit"] = self.unit
        return {"$derivative": result}


class IntegralExpr(ExpressionBase):
    """
    $integral window operator - calculates area under curve.

    Example:
        >>> IntegralExpr(input=F("value"), unit="hour").model_dump()
        {"$integral": {"input": "$value", "unit": "hour"}}
    """

    input: Any
    unit: str | None = None

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $integral expression."""
        result: dict[str, Any] = {"input": serialize_value(self.input)}
        if self.unit is not None:
            result["unit"] = self.unit
        return {"$integral": result}


class CovariancePopExpr(ExpressionBase):
    """
    $covariancePop window operator - population covariance.

    Example:
        >>> CovariancePopExpr(array=[F("x"), F("y")]).model_dump()
        {"$covariancePop": ["$x", "$y"]}
    """

    array: list[Any]

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $covariancePop expression."""
        return {"$covariancePop": [serialize_value(a) for a in self.array]}


class CovarianceSampExpr(ExpressionBase):
    """
    $covarianceSamp window operator - sample covariance.

    Example:
        >>> CovarianceSampExpr(array=[F("x"), F("y")]).model_dump()
        {"$covarianceSamp": ["$x", "$y"]}
    """

    array: list[Any]

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $covarianceSamp expression."""
        return {"$covarianceSamp": [serialize_value(a) for a in self.array]}


class LinearFillExpr(ExpressionBase):
    """
    $linearFill window operator - fills nulls with linear interpolation.

    Example:
        >>> LinearFillExpr(input=F("value")).model_dump()
        {"$linearFill": "$value"}
    """

    input: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $linearFill expression."""
        return {"$linearFill": serialize_value(self.input)}


class LocfExpr(ExpressionBase):
    """
    $locf window operator - last observation carried forward.

    Example:
        >>> LocfExpr(input=F("value")).model_dump()
        {"$locf": "$value"}
    """

    input: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $locf expression."""
        return {"$locf": serialize_value(self.input)}


class TopExpr(ExpressionBase):
    """
    $top accumulator - returns top element based on sort.

    Example:
        >>> TopExpr(sort_by={"score": -1}, output=F("name")).model_dump()
        {"$top": {"sortBy": {"score": -1}, "output": "$name"}}
    """

    sort_by: dict[str, int]
    output: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $top expression."""
        return {
            "$top": {
                "sortBy": self.sort_by,
                "output": serialize_value(self.output),
            }
        }


class BottomExpr(ExpressionBase):
    """
    $bottom accumulator - returns bottom element based on sort.

    Example:
        >>> BottomExpr(sort_by={"score": -1}, output=F("name")).model_dump()
        {"$bottom": {"sortBy": {"score": -1}, "output": "$name"}}
    """

    sort_by: dict[str, int]
    output: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $bottom expression."""
        return {
            "$bottom": {
                "sortBy": self.sort_by,
                "output": serialize_value(self.output),
            }
        }


class TopNWindowExpr(ExpressionBase):
    """
    $topN accumulator - returns top N elements based on sort.

    Example:
        >>> TopNWindowExpr(n=3, sort_by={"score": -1}, output=F("name")).model_dump()
        {"$topN": {"n": 3, "sortBy": {"score": -1}, "output": "$name"}}
    """

    n: Any
    sort_by: dict[str, int]
    output: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $topN expression."""
        return {
            "$topN": {
                "n": serialize_value(self.n),
                "sortBy": self.sort_by,
                "output": serialize_value(self.output),
            }
        }


class BottomNWindowExpr(ExpressionBase):
    """
    $bottomN accumulator - returns bottom N elements based on sort.

    Example:
        >>> BottomNWindowExpr(n=3, sort_by={"score": -1}, output=F("name")).model_dump()
        {"$bottomN": {"n": 3, "sortBy": {"score": -1}, "output": "$name"}}
    """

    n: Any
    sort_by: dict[str, int]
    output: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $bottomN expression."""
        return {
            "$bottomN": {
                "n": serialize_value(self.n),
                "sortBy": self.sort_by,
                "output": serialize_value(self.output),
            }
        }


__all__ = [
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
]

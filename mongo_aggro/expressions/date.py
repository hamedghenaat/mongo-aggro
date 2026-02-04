"""Date expression operators for MongoDB aggregation."""

from typing import Any

from pydantic import model_serializer

from mongo_aggro.base import serialize_value
from mongo_aggro.expressions.base import ExpressionBase


class DateAddExpr(ExpressionBase):
    """
    $dateAdd expression operator - adds time to a date.

    Example:
        >>> DateAddExpr(
        ...     start_date=F("orderDate"),
        ...     unit="day",
        ...     amount=7
        ... ).model_dump()
        {"$dateAdd": {"startDate": "$orderDate", "unit": "day", "amount": 7}}
    """

    start_date: Any
    unit: str
    amount: Any
    timezone: str | None = None

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $dateAdd expression."""
        result: dict[str, Any] = {
            "$dateAdd": {
                "startDate": serialize_value(self.start_date),
                "unit": self.unit,
                "amount": serialize_value(self.amount),
            }
        }
        if self.timezone:
            result["$dateAdd"]["timezone"] = self.timezone
        return result


class DateSubtractExpr(ExpressionBase):
    """
    $dateSubtract expression operator - subtracts time from a date.

    Example:
        >>> DateSubtractExpr(
        ...     start_date=F("endDate"),
        ...     unit="month",
        ...     amount=1
        ... ).model_dump()
        {"$dateSubtract": {"startDate": "$endDate", "unit": "month", "amount": 1}}
    """

    start_date: Any
    unit: str
    amount: Any
    timezone: str | None = None

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $dateSubtract expression."""
        result: dict[str, Any] = {
            "$dateSubtract": {
                "startDate": serialize_value(self.start_date),
                "unit": self.unit,
                "amount": serialize_value(self.amount),
            }
        }
        if self.timezone:
            result["$dateSubtract"]["timezone"] = self.timezone
        return result


class DateDiffExpr(ExpressionBase):
    """
    $dateDiff expression operator - calculates difference between dates.

    Example:
        >>> DateDiffExpr(
        ...     start_date=F("start"),
        ...     end_date=F("end"),
        ...     unit="day"
        ... ).model_dump()
        {"$dateDiff": {"startDate": "$start", "endDate": "$end", "unit": "day"}}
    """

    start_date: Any
    end_date: Any
    unit: str
    timezone: str | None = None
    start_of_week: str | None = None

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $dateDiff expression."""
        result: dict[str, Any] = {
            "$dateDiff": {
                "startDate": serialize_value(self.start_date),
                "endDate": serialize_value(self.end_date),
                "unit": self.unit,
            }
        }
        if self.timezone:
            result["$dateDiff"]["timezone"] = self.timezone
        if self.start_of_week:
            result["$dateDiff"]["startOfWeek"] = self.start_of_week
        return result


class DateToStringExpr(ExpressionBase):
    """
    $dateToString expression operator - converts date to string.

    Example:
        >>> DateToStringExpr(
        ...     date=F("orderDate"),
        ...     format="%Y-%m-%d"
        ... ).model_dump()
        {"$dateToString": {"date": "$orderDate", "format": "%Y-%m-%d"}}
    """

    date: Any
    format: str | None = None
    timezone: str | None = None
    on_null: Any = None

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $dateToString expression."""
        result: dict[str, Any] = {
            "$dateToString": {
                "date": serialize_value(self.date),
            }
        }
        if self.format:
            result["$dateToString"]["format"] = self.format
        if self.timezone:
            result["$dateToString"]["timezone"] = self.timezone
        if self.on_null is not None:
            result["$dateToString"]["onNull"] = serialize_value(self.on_null)
        return result


class DateFromStringExpr(ExpressionBase):
    """
    $dateFromString expression operator - parses string to date.

    Example:
        >>> DateFromStringExpr(
        ...     date_string=F("dateStr"),
        ...     format="%Y-%m-%d"
        ... ).model_dump()
        {"$dateFromString": {"dateString": "$dateStr", "format": "%Y-%m-%d"}}
    """

    date_string: Any
    format: str | None = None
    timezone: str | None = None
    on_error: Any = None
    on_null: Any = None

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $dateFromString expression."""
        result: dict[str, Any] = {
            "$dateFromString": {
                "dateString": serialize_value(self.date_string),
            }
        }
        if self.format:
            result["$dateFromString"]["format"] = self.format
        if self.timezone:
            result["$dateFromString"]["timezone"] = self.timezone
        if self.on_error is not None:
            result["$dateFromString"]["onError"] = serialize_value(
                self.on_error
            )
        if self.on_null is not None:
            result["$dateFromString"]["onNull"] = serialize_value(self.on_null)
        return result


class ToDateExpr(ExpressionBase):
    """
    $toDate expression operator - converts value to date.

    Example:
        >>> ToDateExpr(input=F("dateString")).model_dump()
        {"$toDate": "$dateString"}
    """

    input: Any

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $toDate expression."""
        return {"$toDate": serialize_value(self.input)}


class YearExpr(ExpressionBase):
    """
    $year expression operator - extracts year from date.

    Example:
        >>> YearExpr(date=F("createdAt")).model_dump()
        {"$year": "$createdAt"}
    """

    date: Any
    timezone: str | None = None

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $year expression."""
        if self.timezone is None:
            return {"$year": serialize_value(self.date)}
        return {
            "$year": {
                "date": serialize_value(self.date),
                "timezone": self.timezone,
            }
        }


class MonthExpr(ExpressionBase):
    """
    $month expression operator - extracts month (1-12) from date.

    Example:
        >>> MonthExpr(date=F("createdAt")).model_dump()
        {"$month": "$createdAt"}
    """

    date: Any
    timezone: str | None = None

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $month expression."""
        if self.timezone is None:
            return {"$month": serialize_value(self.date)}
        return {
            "$month": {
                "date": serialize_value(self.date),
                "timezone": self.timezone,
            }
        }


class DayOfMonthExpr(ExpressionBase):
    """
    $dayOfMonth expression operator - extracts day of month (1-31).

    Example:
        >>> DayOfMonthExpr(date=F("createdAt")).model_dump()
        {"$dayOfMonth": "$createdAt"}
    """

    date: Any
    timezone: str | None = None

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $dayOfMonth expression."""
        if self.timezone is None:
            return {"$dayOfMonth": serialize_value(self.date)}
        return {
            "$dayOfMonth": {
                "date": serialize_value(self.date),
                "timezone": self.timezone,
            }
        }


class DayOfWeekExpr(ExpressionBase):
    """
    $dayOfWeek expression operator - extracts day of week (1=Sun, 7=Sat).

    Example:
        >>> DayOfWeekExpr(date=F("createdAt")).model_dump()
        {"$dayOfWeek": "$createdAt"}
    """

    date: Any
    timezone: str | None = None

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $dayOfWeek expression."""
        if self.timezone is None:
            return {"$dayOfWeek": serialize_value(self.date)}
        return {
            "$dayOfWeek": {
                "date": serialize_value(self.date),
                "timezone": self.timezone,
            }
        }


class DayOfYearExpr(ExpressionBase):
    """
    $dayOfYear expression operator - extracts day of year (1-366).

    Example:
        >>> DayOfYearExpr(date=F("createdAt")).model_dump()
        {"$dayOfYear": "$createdAt"}
    """

    date: Any
    timezone: str | None = None

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $dayOfYear expression."""
        if self.timezone is None:
            return {"$dayOfYear": serialize_value(self.date)}
        return {
            "$dayOfYear": {
                "date": serialize_value(self.date),
                "timezone": self.timezone,
            }
        }


class HourExpr(ExpressionBase):
    """
    $hour expression operator - extracts hour (0-23) from date.

    Example:
        >>> HourExpr(date=F("createdAt")).model_dump()
        {"$hour": "$createdAt"}
    """

    date: Any
    timezone: str | None = None

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $hour expression."""
        if self.timezone is None:
            return {"$hour": serialize_value(self.date)}
        return {
            "$hour": {
                "date": serialize_value(self.date),
                "timezone": self.timezone,
            }
        }


class MinuteExpr(ExpressionBase):
    """
    $minute expression operator - extracts minute (0-59) from date.

    Example:
        >>> MinuteExpr(date=F("createdAt")).model_dump()
        {"$minute": "$createdAt"}
    """

    date: Any
    timezone: str | None = None

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $minute expression."""
        if self.timezone is None:
            return {"$minute": serialize_value(self.date)}
        return {
            "$minute": {
                "date": serialize_value(self.date),
                "timezone": self.timezone,
            }
        }


class SecondExpr(ExpressionBase):
    """
    $second expression operator - extracts second (0-60) from date.

    Example:
        >>> SecondExpr(date=F("createdAt")).model_dump()
        {"$second": "$createdAt"}
    """

    date: Any
    timezone: str | None = None

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $second expression."""
        if self.timezone is None:
            return {"$second": serialize_value(self.date)}
        return {
            "$second": {
                "date": serialize_value(self.date),
                "timezone": self.timezone,
            }
        }


class MillisecondExpr(ExpressionBase):
    """
    $millisecond expression operator - extracts milliseconds (0-999).

    Example:
        >>> MillisecondExpr(date=F("createdAt")).model_dump()
        {"$millisecond": "$createdAt"}
    """

    date: Any
    timezone: str | None = None

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $millisecond expression."""
        if self.timezone is None:
            return {"$millisecond": serialize_value(self.date)}
        return {
            "$millisecond": {
                "date": serialize_value(self.date),
                "timezone": self.timezone,
            }
        }


class WeekExpr(ExpressionBase):
    """
    $week expression operator - extracts week number (0-53).

    Example:
        >>> WeekExpr(date=F("createdAt")).model_dump()
        {"$week": "$createdAt"}
    """

    date: Any
    timezone: str | None = None

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $week expression."""
        if self.timezone is None:
            return {"$week": serialize_value(self.date)}
        return {
            "$week": {
                "date": serialize_value(self.date),
                "timezone": self.timezone,
            }
        }


class IsoWeekExpr(ExpressionBase):
    """
    $isoWeek expression operator - extracts ISO week number (1-53).

    Example:
        >>> IsoWeekExpr(date=F("createdAt")).model_dump()
        {"$isoWeek": "$createdAt"}
    """

    date: Any
    timezone: str | None = None

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $isoWeek expression."""
        if self.timezone is None:
            return {"$isoWeek": serialize_value(self.date)}
        return {
            "$isoWeek": {
                "date": serialize_value(self.date),
                "timezone": self.timezone,
            }
        }


class IsoWeekYearExpr(ExpressionBase):
    """
    $isoWeekYear expression operator - extracts ISO week year.

    Example:
        >>> IsoWeekYearExpr(date=F("createdAt")).model_dump()
        {"$isoWeekYear": "$createdAt"}
    """

    date: Any
    timezone: str | None = None

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $isoWeekYear expression."""
        if self.timezone is None:
            return {"$isoWeekYear": serialize_value(self.date)}
        return {
            "$isoWeekYear": {
                "date": serialize_value(self.date),
                "timezone": self.timezone,
            }
        }


class IsoDayOfWeekExpr(ExpressionBase):
    """
    $isoDayOfWeek expression operator - extracts ISO day of week (1=Mon, 7=Sun).

    Example:
        >>> IsoDayOfWeekExpr(date=F("createdAt")).model_dump()
        {"$isoDayOfWeek": "$createdAt"}
    """

    date: Any
    timezone: str | None = None

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $isoDayOfWeek expression."""
        if self.timezone is None:
            return {"$isoDayOfWeek": serialize_value(self.date)}
        return {
            "$isoDayOfWeek": {
                "date": serialize_value(self.date),
                "timezone": self.timezone,
            }
        }


class DateFromPartsExpr(ExpressionBase):
    """
    $dateFromParts expression operator - constructs date from parts.

    Example:
        >>> DateFromPartsExpr(year=2024, month=1, day=15).model_dump()
        {"$dateFromParts": {"year": 2024, "month": 1, "day": 15}}
    """

    year: Any
    month: Any | None = None
    day: Any | None = None
    hour: Any | None = None
    minute: Any | None = None
    second: Any | None = None
    millisecond: Any | None = None
    timezone: str | None = None
    # ISO week date fields
    iso_week_year: Any | None = None
    iso_week: Any | None = None
    iso_day_of_week: Any | None = None

    def _add_date_parts(self, result: dict[str, Any]) -> None:
        """Add date part fields to result dict."""
        if self.iso_week_year is not None:
            result["isoWeekYear"] = serialize_value(self.iso_week_year)
            if self.iso_week is not None:
                result["isoWeek"] = serialize_value(self.iso_week)
            if self.iso_day_of_week is not None:
                result["isoDayOfWeek"] = serialize_value(self.iso_day_of_week)
        else:
            result["year"] = serialize_value(self.year)
            if self.month is not None:
                result["month"] = serialize_value(self.month)
            if self.day is not None:
                result["day"] = serialize_value(self.day)

    def _add_time_parts(self, result: dict[str, Any]) -> None:
        """Add time part fields to result dict."""
        if self.hour is not None:
            result["hour"] = serialize_value(self.hour)
        if self.minute is not None:
            result["minute"] = serialize_value(self.minute)
        if self.second is not None:
            result["second"] = serialize_value(self.second)
        if self.millisecond is not None:
            result["millisecond"] = serialize_value(self.millisecond)
        if self.timezone is not None:
            result["timezone"] = self.timezone

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $dateFromParts expression."""
        result: dict[str, Any] = {}
        self._add_date_parts(result)
        self._add_time_parts(result)
        return {"$dateFromParts": result}


class DateToPartsExpr(ExpressionBase):
    """
    $dateToParts expression operator - extracts all date parts.

    Example:
        >>> DateToPartsExpr(date=F("createdAt")).model_dump()
        {"$dateToParts": {"date": "$createdAt"}}
    """

    date: Any
    timezone: str | None = None
    iso8601: bool | None = None

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $dateToParts expression."""
        result: dict[str, Any] = {"date": serialize_value(self.date)}
        if self.timezone is not None:
            result["timezone"] = self.timezone
        if self.iso8601 is not None:
            result["iso8601"] = self.iso8601
        return {"$dateToParts": result}


class DateTruncExpr(ExpressionBase):
    """
    $dateTrunc expression operator - truncates date to specified unit.

    Example:
        >>> DateTruncExpr(date=F("timestamp"), unit="day").model_dump()
        {"$dateTrunc": {"date": "$timestamp", "unit": "day"}}
    """

    date: Any
    unit: str
    bin_size: int | None = None
    timezone: str | None = None
    start_of_week: str | None = None

    @model_serializer
    def serialize(self) -> dict[str, Any]:
        """Serialize to MongoDB $dateTrunc expression."""
        result: dict[str, Any] = {
            "date": serialize_value(self.date),
            "unit": self.unit,
        }
        if self.bin_size is not None:
            result["binSize"] = self.bin_size
        if self.timezone is not None:
            result["timezone"] = self.timezone
        if self.start_of_week is not None:
            result["startOfWeek"] = self.start_of_week
        return {"$dateTrunc": result}


__all__ = [
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
]

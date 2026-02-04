"""Tests for date expression operators.

This module tests:
- DateAddExpr, DateSubtractExpr, DateDiffExpr
- DateToStringExpr, DateFromStringExpr, ToDateExpr
- YearExpr, MonthExpr, DayOfMonthExpr, DayOfWeekExpr, DayOfYearExpr
- HourExpr, MinuteExpr, SecondExpr, MillisecondExpr
- WeekExpr, IsoWeekExpr, IsoWeekYearExpr, IsoDayOfWeekExpr
- DateFromPartsExpr, DateToPartsExpr, DateTruncExpr
"""

from datetime import datetime

import pytest
from pydantic import ValidationError

from mongo_aggro.expressions import (
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
    F,
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

# --- DateAddExpr Tests ---


def test_date_add_expr() -> None:
    """DateAddExpr serialization."""
    expr = DateAddExpr(start_date=F("orderDate"), unit="day", amount=7)
    result = expr.model_dump()
    assert result == {
        "$dateAdd": {
            "startDate": "$orderDate",
            "unit": "day",
            "amount": 7,
        }
    }


def test_date_add_expr_with_timezone() -> None:
    """DateAddExpr with timezone."""
    expr = DateAddExpr(
        start_date=F("date"),
        unit="hour",
        amount=2,
        timezone="America/New_York",
    )
    result = expr.model_dump()
    assert result["$dateAdd"]["timezone"] == "America/New_York"


def test_date_add_missing_unit_raises() -> None:
    """DateAddExpr requires unit."""
    with pytest.raises(ValidationError):
        DateAddExpr(start_date=F("date"), amount=7)  # type: ignore[call-arg]


# --- DateSubtractExpr Tests ---


def test_date_subtract_expr() -> None:
    """DateSubtractExpr serialization."""
    expr = DateSubtractExpr(start_date=F("endDate"), unit="month", amount=1)
    result = expr.model_dump()
    assert result == {
        "$dateSubtract": {
            "startDate": "$endDate",
            "unit": "month",
            "amount": 1,
        }
    }


# --- DateDiffExpr Tests ---


def test_date_diff_expr() -> None:
    """DateDiffExpr serialization."""
    expr = DateDiffExpr(start_date=F("start"), end_date=F("end"), unit="day")
    result = expr.model_dump()
    assert result == {
        "$dateDiff": {
            "startDate": "$start",
            "endDate": "$end",
            "unit": "day",
        }
    }


def test_date_diff_expr_with_options() -> None:
    """DateDiffExpr with timezone and startOfWeek."""
    expr = DateDiffExpr(
        start_date=F("start"),
        end_date=F("end"),
        unit="week",
        timezone="UTC",
        start_of_week="monday",
    )
    result = expr.model_dump()
    assert result["$dateDiff"]["timezone"] == "UTC"
    assert result["$dateDiff"]["startOfWeek"] == "monday"


def test_date_diff_missing_end_date_raises() -> None:
    """DateDiffExpr requires end_date."""
    with pytest.raises(ValidationError):
        DateDiffExpr(start_date=F("start"), unit="day")  # type: ignore[call-arg]


# --- DateToStringExpr Tests ---


def test_date_to_string_expr() -> None:
    """DateToStringExpr serialization."""
    expr = DateToStringExpr(date=F("orderDate"), format="%Y-%m-%d")
    result = expr.model_dump()
    assert result == {
        "$dateToString": {
            "date": "$orderDate",
            "format": "%Y-%m-%d",
        }
    }


def test_date_to_string_expr_with_options() -> None:
    """DateToStringExpr with all options."""
    expr = DateToStringExpr(
        date=F("date"),
        format="%Y-%m-%d %H:%M",
        timezone="Europe/London",
        on_null="N/A",
    )
    result = expr.model_dump()
    assert result["$dateToString"]["timezone"] == "Europe/London"
    assert result["$dateToString"]["onNull"] == "N/A"


# --- DateFromStringExpr Tests ---


def test_date_from_string_expr() -> None:
    """DateFromStringExpr serialization."""
    expr = DateFromStringExpr(date_string=F("dateStr"), format="%Y-%m-%d")
    result = expr.model_dump()
    assert result == {
        "$dateFromString": {
            "dateString": "$dateStr",
            "format": "%Y-%m-%d",
        }
    }


def test_date_from_string_expr_with_error_handling() -> None:
    """DateFromStringExpr with error handling."""
    default_date = datetime(2020, 1, 1)
    expr = DateFromStringExpr(
        date_string=F("dateStr"),
        on_error=default_date,
        on_null=default_date,
    )
    result = expr.model_dump()
    assert result["$dateFromString"]["onError"] == default_date
    assert result["$dateFromString"]["onNull"] == default_date


# --- ToDateExpr Tests ---


def test_to_date_expr() -> None:
    """ToDateExpr serialization."""
    expr = ToDateExpr(input=F("dateString"))
    assert expr.model_dump() == {"$toDate": "$dateString"}


def test_to_date_missing_input_raises() -> None:
    """ToDateExpr requires input."""
    with pytest.raises(ValidationError):
        ToDateExpr()  # type: ignore[call-arg]


# --- Date Part Expressions Tests ---


def test_year_expr() -> None:
    """YearExpr serialization."""
    expr = YearExpr(date=F("createdAt"))
    assert expr.model_dump() == {"$year": "$createdAt"}


def test_year_expr_with_timezone() -> None:
    """YearExpr with timezone."""
    expr = YearExpr(date=F("createdAt"), timezone="UTC")
    assert expr.model_dump() == {
        "$year": {"date": "$createdAt", "timezone": "UTC"}
    }


def test_month_expr() -> None:
    """MonthExpr serialization."""
    expr = MonthExpr(date=F("createdAt"))
    assert expr.model_dump() == {"$month": "$createdAt"}


def test_day_of_month_expr() -> None:
    """DayOfMonthExpr serialization."""
    expr = DayOfMonthExpr(date=F("createdAt"))
    assert expr.model_dump() == {"$dayOfMonth": "$createdAt"}


def test_day_of_week_expr() -> None:
    """DayOfWeekExpr serialization."""
    expr = DayOfWeekExpr(date=F("createdAt"))
    assert expr.model_dump() == {"$dayOfWeek": "$createdAt"}


def test_day_of_year_expr() -> None:
    """DayOfYearExpr serialization."""
    expr = DayOfYearExpr(date=F("createdAt"))
    assert expr.model_dump() == {"$dayOfYear": "$createdAt"}


# --- Time Part Expressions Tests ---


def test_hour_expr() -> None:
    """HourExpr serialization."""
    expr = HourExpr(date=F("createdAt"))
    assert expr.model_dump() == {"$hour": "$createdAt"}


def test_minute_expr() -> None:
    """MinuteExpr serialization."""
    expr = MinuteExpr(date=F("createdAt"))
    assert expr.model_dump() == {"$minute": "$createdAt"}


def test_second_expr() -> None:
    """SecondExpr serialization."""
    expr = SecondExpr(date=F("createdAt"))
    assert expr.model_dump() == {"$second": "$createdAt"}


def test_millisecond_expr() -> None:
    """MillisecondExpr serialization."""
    expr = MillisecondExpr(date=F("createdAt"))
    assert expr.model_dump() == {"$millisecond": "$createdAt"}


# --- Week Expressions Tests ---


def test_week_expr() -> None:
    """WeekExpr serialization."""
    expr = WeekExpr(date=F("createdAt"))
    assert expr.model_dump() == {"$week": "$createdAt"}


def test_iso_week_expr() -> None:
    """IsoWeekExpr serialization."""
    expr = IsoWeekExpr(date=F("createdAt"))
    assert expr.model_dump() == {"$isoWeek": "$createdAt"}


def test_iso_week_year_expr() -> None:
    """IsoWeekYearExpr serialization."""
    expr = IsoWeekYearExpr(date=F("createdAt"))
    assert expr.model_dump() == {"$isoWeekYear": "$createdAt"}


def test_iso_day_of_week_expr() -> None:
    """IsoDayOfWeekExpr serialization."""
    expr = IsoDayOfWeekExpr(date=F("createdAt"))
    assert expr.model_dump() == {"$isoDayOfWeek": "$createdAt"}


# --- DateFromPartsExpr Tests ---


def test_date_from_parts_expr() -> None:
    """DateFromPartsExpr serialization."""
    expr = DateFromPartsExpr(year=2024, month=1, day=15)
    result = expr.model_dump()
    assert result["$dateFromParts"]["year"] == 2024
    assert result["$dateFromParts"]["month"] == 1
    assert result["$dateFromParts"]["day"] == 15


def test_date_from_parts_expr_iso() -> None:
    """DateFromPartsExpr with ISO week date."""
    expr = DateFromPartsExpr(
        year=2024, iso_week_year=2024, iso_week=1, iso_day_of_week=1
    )
    result = expr.model_dump()
    assert result["$dateFromParts"]["isoWeekYear"] == 2024
    assert result["$dateFromParts"]["isoWeek"] == 1
    assert result["$dateFromParts"]["isoDayOfWeek"] == 1


def test_date_from_parts_missing_year_raises() -> None:
    """DateFromPartsExpr requires year."""
    with pytest.raises(ValidationError):
        DateFromPartsExpr(month=1, day=15)  # type: ignore[call-arg]


# --- DateToPartsExpr Tests ---


def test_date_to_parts_expr() -> None:
    """DateToPartsExpr serialization."""
    expr = DateToPartsExpr(date=F("createdAt"))
    assert expr.model_dump() == {"$dateToParts": {"date": "$createdAt"}}


def test_date_to_parts_expr_with_options() -> None:
    """DateToPartsExpr with timezone and iso8601."""
    expr = DateToPartsExpr(date=F("createdAt"), timezone="UTC", iso8601=True)
    result = expr.model_dump()
    assert result["$dateToParts"]["timezone"] == "UTC"
    assert result["$dateToParts"]["iso8601"] is True


# --- DateTruncExpr Tests ---


def test_date_trunc_expr() -> None:
    """DateTruncExpr serialization."""
    expr = DateTruncExpr(date=F("timestamp"), unit="day")
    assert expr.model_dump() == {
        "$dateTrunc": {"date": "$timestamp", "unit": "day"}
    }


def test_date_trunc_expr_with_options() -> None:
    """DateTruncExpr with all options."""
    expr = DateTruncExpr(
        date=F("timestamp"),
        unit="week",
        bin_size=2,
        timezone="UTC",
        start_of_week="monday",
    )
    result = expr.model_dump()
    assert result["$dateTrunc"]["binSize"] == 2
    assert result["$dateTrunc"]["timezone"] == "UTC"
    assert result["$dateTrunc"]["startOfWeek"] == "monday"


def test_date_trunc_missing_unit_raises() -> None:
    """DateTruncExpr requires unit."""
    with pytest.raises(ValidationError):
        DateTruncExpr(date=F("timestamp"))  # type: ignore[call-arg]

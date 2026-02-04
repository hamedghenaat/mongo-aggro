"""Tests for expression operators and operator overloading."""

from datetime import datetime

import pytest

from mongo_aggro import Expr, Match, Pipeline
from mongo_aggro.expressions import (
    AndExpr,
    CmpExpr,
    EqExpr,
    F,
    Field,
    GteExpr,
    GtExpr,
    LteExpr,
    LtExpr,
    NeExpr,
    NotExpr,
    OrExpr,
)

# --- Field Class Tests ---


def test_field_creates_dollar_prefix() -> None:
    """Field adds $ prefix to path."""
    field = F("status")
    assert str(field) == "$status"


def test_field_preserves_existing_prefix() -> None:
    """Field preserves existing $ prefix."""
    field = F("$status")
    assert str(field) == "$status"


def test_field_nested_path() -> None:
    """Field handles nested paths."""
    field = F("user.profile.name")
    assert str(field) == "$user.profile.name"


def test_field_repr() -> None:
    """Field has readable repr."""
    field = F("status")
    assert repr(field) == "Field('$status')"


def test_field_is_hashable() -> None:
    """Field can be used in sets/dicts."""
    field = F("status")
    field_set = {field}
    assert F("status") in field_set or len(field_set) == 1


# --- Simple Expression Serialization Tests ---


def test_eq_expr_serialization(simple_eq_expr: EqExpr) -> None:
    """EqExpr serializes correctly."""
    assert simple_eq_expr.model_dump() == {"$eq": ["$status", "active"]}


def test_ne_expr_serialization() -> None:
    """NeExpr serializes correctly."""
    expr = NeExpr(left=F("status"), right="deleted")
    assert expr.model_dump() == {"$ne": ["$status", "deleted"]}


def test_gt_expr_serialization(simple_gt_expr: GtExpr) -> None:
    """GtExpr serializes correctly."""
    assert simple_gt_expr.model_dump() == {"$gt": ["$age", 18]}


def test_gte_expr_serialization() -> None:
    """GteExpr serializes correctly."""
    expr = GteExpr(left=F("age"), right=18)
    assert expr.model_dump() == {"$gte": ["$age", 18]}


def test_lt_expr_serialization(simple_lt_expr: LtExpr) -> None:
    """LtExpr serializes correctly."""
    assert simple_lt_expr.model_dump() == {"$lt": ["$age", 65]}


def test_lte_expr_serialization() -> None:
    """LteExpr serializes correctly."""
    expr = LteExpr(left=F("age"), right=65)
    assert expr.model_dump() == {"$lte": ["$age", 65]}


def test_cmp_expr_serialization() -> None:
    """CmpExpr serializes correctly."""
    expr = CmpExpr(left=F("a"), right=F("b"))
    assert expr.model_dump() == {"$cmp": ["$a", "$b"]}


# --- Comparison Operator Overloading Tests ---


def test_eq_via_operator(status_field: Field) -> None:
    """== operator creates EqExpr."""
    expr = status_field == "active"
    assert isinstance(expr, EqExpr)
    assert expr.model_dump() == {"$eq": ["$status", "active"]}


def test_ne_via_operator(status_field: Field) -> None:
    """!= operator creates NeExpr."""
    expr = status_field != "deleted"
    assert isinstance(expr, NeExpr)
    assert expr.model_dump() == {"$ne": ["$status", "deleted"]}


def test_gt_via_operator(age_field: Field) -> None:
    """> operator creates GtExpr."""
    expr = age_field > 18
    assert isinstance(expr, GtExpr)
    assert expr.model_dump() == {"$gt": ["$age", 18]}


def test_ge_via_operator(age_field: Field) -> None:
    """>= operator creates GteExpr."""
    expr = age_field >= 18
    assert isinstance(expr, GteExpr)
    assert expr.model_dump() == {"$gte": ["$age", 18]}


def test_lt_via_operator(age_field: Field) -> None:
    """< operator creates LtExpr."""
    expr = age_field < 65
    assert isinstance(expr, LtExpr)
    assert expr.model_dump() == {"$lt": ["$age", 65]}


def test_le_via_operator(age_field: Field) -> None:
    """<= operator creates LteExpr."""
    expr = age_field <= 65
    assert isinstance(expr, LteExpr)
    assert expr.model_dump() == {"$lte": ["$age", 65]}


# --- Logical Expression Tests ---


def test_and_expr_serialization(nested_and_expr: AndExpr) -> None:
    """AndExpr serializes with nested expressions."""
    assert nested_and_expr.model_dump() == {
        "$and": [
            {"$eq": ["$status", "active"]},
            {"$gt": ["$age", 18]}
        ]
    }


def test_or_expr_serialization() -> None:
    """OrExpr serializes correctly."""
    expr = OrExpr(conditions=[
        EqExpr(left=F("a"), right=1),
        EqExpr(left=F("a"), right=2)
    ])
    assert expr.model_dump() == {
        "$or": [
            {"$eq": ["$a", 1]},
            {"$eq": ["$a", 2]}
        ]
    }


def test_not_expr_serialization() -> None:
    """NotExpr serializes correctly."""
    expr = NotExpr(condition=EqExpr(left=F("status"), right="deleted"))
    assert expr.model_dump() == {
        "$not": {"$eq": ["$status", "deleted"]}
    }


# --- Logical Operator Overloading Tests ---


def test_and_via_operator() -> None:
    """& operator creates AndExpr."""
    expr = (F("a") == 1) & (F("b") == 2)
    assert isinstance(expr, AndExpr)
    assert expr.model_dump() == {
        "$and": [
            {"$eq": ["$a", 1]},
            {"$eq": ["$b", 2]}
        ]
    }


def test_or_via_operator() -> None:
    """| operator creates OrExpr."""
    expr = (F("a") == 1) | (F("b") == 2)
    assert isinstance(expr, OrExpr)
    assert expr.model_dump() == {
        "$or": [
            {"$eq": ["$a", 1]},
            {"$eq": ["$b", 2]}
        ]
    }


def test_not_via_operator() -> None:
    """~ operator creates NotExpr."""
    expr = ~(F("status") == "deleted")
    assert isinstance(expr, NotExpr)
    assert expr.model_dump() == {
        "$not": {"$eq": ["$status", "deleted"]}
    }


# --- Flattening Tests ---


def test_and_flattening() -> None:
    """Chained & flattens into single AndExpr."""
    expr = (F("a") == 1) & (F("b") == 2) & (F("c") == 3)
    assert isinstance(expr, AndExpr)
    assert len(expr.conditions) == 3
    assert expr.model_dump() == {
        "$and": [
            {"$eq": ["$a", 1]},
            {"$eq": ["$b", 2]},
            {"$eq": ["$c", 3]}
        ]
    }


def test_or_flattening() -> None:
    """Chained | flattens into single OrExpr."""
    expr = (F("a") == 1) | (F("b") == 2) | (F("c") == 3)
    assert isinstance(expr, OrExpr)
    assert len(expr.conditions) == 3
    assert expr.model_dump() == {
        "$or": [
            {"$eq": ["$a", 1]},
            {"$eq": ["$b", 2]},
            {"$eq": ["$c", 3]}
        ]
    }


# --- Deeply Nested Expression Tests ---


def test_deeply_nested_serialization(deeply_nested_expr: OrExpr) -> None:
    """Deeply nested expressions serialize correctly."""
    assert deeply_nested_expr.model_dump() == {
        "$or": [
            {"$and": [
                {"$eq": ["$x", 1]},
                {"$lt": ["$y", 10]}
            ]},
            {"$gt": ["$z", 100]}
        ]
    }


def test_and_containing_or() -> None:
    """AND containing OR serializes correctly."""
    expr = (F("a") == 1) & ((F("b") == 2) | (F("c") == 3))
    assert expr.model_dump() == {
        "$and": [
            {"$eq": ["$a", 1]},
            {"$or": [
                {"$eq": ["$b", 2]},
                {"$eq": ["$c", 3]}
            ]}
        ]
    }


def test_or_containing_and() -> None:
    """OR containing AND serializes correctly."""
    expr = (F("a") == 1) | ((F("b") == 2) & (F("c") == 3))
    assert expr.model_dump() == {
        "$or": [
            {"$eq": ["$a", 1]},
            {"$and": [
                {"$eq": ["$b", 2]},
                {"$eq": ["$c", 3]}
            ]}
        ]
    }


def test_complex_combined_expr(complex_combined_expr: AndExpr) -> None:
    """Complex expression from fixture serializes correctly."""
    result = complex_combined_expr.model_dump()
    assert "$and" in result
    assert len(result["$and"]) == 4
    assert "$or" in result["$and"][3]


# --- Field-to-Field Comparison Tests ---


def test_field_to_field_comparison() -> None:
    """Comparing two fields works."""
    expr = F("price") > F("cost")
    assert expr.model_dump() == {"$gt": ["$price", "$cost"]}


def test_field_with_datetime() -> None:
    """Field comparison with datetime works."""
    dt = datetime(2024, 1, 1)
    expr = F("created_at") >= dt
    assert expr.model_dump() == {"$gte": ["$created_at", dt]}


# --- Expr Wrapper Tests ---


def test_expr_with_expression_object(nested_and_expr: AndExpr) -> None:
    """Expr wrapper accepts expression objects."""
    expr = Expr(expression=nested_and_expr)
    assert expr.model_dump() == {
        "$expr": {
            "$and": [
                {"$eq": ["$status", "active"]},
                {"$gt": ["$age", 18]}
            ]
        }
    }


def test_expr_with_operator_built_expression() -> None:
    """Expr wrapper accepts operator-built expressions."""
    expr = Expr(expression=(F("status") == "active") & (F("age") > 18))
    assert expr.model_dump() == {
        "$expr": {
            "$and": [
                {"$eq": ["$status", "active"]},
                {"$gt": ["$age", 18]}
            ]
        }
    }


def test_expr_with_raw_dict() -> None:
    """Expr wrapper still accepts raw dicts (backward compat)."""
    expr = Expr(expression={"$eq": ["$a", "$b"]})
    assert expr.model_dump() == {"$expr": {"$eq": ["$a", "$b"]}}


# --- Pipeline Integration Tests ---


def test_match_with_operator_expr() -> None:
    """Match stage with operator-built expression."""
    pipeline = Pipeline([
        Match(query=Expr(
            expression=(F("status") == "active") & (F("age") > 18)
        ).model_dump())
    ])
    result = pipeline.to_list()
    assert result == [{
        "$match": {
            "$expr": {
                "$and": [
                    {"$eq": ["$status", "active"]},
                    {"$gt": ["$age", 18]}
                ]
            }
        }
    }]


def test_pipeline_with_nested_expression() -> None:
    """Pipeline with complex nested expression."""
    pipeline = Pipeline([
        Match(query=Expr(expression=(
            (F("active") == True)  # noqa: E712
            & ((F("role") == "admin") | (F("level") >= 5))
        )).model_dump())
    ])
    result = pipeline.to_list()
    match_expr = result[0]["$match"]["$expr"]

    assert "$and" in match_expr
    assert len(match_expr["$and"]) == 2
    assert "$or" in match_expr["$and"][1]


# --- Mixed Expression Tests ---


def test_mixed_with_raw_dicts() -> None:
    """Expressions can be mixed with raw dicts."""
    expr = AndExpr(conditions=[
        EqExpr(left=F("a"), right=1),
        {"$regex": {"input": "$name", "regex": "^test"}}
    ])
    assert expr.model_dump() == {
        "$and": [
            {"$eq": ["$a", 1]},
            {"$regex": {"input": "$name", "regex": "^test"}}
        ]
    }


# --- Backward Compatibility Tests ---


def test_raw_dict_in_match_still_works() -> None:
    """Raw dicts in Match still work (no regression)."""
    match = Match(query={"status": "active"})
    assert match.model_dump() == {"$match": {"status": "active"}}


def test_existing_expr_with_raw_dict() -> None:
    """Existing Expr usage with raw dict still works."""
    expr = Expr(expression={"$and": [{"$gt": ["$a", 1]}, {"$lt": ["$b", 10]}]})
    assert expr.model_dump() == {
        "$expr": {"$and": [{"$gt": ["$a", 1]}, {"$lt": ["$b", 10]}]}
    }


# --- Parametrized Tests ---


@pytest.mark.parametrize("value", [
    10,
    "string",
    True,
    False,
    None,
    3.14,
    datetime(2024, 1, 1),
])
def test_eq_with_various_types(value) -> None:
    """EqExpr handles various Python types."""
    expr = F("field") == value
    result = expr.model_dump()
    assert result == {"$eq": ["$field", value]}


@pytest.mark.parametrize("op_method,expr_class,mongo_op", [
    ("__eq__", EqExpr, "$eq"),
    ("__ne__", NeExpr, "$ne"),
    ("__gt__", GtExpr, "$gt"),
    ("__ge__", GteExpr, "$gte"),
    ("__lt__", LtExpr, "$lt"),
    ("__le__", LteExpr, "$lte"),
])
def test_all_comparison_operators(op_method, expr_class, mongo_op) -> None:
    """All comparison operators create correct expression types."""
    field = F("value")
    expr = getattr(field, op_method)(10)

    assert isinstance(expr, expr_class)
    assert mongo_op in expr.model_dump()


# --- Arithmetic Expression Tests ---


def test_add_expr_two_operands() -> None:
    """AddExpr with two operands."""
    from mongo_aggro.expressions import AddExpr

    expr = AddExpr(operands=[F("price"), F("tax")])
    assert expr.model_dump() == {"$add": ["$price", "$tax"]}


def test_add_expr_multiple_operands() -> None:
    """AddExpr with multiple operands."""
    from mongo_aggro.expressions import AddExpr

    expr = AddExpr(operands=[F("a"), F("b"), 10])
    assert expr.model_dump() == {"$add": ["$a", "$b", 10]}


def test_subtract_expr() -> None:
    """SubtractExpr serialization."""
    from mongo_aggro.expressions import SubtractExpr

    expr = SubtractExpr(left=F("total"), right=F("discount"))
    assert expr.model_dump() == {"$subtract": ["$total", "$discount"]}


def test_multiply_expr() -> None:
    """MultiplyExpr serialization."""
    from mongo_aggro.expressions import MultiplyExpr

    expr = MultiplyExpr(operands=[F("price"), F("quantity")])
    assert expr.model_dump() == {"$multiply": ["$price", "$quantity"]}


def test_divide_expr() -> None:
    """DivideExpr serialization."""
    from mongo_aggro.expressions import DivideExpr

    expr = DivideExpr(dividend=F("total"), divisor=F("count"))
    assert expr.model_dump() == {"$divide": ["$total", "$count"]}


def test_abs_expr() -> None:
    """AbsExpr serialization."""
    from mongo_aggro.expressions import AbsExpr

    expr = AbsExpr(value=F("balance"))
    assert expr.model_dump() == {"$abs": "$balance"}


def test_mod_expr() -> None:
    """ModExpr serialization."""
    from mongo_aggro.expressions import ModExpr

    expr = ModExpr(dividend=F("num"), divisor=2)
    assert expr.model_dump() == {"$mod": ["$num", 2]}


# --- Conditional Expression Tests ---


def test_cond_expr() -> None:
    """CondExpr serialization."""
    from mongo_aggro.expressions import CondExpr

    expr = CondExpr(
        if_=GtExpr(left=F("qty"), right=100),
        then="bulk",
        else_="retail",
    )
    result = expr.model_dump()
    assert result == {
        "$cond": {
            "if": {"$gt": ["$qty", 100]},
            "then": "bulk",
            "else": "retail",
        }
    }


def test_ifnull_expr() -> None:
    """IfNullExpr serialization."""
    from mongo_aggro.expressions import IfNullExpr

    expr = IfNullExpr(input=F("name"), replacement="Unknown")
    assert expr.model_dump() == {"$ifNull": ["$name", "Unknown"]}


def test_switch_expr() -> None:
    """SwitchExpr serialization."""
    from mongo_aggro.expressions import SwitchBranch, SwitchExpr

    expr = SwitchExpr(
        branches=[
            SwitchBranch(case=EqExpr(left=F("status"), right="A"), then=1),
            SwitchBranch(case=EqExpr(left=F("status"), right="B"), then=2),
        ],
        default=0,
    )
    result = expr.model_dump()
    assert result["$switch"]["branches"][0] == {
        "case": {"$eq": ["$status", "A"]},
        "then": 1,
    }
    assert result["$switch"]["default"] == 0


def test_switch_expr_no_default() -> None:
    """SwitchExpr without default."""
    from mongo_aggro.expressions import SwitchBranch, SwitchExpr

    expr = SwitchExpr(
        branches=[
            SwitchBranch(case=EqExpr(left=F("x"), right=1), then="one"),
        ],
    )
    result = expr.model_dump()
    assert "default" not in result["$switch"]


# --- String Expression Tests ---


def test_concat_expr() -> None:
    """ConcatExpr serialization."""
    from mongo_aggro.expressions import ConcatExpr

    expr = ConcatExpr(strings=[F("first"), " ", F("last")])
    assert expr.model_dump() == {"$concat": ["$first", " ", "$last"]}


def test_split_expr() -> None:
    """SplitExpr serialization."""
    from mongo_aggro.expressions import SplitExpr

    expr = SplitExpr(input=F("fullName"), delimiter=" ")
    assert expr.model_dump() == {"$split": ["$fullName", " "]}


def test_tolower_expr() -> None:
    """ToLowerExpr serialization."""
    from mongo_aggro.expressions import ToLowerExpr

    expr = ToLowerExpr(input=F("name"))
    assert expr.model_dump() == {"$toLower": "$name"}


def test_toupper_expr() -> None:
    """ToUpperExpr serialization."""
    from mongo_aggro.expressions import ToUpperExpr

    expr = ToUpperExpr(input=F("name"))
    assert expr.model_dump() == {"$toUpper": "$name"}


# --- Array Expression Tests ---


def test_array_size_expr() -> None:
    """ArraySizeExpr serialization."""
    from mongo_aggro.expressions import ArraySizeExpr

    expr = ArraySizeExpr(array=F("items"))
    assert expr.model_dump() == {"$size": "$items"}


def test_slice_expr_n_only() -> None:
    """SliceExpr with n only."""
    from mongo_aggro.expressions import SliceExpr

    expr = SliceExpr(array=F("items"), n=5)
    assert expr.model_dump() == {"$slice": ["$items", 5]}


def test_slice_expr_with_position() -> None:
    """SliceExpr with position and n."""
    from mongo_aggro.expressions import SliceExpr

    expr = SliceExpr(array=F("items"), position=2, n=3)
    assert expr.model_dump() == {"$slice": ["$items", 2, 3]}


def test_filter_expr() -> None:
    """FilterExpr serialization."""
    from mongo_aggro.expressions import FilterExpr

    expr = FilterExpr(
        input=F("items"),
        as_="item",
        cond=GteExpr(left=Field("$$item.price"), right=100),
    )
    result = expr.model_dump()
    assert result["$filter"]["input"] == "$items"
    assert result["$filter"]["as"] == "item"
    assert result["$filter"]["cond"] == {"$gte": ["$$item.price", 100]}


def test_filter_expr_with_limit() -> None:
    """FilterExpr with limit."""
    from mongo_aggro.expressions import FilterExpr

    expr = FilterExpr(
        input=F("items"),
        cond=GtExpr(left=Field("$$this.qty"), right=0),
        limit=5,
    )
    result = expr.model_dump()
    assert result["$filter"]["limit"] == 5


def test_map_expr() -> None:
    """MapExpr serialization."""
    from mongo_aggro.expressions import MapExpr, MultiplyExpr

    expr = MapExpr(
        input=F("prices"),
        as_="price",
        in_=MultiplyExpr(operands=[Field("$$price"), 1.1]),
    )
    result = expr.model_dump()
    assert result["$map"]["input"] == "$prices"
    assert result["$map"]["as"] == "price"
    assert result["$map"]["in"] == {"$multiply": ["$$price", 1.1]}


def test_reduce_expr() -> None:
    """ReduceExpr serialization."""
    from mongo_aggro.expressions import AddExpr, ReduceExpr

    expr = ReduceExpr(
        input=F("items"),
        initial_value=0,
        in_=AddExpr(operands=[Field("$$value"), Field("$$this.qty")]),
    )
    result = expr.model_dump()
    assert result["$reduce"]["input"] == "$items"
    assert result["$reduce"]["initialValue"] == 0
    assert result["$reduce"]["in"] == {"$add": ["$$value", "$$this.qty"]}


# --- Nested Expression Tests ---


def test_nested_arithmetic_expressions() -> None:
    """Nested arithmetic expressions serialize correctly."""
    from mongo_aggro.expressions import DivideExpr, MultiplyExpr

    # (price * qty) / total
    expr = DivideExpr(
        dividend=MultiplyExpr(operands=[F("price"), F("qty")]),
        divisor=F("total"),
    )
    result = expr.model_dump()
    assert result == {
        "$divide": [
            {"$multiply": ["$price", "$qty"]},
            "$total",
        ]
    }


def test_cond_with_comparison() -> None:
    """CondExpr with nested comparison and arithmetic."""
    from mongo_aggro.expressions import CondExpr, MultiplyExpr

    expr = CondExpr(
        if_=(F("qty") > 100),
        then=MultiplyExpr(operands=[F("price"), 0.9]),
        else_=F("price"),
    )
    result = expr.model_dump()
    assert result["$cond"]["if"] == {"$gt": ["$qty", 100]}
    assert result["$cond"]["then"] == {"$multiply": ["$price", 0.9]}
    assert result["$cond"]["else"] == "$price"


# --- Date Expression Tests ---


def test_date_add_expr() -> None:
    """DateAddExpr serialization."""
    from mongo_aggro.expressions import DateAddExpr

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
    from mongo_aggro.expressions import DateAddExpr

    expr = DateAddExpr(
        start_date=F("date"),
        unit="hour",
        amount=2,
        timezone="America/New_York",
    )
    result = expr.model_dump()
    assert result["$dateAdd"]["timezone"] == "America/New_York"


def test_date_subtract_expr() -> None:
    """DateSubtractExpr serialization."""
    from mongo_aggro.expressions import DateSubtractExpr

    expr = DateSubtractExpr(start_date=F("endDate"), unit="month", amount=1)
    result = expr.model_dump()
    assert result == {
        "$dateSubtract": {
            "startDate": "$endDate",
            "unit": "month",
            "amount": 1,
        }
    }


def test_date_diff_expr() -> None:
    """DateDiffExpr serialization."""
    from mongo_aggro.expressions import DateDiffExpr

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
    from mongo_aggro.expressions import DateDiffExpr

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


def test_date_to_string_expr() -> None:
    """DateToStringExpr serialization."""
    from mongo_aggro.expressions import DateToStringExpr

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
    from mongo_aggro.expressions import DateToStringExpr

    expr = DateToStringExpr(
        date=F("date"),
        format="%Y-%m-%d %H:%M",
        timezone="Europe/London",
        on_null="N/A",
    )
    result = expr.model_dump()
    assert result["$dateToString"]["timezone"] == "Europe/London"
    assert result["$dateToString"]["onNull"] == "N/A"


def test_date_from_string_expr() -> None:
    """DateFromStringExpr serialization."""
    from mongo_aggro.expressions import DateFromStringExpr

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
    from datetime import datetime

    from mongo_aggro.expressions import DateFromStringExpr

    default_date = datetime(2020, 1, 1)
    expr = DateFromStringExpr(
        date_string=F("dateStr"),
        on_error=default_date,
        on_null=default_date,
    )
    result = expr.model_dump()
    assert result["$dateFromString"]["onError"] == default_date
    assert result["$dateFromString"]["onNull"] == default_date


# --- Type Conversion Expression Tests ---


def test_to_date_expr() -> None:
    """ToDateExpr serialization."""
    from mongo_aggro.expressions import ToDateExpr

    expr = ToDateExpr(input=F("dateString"))
    assert expr.model_dump() == {"$toDate": "$dateString"}


def test_to_string_expr() -> None:
    """ToStringExpr serialization."""
    from mongo_aggro.expressions import ToStringExpr

    expr = ToStringExpr(input=F("numericId"))
    assert expr.model_dump() == {"$toString": "$numericId"}


def test_to_int_expr() -> None:
    """ToIntExpr serialization."""
    from mongo_aggro.expressions import ToIntExpr

    expr = ToIntExpr(input=F("stringNum"))
    assert expr.model_dump() == {"$toInt": "$stringNum"}


def test_to_double_expr() -> None:
    """ToDoubleExpr serialization."""
    from mongo_aggro.expressions import ToDoubleExpr

    expr = ToDoubleExpr(input=F("intValue"))
    assert expr.model_dump() == {"$toDouble": "$intValue"}


def test_to_bool_expr() -> None:
    """ToBoolExpr serialization."""
    from mongo_aggro.expressions import ToBoolExpr

    expr = ToBoolExpr(input=F("flag"))
    assert expr.model_dump() == {"$toBool": "$flag"}


def test_to_object_id_expr() -> None:
    """ToObjectIdExpr serialization."""
    from mongo_aggro.expressions import ToObjectIdExpr

    expr = ToObjectIdExpr(input=F("idString"))
    assert expr.model_dump() == {"$toObjectId": "$idString"}


def test_convert_expr() -> None:
    """ConvertExpr serialization."""
    from mongo_aggro.expressions import ConvertExpr

    expr = ConvertExpr(input=F("value"), to="int")
    assert expr.model_dump() == {
        "$convert": {
            "input": "$value",
            "to": "int",
        }
    }


def test_convert_expr_with_error_handling() -> None:
    """ConvertExpr with error handling."""
    from mongo_aggro.expressions import ConvertExpr

    expr = ConvertExpr(
        input=F("value"),
        to="double",
        on_error=0.0,
        on_null=-1.0,
    )
    result = expr.model_dump()
    assert result["$convert"]["onError"] == 0.0
    assert result["$convert"]["onNull"] == -1.0


def test_type_expr() -> None:
    """TypeExpr serialization."""
    from mongo_aggro.expressions import TypeExpr

    expr = TypeExpr(input=F("field"))
    assert expr.model_dump() == {"$type": "$field"}


# --- Set Expression Tests ---


def test_set_union_expr() -> None:
    """SetUnionExpr serialization."""
    from mongo_aggro.expressions import SetUnionExpr

    expr = SetUnionExpr(arrays=[F("tags1"), F("tags2")])
    assert expr.model_dump() == {"$setUnion": ["$tags1", "$tags2"]}


def test_set_intersection_expr() -> None:
    """SetIntersectionExpr serialization."""
    from mongo_aggro.expressions import SetIntersectionExpr

    expr = SetIntersectionExpr(arrays=[F("a"), F("b")])
    assert expr.model_dump() == {"$setIntersection": ["$a", "$b"]}


def test_set_difference_expr() -> None:
    """SetDifferenceExpr serialization."""
    from mongo_aggro.expressions import SetDifferenceExpr

    expr = SetDifferenceExpr(first=F("all"), second=F("excluded"))
    assert expr.model_dump() == {"$setDifference": ["$all", "$excluded"]}


def test_set_equals_expr() -> None:
    """SetEqualsExpr serialization."""
    from mongo_aggro.expressions import SetEqualsExpr

    expr = SetEqualsExpr(arrays=[F("a"), F("b")])
    assert expr.model_dump() == {"$setEquals": ["$a", "$b"]}


def test_set_is_subset_expr() -> None:
    """SetIsSubsetExpr serialization."""
    from mongo_aggro.expressions import SetIsSubsetExpr

    expr = SetIsSubsetExpr(first=F("small"), second=F("large"))
    assert expr.model_dump() == {"$setIsSubset": ["$small", "$large"]}


def test_any_element_true_expr() -> None:
    """AnyElementTrueExpr serialization."""
    from mongo_aggro.expressions import AnyElementTrueExpr

    expr = AnyElementTrueExpr(input=F("flags"))
    assert expr.model_dump() == {"$anyElementTrue": "$flags"}


def test_all_elements_true_expr() -> None:
    """AllElementsTrueExpr serialization."""
    from mongo_aggro.expressions import AllElementsTrueExpr

    expr = AllElementsTrueExpr(input=F("conditions"))
    assert expr.model_dump() == {"$allElementsTrue": "$conditions"}


# --- Object Expression Tests ---


def test_merge_objects_expr() -> None:
    """MergeObjectsExpr serialization."""
    from mongo_aggro.expressions import MergeObjectsExpr

    expr = MergeObjectsExpr(objects=[F("defaults"), F("overrides")])
    assert expr.model_dump() == {"$mergeObjects": ["$defaults", "$overrides"]}


def test_object_to_array_expr() -> None:
    """ObjectToArrayExpr serialization."""
    from mongo_aggro.expressions import ObjectToArrayExpr

    expr = ObjectToArrayExpr(input=F("doc"))
    assert expr.model_dump() == {"$objectToArray": "$doc"}


def test_array_to_object_expr() -> None:
    """ArrayToObjectExpr serialization."""
    from mongo_aggro.expressions import ArrayToObjectExpr

    expr = ArrayToObjectExpr(input=F("pairs"))
    assert expr.model_dump() == {"$arrayToObject": "$pairs"}


def test_get_field_expr_simple() -> None:
    """GetFieldExpr simple serialization."""
    from mongo_aggro.expressions import GetFieldExpr

    expr = GetFieldExpr(field="status")
    assert expr.model_dump() == {"$getField": "status"}


def test_get_field_expr_with_input() -> None:
    """GetFieldExpr with input document."""
    from mongo_aggro.expressions import GetFieldExpr

    expr = GetFieldExpr(field="status", input=F("doc"))
    assert expr.model_dump() == {
        "$getField": {"field": "status", "input": "$doc"}
    }


def test_set_field_expr() -> None:
    """SetFieldExpr serialization."""
    from mongo_aggro.expressions import SetFieldExpr

    expr = SetFieldExpr(field="status", input=F("doc"), value="active")
    assert expr.model_dump() == {
        "$setField": {"field": "status", "input": "$doc", "value": "active"}
    }


# --- Variable Expression Tests ---


def test_let_expr() -> None:
    """LetExpr serialization."""
    from mongo_aggro.expressions import LetExpr, MultiplyExpr

    expr = LetExpr(
        vars={"total": MultiplyExpr(operands=[F("price"), F("qty")])},
        in_=Field("$$total"),
    )
    result = expr.model_dump()
    assert "$let" in result
    assert "vars" in result["$let"]
    assert "total" in result["$let"]["vars"]
    assert result["$let"]["in"] == "$$total"


# --- Miscellaneous Expression Tests ---


def test_literal_expr() -> None:
    """LiteralExpr serialization."""
    from mongo_aggro.expressions import LiteralExpr

    expr = LiteralExpr(value="$field")
    assert expr.model_dump() == {"$literal": "$field"}


def test_rand_expr() -> None:
    """RandExpr serialization."""
    from mongo_aggro.expressions import RandExpr

    expr = RandExpr()
    assert expr.model_dump() == {"$rand": {}}


# --- Additional Array Expression Tests ---


def test_array_elem_at_expr() -> None:
    """ArrayElemAtExpr serialization."""
    from mongo_aggro.expressions import ArrayElemAtExpr

    expr = ArrayElemAtExpr(array=F("items"), index=0)
    assert expr.model_dump() == {"$arrayElemAt": ["$items", 0]}


def test_concat_arrays_expr() -> None:
    """ConcatArraysExpr serialization."""
    from mongo_aggro.expressions import ConcatArraysExpr

    expr = ConcatArraysExpr(arrays=[F("arr1"), F("arr2")])
    assert expr.model_dump() == {"$concatArrays": ["$arr1", "$arr2"]}


def test_in_array_expr() -> None:
    """InArrayExpr serialization."""
    from mongo_aggro.expressions import InArrayExpr

    expr = InArrayExpr(value="admin", array=F("roles"))
    assert expr.model_dump() == {"$in": ["admin", "$roles"]}


def test_index_of_array_expr() -> None:
    """IndexOfArrayExpr serialization."""
    from mongo_aggro.expressions import IndexOfArrayExpr

    expr = IndexOfArrayExpr(array=F("items"), value="target")
    assert expr.model_dump() == {"$indexOfArray": ["$items", "target"]}


def test_index_of_array_expr_with_range() -> None:
    """IndexOfArrayExpr with start and end."""
    from mongo_aggro.expressions import IndexOfArrayExpr

    expr = IndexOfArrayExpr(array=F("items"), value="x", start=2, end=10)
    assert expr.model_dump() == {"$indexOfArray": ["$items", "x", 2, 10]}


def test_is_array_expr() -> None:
    """IsArrayExpr serialization."""
    from mongo_aggro.expressions import IsArrayExpr

    expr = IsArrayExpr(input=F("field"))
    assert expr.model_dump() == {"$isArray": "$field"}


def test_reverse_array_expr() -> None:
    """ReverseArrayExpr serialization."""
    from mongo_aggro.expressions import ReverseArrayExpr

    expr = ReverseArrayExpr(input=F("items"))
    assert expr.model_dump() == {"$reverseArray": "$items"}


def test_sort_array_expr() -> None:
    """SortArrayExpr serialization."""
    from mongo_aggro.expressions import SortArrayExpr

    expr = SortArrayExpr(input=F("scores"), sort_by={"score": -1})
    assert expr.model_dump() == {
        "$sortArray": {"input": "$scores", "sortBy": {"score": -1}}
    }


def test_range_expr() -> None:
    """RangeExpr serialization."""
    from mongo_aggro.expressions import RangeExpr

    expr = RangeExpr(start=0, end=10, step=2)
    assert expr.model_dump() == {"$range": [0, 10, 2]}


def test_first_n_expr() -> None:
    """FirstNExpr serialization."""
    from mongo_aggro.expressions import FirstNExpr

    expr = FirstNExpr(input=F("items"), n=3)
    assert expr.model_dump() == {"$firstN": {"input": "$items", "n": 3}}


def test_last_n_expr() -> None:
    """LastNExpr serialization."""
    from mongo_aggro.expressions import LastNExpr

    expr = LastNExpr(input=F("items"), n=3)
    assert expr.model_dump() == {"$lastN": {"input": "$items", "n": 3}}


def test_max_n_expr() -> None:
    """MaxNExpr serialization."""
    from mongo_aggro.expressions import MaxNExpr

    expr = MaxNExpr(input=F("scores"), n=3)
    assert expr.model_dump() == {"$maxN": {"input": "$scores", "n": 3}}


def test_min_n_expr() -> None:
    """MinNExpr serialization."""
    from mongo_aggro.expressions import MinNExpr

    expr = MinNExpr(input=F("scores"), n=3)
    assert expr.model_dump() == {"$minN": {"input": "$scores", "n": 3}}


# --- Additional String Expression Tests ---


def test_trim_expr() -> None:
    """TrimExpr serialization."""
    from mongo_aggro.expressions import TrimExpr

    expr = TrimExpr(input=F("text"))
    assert expr.model_dump() == {"$trim": {"input": "$text"}}


def test_trim_expr_with_chars() -> None:
    """TrimExpr with custom chars."""
    from mongo_aggro.expressions import TrimExpr

    expr = TrimExpr(input=F("text"), chars=" -")
    assert expr.model_dump() == {"$trim": {"input": "$text", "chars": " -"}}


def test_ltrim_expr() -> None:
    """LTrimExpr serialization."""
    from mongo_aggro.expressions import LTrimExpr

    expr = LTrimExpr(input=F("text"))
    assert expr.model_dump() == {"$ltrim": {"input": "$text"}}


def test_rtrim_expr() -> None:
    """RTrimExpr serialization."""
    from mongo_aggro.expressions import RTrimExpr

    expr = RTrimExpr(input=F("text"))
    assert expr.model_dump() == {"$rtrim": {"input": "$text"}}


def test_replace_one_expr() -> None:
    """ReplaceOneExpr serialization."""
    from mongo_aggro.expressions import ReplaceOneExpr

    expr = ReplaceOneExpr(input=F("text"), find="old", replacement="new")
    assert expr.model_dump() == {
        "$replaceOne": {"input": "$text", "find": "old", "replacement": "new"}
    }


def test_replace_all_expr() -> None:
    """ReplaceAllExpr serialization."""
    from mongo_aggro.expressions import ReplaceAllExpr

    expr = ReplaceAllExpr(input=F("text"), find="old", replacement="new")
    assert expr.model_dump() == {
        "$replaceAll": {"input": "$text", "find": "old", "replacement": "new"}
    }


def test_regex_match_expr() -> None:
    """RegexMatchExpr serialization."""
    from mongo_aggro.expressions import RegexMatchExpr

    expr = RegexMatchExpr(input=F("email"), regex=r"@.*\.com$")
    assert expr.model_dump() == {
        "$regexMatch": {"input": "$email", "regex": r"@.*\.com$"}
    }


def test_regex_match_expr_with_options() -> None:
    """RegexMatchExpr with options."""
    from mongo_aggro.expressions import RegexMatchExpr

    expr = RegexMatchExpr(input=F("text"), regex=r"pattern", options="i")
    result = expr.model_dump()
    assert result["$regexMatch"]["options"] == "i"


def test_regex_find_expr() -> None:
    """RegexFindExpr serialization."""
    from mongo_aggro.expressions import RegexFindExpr

    expr = RegexFindExpr(input=F("text"), regex=r"\d+")
    assert expr.model_dump() == {
        "$regexFind": {"input": "$text", "regex": r"\d+"}
    }


def test_regex_find_all_expr() -> None:
    """RegexFindAllExpr serialization."""
    from mongo_aggro.expressions import RegexFindAllExpr

    expr = RegexFindAllExpr(input=F("text"), regex=r"\w+")
    assert expr.model_dump() == {
        "$regexFindAll": {"input": "$text", "regex": r"\w+"}
    }


def test_substr_cp_expr() -> None:
    """SubstrCPExpr serialization."""
    from mongo_aggro.expressions import SubstrCPExpr

    expr = SubstrCPExpr(input=F("text"), start=0, length=5)
    assert expr.model_dump() == {"$substrCP": ["$text", 0, 5]}


def test_str_len_cp_expr() -> None:
    """StrLenCPExpr serialization."""
    from mongo_aggro.expressions import StrLenCPExpr

    expr = StrLenCPExpr(input=F("text"))
    assert expr.model_dump() == {"$strLenCP": "$text"}


def test_str_case_cmp_expr() -> None:
    """StrCaseCmpExpr serialization."""
    from mongo_aggro.expressions import StrCaseCmpExpr

    expr = StrCaseCmpExpr(first=F("a"), second=F("b"))
    assert expr.model_dump() == {"$strcasecmp": ["$a", "$b"]}


# --- Additional Arithmetic Expression Tests ---


def test_ceil_expr() -> None:
    """CeilExpr serialization."""
    from mongo_aggro.expressions import CeilExpr

    expr = CeilExpr(input=F("value"))
    assert expr.model_dump() == {"$ceil": "$value"}


def test_floor_expr() -> None:
    """FloorExpr serialization."""
    from mongo_aggro.expressions import FloorExpr

    expr = FloorExpr(input=F("value"))
    assert expr.model_dump() == {"$floor": "$value"}


def test_round_expr() -> None:
    """RoundExpr serialization."""
    from mongo_aggro.expressions import RoundExpr

    expr = RoundExpr(input=F("value"), place=2)
    assert expr.model_dump() == {"$round": ["$value", 2]}


def test_trunc_expr() -> None:
    """TruncExpr serialization."""
    from mongo_aggro.expressions import TruncExpr

    expr = TruncExpr(input=F("value"), place=1)
    assert expr.model_dump() == {"$trunc": ["$value", 1]}


def test_sqrt_expr() -> None:
    """SqrtExpr serialization."""
    from mongo_aggro.expressions import SqrtExpr

    expr = SqrtExpr(input=F("value"))
    assert expr.model_dump() == {"$sqrt": "$value"}


def test_pow_expr() -> None:
    """PowExpr serialization."""
    from mongo_aggro.expressions import PowExpr

    expr = PowExpr(base=F("value"), exponent=2)
    assert expr.model_dump() == {"$pow": ["$value", 2]}


def test_exp_expr() -> None:
    """ExpExpr serialization."""
    from mongo_aggro.expressions import ExpExpr

    expr = ExpExpr(input=F("value"))
    assert expr.model_dump() == {"$exp": "$value"}


def test_ln_expr() -> None:
    """LnExpr serialization."""
    from mongo_aggro.expressions import LnExpr

    expr = LnExpr(input=F("value"))
    assert expr.model_dump() == {"$ln": "$value"}


def test_log10_expr() -> None:
    """Log10Expr serialization."""
    from mongo_aggro.expressions import Log10Expr

    expr = Log10Expr(input=F("value"))
    assert expr.model_dump() == {"$log10": "$value"}


def test_log_expr() -> None:
    """LogExpr serialization."""
    from mongo_aggro.expressions import LogExpr

    expr = LogExpr(input=F("value"), base=2)
    assert expr.model_dump() == {"$log": ["$value", 2]}


# --- Additional Type Expression Tests ---


def test_to_long_expr() -> None:
    """ToLongExpr serialization."""
    from mongo_aggro.expressions import ToLongExpr

    expr = ToLongExpr(input=F("value"))
    assert expr.model_dump() == {"$toLong": "$value"}


def test_to_decimal_expr() -> None:
    """ToDecimalExpr serialization."""
    from mongo_aggro.expressions import ToDecimalExpr

    expr = ToDecimalExpr(input=F("value"))
    assert expr.model_dump() == {"$toDecimal": "$value"}


def test_is_number_expr() -> None:
    """IsNumberExpr serialization."""
    from mongo_aggro.expressions import IsNumberExpr

    expr = IsNumberExpr(input=F("value"))
    assert expr.model_dump() == {"$isNumber": "$value"}


# --- Trigonometry Expression Tests ---


def test_sin_expr() -> None:
    """SinExpr serialization."""
    from mongo_aggro.expressions import SinExpr

    expr = SinExpr(input=F("angle"))
    assert expr.model_dump() == {"$sin": "$angle"}


def test_cos_expr() -> None:
    """CosExpr serialization."""
    from mongo_aggro.expressions import CosExpr

    expr = CosExpr(input=F("angle"))
    assert expr.model_dump() == {"$cos": "$angle"}


def test_tan_expr() -> None:
    """TanExpr serialization."""
    from mongo_aggro.expressions import TanExpr

    expr = TanExpr(input=F("angle"))
    assert expr.model_dump() == {"$tan": "$angle"}


def test_asin_expr() -> None:
    """AsinExpr serialization."""
    from mongo_aggro.expressions import AsinExpr

    expr = AsinExpr(input=F("value"))
    assert expr.model_dump() == {"$asin": "$value"}


def test_acos_expr() -> None:
    """AcosExpr serialization."""
    from mongo_aggro.expressions import AcosExpr

    expr = AcosExpr(input=F("value"))
    assert expr.model_dump() == {"$acos": "$value"}


def test_atan_expr() -> None:
    """AtanExpr serialization."""
    from mongo_aggro.expressions import AtanExpr

    expr = AtanExpr(input=F("value"))
    assert expr.model_dump() == {"$atan": "$value"}


def test_atan2_expr() -> None:
    """Atan2Expr serialization."""
    from mongo_aggro.expressions import Atan2Expr

    expr = Atan2Expr(y=F("y"), x=F("x"))
    assert expr.model_dump() == {"$atan2": ["$y", "$x"]}


def test_sinh_expr() -> None:
    """SinhExpr serialization."""
    from mongo_aggro.expressions import SinhExpr

    expr = SinhExpr(input=F("value"))
    assert expr.model_dump() == {"$sinh": "$value"}


def test_cosh_expr() -> None:
    """CoshExpr serialization."""
    from mongo_aggro.expressions import CoshExpr

    expr = CoshExpr(input=F("value"))
    assert expr.model_dump() == {"$cosh": "$value"}


def test_tanh_expr() -> None:
    """TanhExpr serialization."""
    from mongo_aggro.expressions import TanhExpr

    expr = TanhExpr(input=F("value"))
    assert expr.model_dump() == {"$tanh": "$value"}


def test_asinh_expr() -> None:
    """AsinhExpr serialization."""
    from mongo_aggro.expressions import AsinhExpr

    expr = AsinhExpr(input=F("value"))
    assert expr.model_dump() == {"$asinh": "$value"}


def test_acosh_expr() -> None:
    """AcoshExpr serialization."""
    from mongo_aggro.expressions import AcoshExpr

    expr = AcoshExpr(input=F("value"))
    assert expr.model_dump() == {"$acosh": "$value"}


def test_atanh_expr() -> None:
    """AtanhExpr serialization."""
    from mongo_aggro.expressions import AtanhExpr

    expr = AtanhExpr(input=F("value"))
    assert expr.model_dump() == {"$atanh": "$value"}


def test_degrees_to_radians_expr() -> None:
    """DegreesToRadiansExpr serialization."""
    from mongo_aggro.expressions import DegreesToRadiansExpr

    expr = DegreesToRadiansExpr(input=F("degrees"))
    assert expr.model_dump() == {"$degreesToRadians": "$degrees"}


def test_radians_to_degrees_expr() -> None:
    """RadiansToDegreesExpr serialization."""
    from mongo_aggro.expressions import RadiansToDegreesExpr

    expr = RadiansToDegreesExpr(input=F("radians"))
    assert expr.model_dump() == {"$radiansToDegrees": "$radians"}


# --- Bitwise Expression Tests ---


def test_bit_and_expr() -> None:
    """BitAndExpr serialization."""
    from mongo_aggro.expressions import BitAndExpr

    expr = BitAndExpr(operands=[F("a"), F("b")])
    assert expr.model_dump() == {"$bitAnd": ["$a", "$b"]}


def test_bit_or_expr() -> None:
    """BitOrExpr serialization."""
    from mongo_aggro.expressions import BitOrExpr

    expr = BitOrExpr(operands=[F("a"), F("b")])
    assert expr.model_dump() == {"$bitOr": ["$a", "$b"]}


def test_bit_xor_expr() -> None:
    """BitXorExpr serialization."""
    from mongo_aggro.expressions import BitXorExpr

    expr = BitXorExpr(operands=[F("a"), F("b")])
    assert expr.model_dump() == {"$bitXor": ["$a", "$b"]}


def test_bit_not_expr() -> None:
    """BitNotExpr serialization."""
    from mongo_aggro.expressions import BitNotExpr

    expr = BitNotExpr(input=F("value"))
    assert expr.model_dump() == {"$bitNot": "$value"}


# --- Data Size Expression Tests ---


def test_bson_size_expr() -> None:
    """BsonSizeExpr serialization."""
    from mongo_aggro.expressions import BsonSizeExpr

    expr = BsonSizeExpr(input=F("doc"))
    assert expr.model_dump() == {"$bsonSize": "$doc"}


def test_binary_size_expr() -> None:
    """BinarySizeExpr serialization."""
    from mongo_aggro.expressions import BinarySizeExpr

    expr = BinarySizeExpr(input=F("data"))
    assert expr.model_dump() == {"$binarySize": "$data"}


# --- Date Part Expression Tests ---


def test_year_expr() -> None:
    """YearExpr serialization."""
    from mongo_aggro.expressions import YearExpr

    expr = YearExpr(date=F("createdAt"))
    assert expr.model_dump() == {"$year": "$createdAt"}


def test_year_expr_with_timezone() -> None:
    """YearExpr with timezone."""
    from mongo_aggro.expressions import YearExpr

    expr = YearExpr(date=F("createdAt"), timezone="UTC")
    assert expr.model_dump() == {
        "$year": {"date": "$createdAt", "timezone": "UTC"}
    }


def test_month_expr() -> None:
    """MonthExpr serialization."""
    from mongo_aggro.expressions import MonthExpr

    expr = MonthExpr(date=F("createdAt"))
    assert expr.model_dump() == {"$month": "$createdAt"}


def test_day_of_month_expr() -> None:
    """DayOfMonthExpr serialization."""
    from mongo_aggro.expressions import DayOfMonthExpr

    expr = DayOfMonthExpr(date=F("createdAt"))
    assert expr.model_dump() == {"$dayOfMonth": "$createdAt"}


def test_day_of_week_expr() -> None:
    """DayOfWeekExpr serialization."""
    from mongo_aggro.expressions import DayOfWeekExpr

    expr = DayOfWeekExpr(date=F("createdAt"))
    assert expr.model_dump() == {"$dayOfWeek": "$createdAt"}


def test_day_of_year_expr() -> None:
    """DayOfYearExpr serialization."""
    from mongo_aggro.expressions import DayOfYearExpr

    expr = DayOfYearExpr(date=F("createdAt"))
    assert expr.model_dump() == {"$dayOfYear": "$createdAt"}


def test_hour_expr() -> None:
    """HourExpr serialization."""
    from mongo_aggro.expressions import HourExpr

    expr = HourExpr(date=F("createdAt"))
    assert expr.model_dump() == {"$hour": "$createdAt"}


def test_minute_expr() -> None:
    """MinuteExpr serialization."""
    from mongo_aggro.expressions import MinuteExpr

    expr = MinuteExpr(date=F("createdAt"))
    assert expr.model_dump() == {"$minute": "$createdAt"}


def test_second_expr() -> None:
    """SecondExpr serialization."""
    from mongo_aggro.expressions import SecondExpr

    expr = SecondExpr(date=F("createdAt"))
    assert expr.model_dump() == {"$second": "$createdAt"}


def test_millisecond_expr() -> None:
    """MillisecondExpr serialization."""
    from mongo_aggro.expressions import MillisecondExpr

    expr = MillisecondExpr(date=F("createdAt"))
    assert expr.model_dump() == {"$millisecond": "$createdAt"}


def test_week_expr() -> None:
    """WeekExpr serialization."""
    from mongo_aggro.expressions import WeekExpr

    expr = WeekExpr(date=F("createdAt"))
    assert expr.model_dump() == {"$week": "$createdAt"}


def test_iso_week_expr() -> None:
    """IsoWeekExpr serialization."""
    from mongo_aggro.expressions import IsoWeekExpr

    expr = IsoWeekExpr(date=F("createdAt"))
    assert expr.model_dump() == {"$isoWeek": "$createdAt"}


def test_iso_week_year_expr() -> None:
    """IsoWeekYearExpr serialization."""
    from mongo_aggro.expressions import IsoWeekYearExpr

    expr = IsoWeekYearExpr(date=F("createdAt"))
    assert expr.model_dump() == {"$isoWeekYear": "$createdAt"}


def test_iso_day_of_week_expr() -> None:
    """IsoDayOfWeekExpr serialization."""
    from mongo_aggro.expressions import IsoDayOfWeekExpr

    expr = IsoDayOfWeekExpr(date=F("createdAt"))
    assert expr.model_dump() == {"$isoDayOfWeek": "$createdAt"}


def test_date_from_parts_expr() -> None:
    """DateFromPartsExpr serialization."""
    from mongo_aggro.expressions import DateFromPartsExpr

    expr = DateFromPartsExpr(year=2024, month=1, day=15)
    result = expr.model_dump()
    assert result["$dateFromParts"]["year"] == 2024
    assert result["$dateFromParts"]["month"] == 1
    assert result["$dateFromParts"]["day"] == 15


def test_date_from_parts_expr_iso() -> None:
    """DateFromPartsExpr with ISO week date."""
    from mongo_aggro.expressions import DateFromPartsExpr

    expr = DateFromPartsExpr(
        year=2024, iso_week_year=2024, iso_week=1, iso_day_of_week=1
    )
    result = expr.model_dump()
    assert result["$dateFromParts"]["isoWeekYear"] == 2024
    assert result["$dateFromParts"]["isoWeek"] == 1
    assert result["$dateFromParts"]["isoDayOfWeek"] == 1


def test_date_to_parts_expr() -> None:
    """DateToPartsExpr serialization."""
    from mongo_aggro.expressions import DateToPartsExpr

    expr = DateToPartsExpr(date=F("createdAt"))
    assert expr.model_dump() == {"$dateToParts": {"date": "$createdAt"}}


def test_date_to_parts_expr_with_options() -> None:
    """DateToPartsExpr with timezone and iso8601."""
    from mongo_aggro.expressions import DateToPartsExpr

    expr = DateToPartsExpr(date=F("createdAt"), timezone="UTC", iso8601=True)
    result = expr.model_dump()
    assert result["$dateToParts"]["timezone"] == "UTC"
    assert result["$dateToParts"]["iso8601"] is True


def test_date_trunc_expr() -> None:
    """DateTruncExpr serialization."""
    from mongo_aggro.expressions import DateTruncExpr

    expr = DateTruncExpr(date=F("timestamp"), unit="day")
    assert expr.model_dump() == {
        "$dateTrunc": {"date": "$timestamp", "unit": "day"}
    }


def test_date_trunc_expr_with_options() -> None:
    """DateTruncExpr with all options."""
    from mongo_aggro.expressions import DateTruncExpr

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


# --- Window Expression Tests ---


def test_rank_expr() -> None:
    """RankExpr serialization."""
    from mongo_aggro.expressions import RankExpr

    expr = RankExpr()
    assert expr.model_dump() == {"$rank": {}}


def test_dense_rank_expr() -> None:
    """DenseRankExpr serialization."""
    from mongo_aggro.expressions import DenseRankExpr

    expr = DenseRankExpr()
    assert expr.model_dump() == {"$denseRank": {}}


def test_document_number_expr() -> None:
    """DocumentNumberExpr serialization."""
    from mongo_aggro.expressions import DocumentNumberExpr

    expr = DocumentNumberExpr()
    assert expr.model_dump() == {"$documentNumber": {}}


def test_shift_expr() -> None:
    """ShiftExpr serialization."""
    from mongo_aggro.expressions import ShiftExpr

    expr = ShiftExpr(output=F("value"), by=1)
    result = expr.model_dump()
    assert result == {"$shift": {"output": "$value", "by": 1}}


def test_shift_expr_with_default() -> None:
    """ShiftExpr with default value."""
    from mongo_aggro.expressions import ShiftExpr

    expr = ShiftExpr(output=F("value"), by=-1, default=0)
    result = expr.model_dump()
    assert result["$shift"]["default"] == 0


def test_exp_moving_avg_expr_n() -> None:
    """ExpMovingAvgExpr with N parameter."""
    from mongo_aggro.expressions import ExpMovingAvgExpr

    expr = ExpMovingAvgExpr(input=F("price"), n=5)
    result = expr.model_dump()
    assert result == {"$expMovingAvg": {"input": "$price", "N": 5}}


def test_exp_moving_avg_expr_alpha() -> None:
    """ExpMovingAvgExpr with alpha parameter."""
    from mongo_aggro.expressions import ExpMovingAvgExpr

    expr = ExpMovingAvgExpr(input=F("price"), alpha=0.5)
    result = expr.model_dump()
    assert result == {"$expMovingAvg": {"input": "$price", "alpha": 0.5}}


def test_derivative_expr() -> None:
    """DerivativeExpr serialization."""
    from mongo_aggro.expressions import DerivativeExpr

    expr = DerivativeExpr(input=F("value"), unit="second")
    result = expr.model_dump()
    assert result == {"$derivative": {"input": "$value", "unit": "second"}}


def test_integral_expr() -> None:
    """IntegralExpr serialization."""
    from mongo_aggro.expressions import IntegralExpr

    expr = IntegralExpr(input=F("value"), unit="hour")
    result = expr.model_dump()
    assert result == {"$integral": {"input": "$value", "unit": "hour"}}


def test_covariance_pop_expr() -> None:
    """CovariancePopExpr serialization."""
    from mongo_aggro.expressions import CovariancePopExpr

    expr = CovariancePopExpr(array=[F("x"), F("y")])
    assert expr.model_dump() == {"$covariancePop": ["$x", "$y"]}


def test_covariance_samp_expr() -> None:
    """CovarianceSampExpr serialization."""
    from mongo_aggro.expressions import CovarianceSampExpr

    expr = CovarianceSampExpr(array=[F("x"), F("y")])
    assert expr.model_dump() == {"$covarianceSamp": ["$x", "$y"]}


def test_linear_fill_expr() -> None:
    """LinearFillExpr serialization."""
    from mongo_aggro.expressions import LinearFillExpr

    expr = LinearFillExpr(input=F("value"))
    assert expr.model_dump() == {"$linearFill": "$value"}


def test_locf_expr() -> None:
    """LocfExpr serialization."""
    from mongo_aggro.expressions import LocfExpr

    expr = LocfExpr(input=F("value"))
    assert expr.model_dump() == {"$locf": "$value"}


def test_top_expr() -> None:
    """TopExpr serialization."""
    from mongo_aggro.expressions import TopExpr

    expr = TopExpr(sort_by={"score": -1}, output=F("name"))
    assert expr.model_dump() == {
        "$top": {"sortBy": {"score": -1}, "output": "$name"}
    }


def test_bottom_expr() -> None:
    """BottomExpr serialization."""
    from mongo_aggro.expressions import BottomExpr

    expr = BottomExpr(sort_by={"score": 1}, output=F("name"))
    assert expr.model_dump() == {
        "$bottom": {"sortBy": {"score": 1}, "output": "$name"}
    }


def test_top_n_window_expr() -> None:
    """TopNWindowExpr serialization."""
    from mongo_aggro.expressions import TopNWindowExpr

    expr = TopNWindowExpr(n=3, sort_by={"score": -1}, output=F("name"))
    assert expr.model_dump() == {
        "$topN": {"n": 3, "sortBy": {"score": -1}, "output": "$name"}
    }


def test_bottom_n_window_expr() -> None:
    """BottomNWindowExpr serialization."""
    from mongo_aggro.expressions import BottomNWindowExpr

    expr = BottomNWindowExpr(n=3, sort_by={"score": 1}, output=F("name"))
    assert expr.model_dump() == {
        "$bottomN": {"n": 3, "sortBy": {"score": 1}, "output": "$name"}
    }

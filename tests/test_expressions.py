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

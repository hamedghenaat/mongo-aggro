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

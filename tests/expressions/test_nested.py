"""Tests for complex nested expressions with Expr class."""

from mongo_aggro import Expr, Match, Pipeline, Project
from mongo_aggro.expressions import (
    AddExpr,
    AndExpr,
    CondExpr,
    EqExpr,
    F,
    FilterExpr,
    GtExpr,
    MapExpr,
    MultiplyExpr,
)

# --- Expr with Match Stage Tests ---


def test_expr_simple_comparison_in_match() -> None:
    """Expr with simple comparison in Match stage."""
    expr = Expr(expression=(F("status") == "active"))
    match = Match(query=expr.model_dump())
    assert match.model_dump() == {
        "$match": {"$expr": {"$eq": ["$status", "active"]}}
    }


def test_expr_and_conditions_in_match() -> None:
    """Expr with AND conditions in Match."""
    expr = Expr(expression=((F("status") == "active") & (F("age") >= 18)))
    result = expr.model_dump()
    assert result["$expr"]["$and"][0] == {"$eq": ["$status", "active"]}
    assert result["$expr"]["$and"][1] == {"$gte": ["$age", 18]}


def test_expr_or_conditions_in_match() -> None:
    """Expr with OR conditions in Match."""
    expr = Expr(expression=((F("type") == "premium") | (F("balance") > 1000)))
    result = expr.model_dump()
    assert "$or" in result["$expr"]


def test_expr_complex_nested_and_or() -> None:
    """Expr with complex nested AND/OR."""
    expr = Expr(
        expression=(
            (F("active") == True)  # noqa: E712
            & ((F("role") == "admin") | (F("role") == "superuser"))
            & (F("verified") == True)  # noqa: E712
        )
    )
    result = expr.model_dump()
    # Should flatten to single $and with nested $or
    assert "$and" in result["$expr"]


def test_expr_with_not_operator() -> None:
    """Expr with NOT operator."""
    expr = Expr(expression=~(F("deleted") == True))  # noqa: E712
    result = expr.model_dump()
    assert "$not" in result["$expr"]


# --- Nested Arithmetic in Expressions ---


def test_nested_arithmetic_in_cond() -> None:
    """CondExpr with nested arithmetic."""
    expr = CondExpr(
        if_=GtExpr(left=F("quantity"), right=10),
        then=MultiplyExpr(operands=[F("price"), 0.9]),  # 10% discount
        else_=F("price"),
    )
    result = expr.model_dump()
    assert "$cond" in result
    assert result["$cond"]["then"] == {"$multiply": ["$price", 0.9]}


def test_deeply_nested_arithmetic() -> None:
    """3+ levels of nested arithmetic expressions."""
    # (price * quantity) + (shipping * 1.1)
    expr = AddExpr(
        operands=[
            MultiplyExpr(operands=[F("price"), F("quantity")]),
            MultiplyExpr(operands=[F("shipping"), 1.1]),
        ]
    )
    result = expr.model_dump()
    assert result == {
        "$add": [
            {"$multiply": ["$price", "$quantity"]},
            {"$multiply": ["$shipping", 1.1]},
        ]
    }


# --- Nested Array Expressions ---


def test_filter_with_nested_comparison() -> None:
    """FilterExpr with nested comparison in condition."""
    expr = FilterExpr(
        input=F("items"),
        cond=(F("$$this.price") > 100) & (F("$$this.inStock") == True),  # noqa: E712
    )
    result = expr.model_dump()
    assert "$filter" in result
    assert "$and" in result["$filter"]["cond"]


def test_map_with_nested_arithmetic() -> None:
    """MapExpr with nested arithmetic transformation."""
    expr = MapExpr(
        input=F("prices"), in_=MultiplyExpr(operands=[F("$$this"), 1.2])
    )
    result = expr.model_dump()
    assert result["$map"]["in"] == {"$multiply": ["$$this", 1.2]}


# --- Full Pipeline Integration Tests ---


def test_pipeline_with_nested_expr_in_match() -> None:
    """Pipeline with complex Expr in Match stage."""
    pipeline = Pipeline(
        [
            Match(
                query=Expr(
                    expression=(
                        (F("status") == "active")
                        & (F("age") >= 18)
                        & ((F("role") == "user") | (F("role") == "admin"))
                    )
                ).model_dump()
            )
        ]
    )
    stages = list(pipeline)
    assert len(stages) == 1
    assert "$match" in stages[0]
    assert "$expr" in stages[0]["$match"]


def test_pipeline_with_nested_project() -> None:
    """Pipeline with nested expressions in Project."""
    pipeline = Pipeline(
        [
            Project(
                fields={
                    "name": 1,
                    "total": AddExpr(
                        operands=[F("price"), F("tax")]
                    ).model_dump(),
                    "discounted": CondExpr(
                        if_=GtExpr(left=F("quantity"), right=10),
                        then=MultiplyExpr(operands=[F("price"), 0.9]),
                        else_=F("price"),
                    ).model_dump(),
                }
            )
        ]
    )
    stages = list(pipeline)
    assert "$project" in stages[0]
    assert "$add" in stages[0]["$project"]["total"]
    assert "$cond" in stages[0]["$project"]["discounted"]


# --- Edge Cases ---


def test_empty_and_conditions_allowed() -> None:
    """AndExpr with empty conditions serializes (MongoDB handles)."""
    expr = AndExpr(conditions=[])
    assert expr.model_dump() == {"$and": []}


def test_single_condition_and() -> None:
    """AndExpr with single condition still works."""
    expr = AndExpr(conditions=[EqExpr(left=F("a"), right=1)])
    result = expr.model_dump()
    assert result == {"$and": [{"$eq": ["$a", 1]}]}


def test_chained_operators_flatten() -> None:
    """Multiple chained & operators flatten to single $and."""
    expr = (F("a") == 1) & (F("b") == 2) & (F("c") == 3) & (F("d") == 4)
    result = expr.model_dump()
    assert "$and" in result
    assert len(result["$and"]) == 4  # All flattened


def test_mixed_operators_preserve_structure() -> None:
    """Mixed & and | preserve correct nesting."""
    expr = ((F("a") == 1) | (F("b") == 2)) & ((F("c") == 3) | (F("d") == 4))
    result = expr.model_dump()
    assert "$and" in result
    assert len(result["$and"]) == 2
    assert "$or" in result["$and"][0]
    assert "$or" in result["$and"][1]

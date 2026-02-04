"""Expression-related test fixtures."""

import pytest

from mongo_aggro.expressions import (
    AndExpr,
    EqExpr,
    F,
    Field,
    GtExpr,
    LtExpr,
    OrExpr,
)


@pytest.fixture
def status_field() -> Field:
    """Return a status field reference."""
    return F("status")


@pytest.fixture
def age_field() -> Field:
    """Return an age field reference."""
    return F("age")


@pytest.fixture
def simple_eq_expr(status_field: Field) -> EqExpr:
    """Return a simple equality expression."""
    return EqExpr(left=status_field, right="active")


@pytest.fixture
def simple_gt_expr(age_field: Field) -> GtExpr:
    """Return a simple greater-than expression."""
    return GtExpr(left=age_field, right=18)


@pytest.fixture
def simple_lt_expr(age_field: Field) -> LtExpr:
    """Return a simple less-than expression."""
    return LtExpr(left=age_field, right=65)


@pytest.fixture
def nested_and_expr() -> AndExpr:
    """Return an AND expression with two conditions."""
    return AndExpr(conditions=[
        EqExpr(left=F("status"), right="active"),
        GtExpr(left=F("age"), right=18)
    ])


@pytest.fixture
def deeply_nested_expr() -> OrExpr:
    """Return a deeply nested expression (3 levels)."""
    return OrExpr(conditions=[
        AndExpr(conditions=[
            EqExpr(left=F("x"), right=1),
            LtExpr(left=F("y"), right=10)
        ]),
        GtExpr(left=F("z"), right=100)
    ])


@pytest.fixture
def complex_combined_expr() -> AndExpr:
    """Return complex expression built via operators."""
    return (
        (F("status") == "active")
        & (F("is_active") == True)  # noqa: E712
        & (F("age") > 18)
        & (
            (F("score") < 50)
            | (F("bonus") >= 10)
        )
    )

"""Tests for query operator classes."""

from mongo_aggro import (
    All,
    And,
    ElemMatch,
    Eq,
    Exists,
    Expr,
    Gt,
    Gte,
    In,
    Lt,
    Lte,
    Ne,
    Nin,
    Nor,
    Not,
    Or,
    Regex,
    Size,
    Type,
)

# --- Logical Operators Tests ---


def test_and() -> None:
    """$and operator."""
    op = And(
        conditions=[
            {"status": "active"},
            {"age": {"$gt": 18}},
        ]
    )
    assert op.model_dump() == {
        "$and": [
            {"status": "active"},
            {"age": {"$gt": 18}},
        ]
    }


def test_and_empty() -> None:
    """$and with empty conditions."""
    op = And(conditions=[])
    assert op.model_dump() == {"$and": []}


def test_or() -> None:
    """$or operator."""
    op = Or(
        conditions=[
            {"status": "active"},
            {"status": "pending"},
        ]
    )
    assert op.model_dump() == {
        "$or": [
            {"status": "active"},
            {"status": "pending"},
        ]
    }


def test_not() -> None:
    """$not operator."""
    op = Not(condition={"$regex": "^test"})
    assert op.model_dump() == {"$not": {"$regex": "^test"}}


def test_nor() -> None:
    """$nor operator."""
    op = Nor(
        conditions=[
            {"price": {"$gt": 1000}},
            {"rating": {"$lt": 3}},
        ]
    )
    assert op.model_dump() == {
        "$nor": [
            {"price": {"$gt": 1000}},
            {"rating": {"$lt": 3}},
        ]
    }


# --- Expr Tests ---


def test_expr() -> None:
    """$expr operator."""
    op = Expr(expression={"$eq": ["$field1", "$field2"]})
    assert op.model_dump() == {"$expr": {"$eq": ["$field1", "$field2"]}}


def test_expr_complex() -> None:
    """$expr with complex expression."""
    op = Expr(
        expression={
            "$and": [
                {"$eq": ["$status", "active"]},
                {"$gt": ["$balance", 100]},
            ]
        }
    )
    result = op.model_dump()
    assert "$expr" in result
    assert "$and" in result["$expr"]


# --- Comparison Operators Tests ---


def test_eq() -> None:
    """$eq operator."""
    op = Eq(value=5)
    assert op.model_dump() == {"$eq": 5}


def test_eq_string() -> None:
    """$eq with string value."""
    op = Eq(value="active")
    assert op.model_dump() == {"$eq": "active"}


def test_ne() -> None:
    """$ne operator."""
    op = Ne(value="deleted")
    assert op.model_dump() == {"$ne": "deleted"}


def test_gt() -> None:
    """$gt operator."""
    op = Gt(value=10)
    assert op.model_dump() == {"$gt": 10}


def test_gte() -> None:
    """$gte operator."""
    op = Gte(value=18)
    assert op.model_dump() == {"$gte": 18}


def test_lt() -> None:
    """$lt operator."""
    op = Lt(value=100)
    assert op.model_dump() == {"$lt": 100}


def test_lte() -> None:
    """$lte operator."""
    op = Lte(value=65)
    assert op.model_dump() == {"$lte": 65}


# --- In/Nin Tests ---


def test_in() -> None:
    """$in operator."""
    op = In(values=[1, 2, 3])
    assert op.model_dump() == {"$in": [1, 2, 3]}


def test_in_strings() -> None:
    """$in with string values."""
    op = In(values=["active", "pending", "review"])
    assert op.model_dump() == {"$in": ["active", "pending", "review"]}


def test_nin() -> None:
    """$nin operator."""
    op = Nin(values=["deleted", "archived"])
    assert op.model_dump() == {"$nin": ["deleted", "archived"]}


# --- Regex Tests ---


def test_regex_simple() -> None:
    """$regex with pattern only."""
    op = Regex(pattern="^test")
    assert op.model_dump() == {"$regex": "^test"}


def test_regex_with_options() -> None:
    """$regex with options."""
    op = Regex(pattern="^test", options="i")
    assert op.model_dump() == {"$regex": "^test", "$options": "i"}


def test_regex_multiple_options() -> None:
    """$regex with multiple options."""
    op = Regex(pattern="pattern", options="im")
    assert op.model_dump() == {"$regex": "pattern", "$options": "im"}


# --- Exists Tests ---


def test_exists_true() -> None:
    """$exists true."""
    op = Exists(exists=True)
    assert op.model_dump() == {"$exists": True}


def test_exists_false() -> None:
    """$exists false."""
    op = Exists(exists=False)
    assert op.model_dump() == {"$exists": False}


def test_exists_default() -> None:
    """$exists defaults to true."""
    op = Exists()
    assert op.model_dump() == {"$exists": True}


# --- Type Tests ---


def test_type_string() -> None:
    """$type with string type."""
    op = Type(bson_type="string")
    assert op.model_dump() == {"$type": "string"}


def test_type_number() -> None:
    """$type with numeric type."""
    op = Type(bson_type=2)
    assert op.model_dump() == {"$type": 2}


def test_type_list() -> None:
    """$type with multiple types."""
    op = Type(bson_type=["string", "int"])
    assert op.model_dump() == {"$type": ["string", "int"]}


# --- Array Operators Tests ---


def test_elem_match() -> None:
    """$elemMatch operator."""
    op = ElemMatch(
        conditions={
            "quantity": {"$gt": 5},
            "price": {"$lt": 100},
        }
    )
    assert op.model_dump() == {
        "$elemMatch": {
            "quantity": {"$gt": 5},
            "price": {"$lt": 100},
        }
    }


def test_size() -> None:
    """$size operator."""
    op = Size(size=5)
    assert op.model_dump() == {"$size": 5}


def test_all() -> None:
    """$all operator."""
    op = All(values=["red", "green", "blue"])
    assert op.model_dump() == {"$all": ["red", "green", "blue"]}

"""Tests for element query operators."""

import pytest
from pydantic import ValidationError

from mongo_aggro.operators.element import Exists, Type

# --- Exists Operator Tests ---


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


def test_exists_invalid_type() -> None:
    """$exists requires boolean value."""
    with pytest.raises(ValidationError):
        Exists(exists="not a bool")  # type: ignore[arg-type]


# --- Type Operator Tests ---


def test_type_string() -> None:
    """$type with string type name."""
    op = Type(bson_type="string")
    assert op.model_dump() == {"$type": "string"}


def test_type_number() -> None:
    """$type with numeric type code."""
    op = Type(bson_type=2)
    assert op.model_dump() == {"$type": 2}


def test_type_list() -> None:
    """$type with multiple types."""
    op = Type(bson_type=["string", "int"])
    assert op.model_dump() == {"$type": ["string", "int"]}


def test_type_missing_bson_type() -> None:
    """$type requires bson_type parameter."""
    with pytest.raises(ValidationError):
        Type()  # type: ignore[call-arg]

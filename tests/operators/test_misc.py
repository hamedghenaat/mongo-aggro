"""Tests for miscellaneous query operators."""

import pytest
from pydantic import ValidationError

from mongo_aggro.operators.misc import JsonSchema, Mod, Text, Where

# --- Mod Operator Tests ---


def test_mod() -> None:
    """$mod operator with valid divisor and remainder."""
    op = Mod(divisor=4, remainder=0)
    assert op.model_dump() == {"$mod": [4, 0]}


def test_mod_non_zero_remainder() -> None:
    """$mod with non-zero remainder."""
    op = Mod(divisor=3, remainder=1)
    assert op.model_dump() == {"$mod": [3, 1]}


def test_mod_missing_divisor() -> None:
    """$mod requires divisor parameter."""
    with pytest.raises(ValidationError):
        Mod(remainder=0)  # type: ignore[call-arg]


def test_mod_missing_remainder() -> None:
    """$mod requires remainder parameter."""
    with pytest.raises(ValidationError):
        Mod(divisor=4)  # type: ignore[call-arg]


# --- JsonSchema Operator Tests ---


def test_json_schema() -> None:
    """$jsonSchema operator with valid schema."""
    op = JsonSchema(
        json_schema={
            "bsonType": "object",
            "required": ["name", "email"],
            "properties": {
                "name": {"bsonType": "string"},
                "email": {"bsonType": "string"},
            },
        }
    )
    result = op.model_dump()
    assert "$jsonSchema" in result
    assert result["$jsonSchema"]["required"] == ["name", "email"]


def test_json_schema_simple() -> None:
    """$jsonSchema with simple schema."""
    op = JsonSchema(json_schema={"bsonType": "string"})
    assert op.model_dump() == {"$jsonSchema": {"bsonType": "string"}}


def test_json_schema_missing_schema() -> None:
    """$jsonSchema requires json_schema parameter."""
    with pytest.raises(ValidationError):
        JsonSchema()  # type: ignore[call-arg]


def test_json_schema_invalid_type() -> None:
    """$jsonSchema schema must be a dict."""
    with pytest.raises(ValidationError):
        JsonSchema(json_schema="not a dict")  # type: ignore[arg-type]


# --- Where Operator Tests ---


def test_where() -> None:
    """$where operator with valid expression."""
    op = Where(expression="this.credits == this.debits")
    assert op.model_dump() == {"$where": "this.credits == this.debits"}


def test_where_function() -> None:
    """$where with function expression."""
    op = Where(expression="function() { return this.x > 0; }")
    assert op.model_dump() == {"$where": "function() { return this.x > 0; }"}


def test_where_missing_expression() -> None:
    """$where requires expression parameter."""
    with pytest.raises(ValidationError):
        Where()  # type: ignore[call-arg]


def test_where_invalid_type() -> None:
    """$where expression must be a string."""
    with pytest.raises(ValidationError):
        Where(expression=123)  # type: ignore[arg-type]


# --- Text Operator Tests ---


def test_text_simple() -> None:
    """$text operator with search term only."""
    op = Text(search="coffee shop")
    assert op.model_dump() == {"$text": {"$search": "coffee shop"}}


def test_text_with_options() -> None:
    """$text operator with options."""
    op = Text(search="coffee", language="en", case_sensitive=True)
    assert op.model_dump() == {
        "$text": {
            "$search": "coffee",
            "$language": "en",
            "$caseSensitive": True,
        }
    }


def test_text_diacritic_sensitive() -> None:
    """$text with diacritic sensitivity."""
    op = Text(search="cafe", diacritic_sensitive=True)
    result = op.model_dump()
    assert result["$text"]["$diacriticSensitive"] is True


def test_text_missing_search() -> None:
    """$text requires search parameter."""
    with pytest.raises(ValidationError):
        Text()  # type: ignore[call-arg]


def test_text_invalid_search_type() -> None:
    """$text search must be a string."""
    with pytest.raises(ValidationError):
        Text(search=123)  # type: ignore[arg-type]

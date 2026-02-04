"""Tests for document transformation aggregation stages."""

import pytest
from pydantic import ValidationError

from mongo_aggro.stages import (
    AddFields,
    Redact,
    ReplaceRoot,
    ReplaceWith,
    Set,
    Unset,
)

# --- AddFields Tests ---


def test_add_fields() -> None:
    """AddFields adds new fields."""
    add_fields = AddFields(fields={"isActive": True, "score": 100})
    assert add_fields.model_dump() == {
        "$addFields": {"isActive": True, "score": 100}
    }


def test_add_fields_with_expression() -> None:
    """AddFields with computed expression."""
    add_fields = AddFields(fields={"total": {"$sum": ["$a", "$b"]}})
    assert add_fields.model_dump() == {
        "$addFields": {"total": {"$sum": ["$a", "$b"]}}
    }


def test_add_fields_missing_fields() -> None:
    """AddFields requires fields parameter."""
    with pytest.raises(ValidationError):
        AddFields()  # type: ignore[call-arg]


# --- Set Tests ---


def test_set_fields() -> None:
    """Set is alias for AddFields."""
    set_stage = Set(fields={"status": "processed"})
    assert set_stage.model_dump() == {"$set": {"status": "processed"}}


def test_set_multiple_fields() -> None:
    """Set multiple fields at once."""
    set_stage = Set(fields={"a": 1, "b": 2, "c": {"$add": ["$x", "$y"]}})
    result = set_stage.model_dump()
    assert result["$set"]["a"] == 1
    assert result["$set"]["b"] == 2
    assert result["$set"]["c"] == {"$add": ["$x", "$y"]}


def test_set_missing_fields() -> None:
    """Set requires fields parameter."""
    with pytest.raises(ValidationError):
        Set()  # type: ignore[call-arg]


# --- Unset Tests ---


def test_unset_single() -> None:
    """Unset single field."""
    unset = Unset(fields="password")
    assert unset.model_dump() == {"$unset": "password"}


def test_unset_multiple() -> None:
    """Unset multiple fields."""
    unset = Unset(fields=["password", "secret", "token"])
    assert unset.model_dump() == {"$unset": ["password", "secret", "token"]}


def test_unset_missing_fields() -> None:
    """Unset requires fields parameter."""
    with pytest.raises(ValidationError):
        Unset()  # type: ignore[call-arg]


# --- ReplaceRoot Tests ---


def test_replace_root() -> None:
    """ReplaceRoot with field path."""
    rr = ReplaceRoot(new_root="$nested")
    assert rr.model_dump() == {"$replaceRoot": {"newRoot": "$nested"}}


def test_replace_root_expression() -> None:
    """ReplaceRoot with expression."""
    rr = ReplaceRoot(new_root={"$mergeObjects": ["$defaults", "$doc"]})
    result = rr.model_dump()
    assert result["$replaceRoot"]["newRoot"] == {
        "$mergeObjects": ["$defaults", "$doc"]
    }


def test_replace_root_missing_new_root() -> None:
    """ReplaceRoot requires new_root parameter."""
    with pytest.raises(ValidationError):
        ReplaceRoot()  # type: ignore[call-arg]


# --- ReplaceWith Tests ---


def test_replace_with() -> None:
    """ReplaceWith stage."""
    rw = ReplaceWith(expression="$embedded")
    assert rw.model_dump() == {"$replaceWith": "$embedded"}


def test_replace_with_expression() -> None:
    """ReplaceWith with expression."""
    rw = ReplaceWith(expression={"$mergeObjects": ["$a", "$b"]})
    assert rw.model_dump() == {"$replaceWith": {"$mergeObjects": ["$a", "$b"]}}


def test_replace_with_missing_expression() -> None:
    """ReplaceWith requires expression parameter."""
    with pytest.raises(ValidationError):
        ReplaceWith()  # type: ignore[call-arg]


# --- Redact Tests ---


def test_redact() -> None:
    """Redact stage."""
    redact = Redact(
        expression={
            "$cond": {
                "if": {"$eq": ["$level", 5]},
                "then": "$$PRUNE",
                "else": "$$DESCEND",
            }
        }
    )
    result = redact.model_dump()
    assert "$redact" in result
    assert "$cond" in result["$redact"]


def test_redact_simple() -> None:
    """Redact with simple expression."""
    redact = Redact(expression={"$cond": ["$public", "$$DESCEND", "$$PRUNE"]})
    result = redact.model_dump()
    assert result["$redact"]["$cond"] == ["$public", "$$DESCEND", "$$PRUNE"]


def test_redact_missing_expression() -> None:
    """Redact requires expression parameter."""
    with pytest.raises(ValidationError):
        Redact()  # type: ignore[call-arg]

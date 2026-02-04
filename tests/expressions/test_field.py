"""Tests for Field class and F helper function.

This module tests:
- Field path creation with $ prefix
- Nested path handling
- Field repr and string output
- Field hashability for use in sets/dicts
"""

from mongo_aggro.expressions import F

# --- Field Creation Tests ---


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


def test_field_double_dollar_prefix() -> None:
    """Field preserves $$ prefix for variables."""
    field = F("$$this.value")
    assert str(field) == "$$this.value"


# --- Field Repr Tests ---


def test_field_repr() -> None:
    """Field has readable repr."""
    field = F("status")
    assert repr(field) == "Field('$status')"


def test_field_repr_nested() -> None:
    """Field repr works with nested paths."""
    field = F("user.profile.name")
    assert repr(field) == "Field('$user.profile.name')"


# --- Field Hashability Tests ---


def test_field_is_hashable() -> None:
    """Field can be used in sets/dicts."""
    field = F("status")
    field_set = {field}
    assert len(field_set) == 1


def test_field_hash_consistency() -> None:
    """Same path produces same hash."""
    field1 = F("status")
    field2 = F("status")
    assert hash(field1) == hash(field2)


# --- Field Sad Paths Tests ---


def test_field_empty_path_allowed() -> None:
    """Empty string path creates valid field (MongoDB will handle)."""
    field = F("")
    assert str(field) == "$"


def test_field_whitespace_path() -> None:
    """Whitespace path is allowed (MongoDB will validate)."""
    field = F("  ")
    assert str(field) == "$  "

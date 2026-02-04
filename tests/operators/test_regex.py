"""Tests for regex query operator."""

import pytest
from pydantic import ValidationError

from mongo_aggro.operators.regex import Regex

# --- Regex Operator Tests ---


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


def test_regex_missing_pattern() -> None:
    """$regex requires pattern parameter."""
    with pytest.raises(ValidationError):
        Regex()  # type: ignore[call-arg]


def test_regex_invalid_pattern_type() -> None:
    """$regex pattern must be a string."""
    with pytest.raises(ValidationError):
        Regex(pattern=123)  # type: ignore[arg-type]

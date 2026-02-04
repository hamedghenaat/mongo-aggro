"""Tests for bitwise query operators."""

import pytest
from pydantic import ValidationError

from mongo_aggro.operators.bitwise import (
    BitsAllClear,
    BitsAllSet,
    BitsAnyClear,
    BitsAnySet,
)

# --- BitsAllClear Operator Tests ---


def test_bits_all_clear_mask() -> None:
    """$bitsAllClear with bitmask."""
    op = BitsAllClear(mask=35)
    assert op.model_dump() == {"$bitsAllClear": 35}


def test_bits_all_clear_positions() -> None:
    """$bitsAllClear with bit positions."""
    op = BitsAllClear(mask=[1, 5])
    assert op.model_dump() == {"$bitsAllClear": [1, 5]}


def test_bits_all_clear_missing_mask() -> None:
    """$bitsAllClear requires mask parameter."""
    with pytest.raises(ValidationError):
        BitsAllClear()  # type: ignore[call-arg]


# --- BitsAllSet Operator Tests ---


def test_bits_all_set() -> None:
    """$bitsAllSet operator with bitmask."""
    op = BitsAllSet(mask=35)
    assert op.model_dump() == {"$bitsAllSet": 35}


def test_bits_all_set_positions() -> None:
    """$bitsAllSet with bit positions."""
    op = BitsAllSet(mask=[0, 2, 4])
    assert op.model_dump() == {"$bitsAllSet": [0, 2, 4]}


def test_bits_all_set_missing_mask() -> None:
    """$bitsAllSet requires mask parameter."""
    with pytest.raises(ValidationError):
        BitsAllSet()  # type: ignore[call-arg]


# --- BitsAnyClear Operator Tests ---


def test_bits_any_clear() -> None:
    """$bitsAnyClear operator with bit positions."""
    op = BitsAnyClear(mask=[1, 5])
    assert op.model_dump() == {"$bitsAnyClear": [1, 5]}


def test_bits_any_clear_mask() -> None:
    """$bitsAnyClear with bitmask."""
    op = BitsAnyClear(mask=16)
    assert op.model_dump() == {"$bitsAnyClear": 16}


def test_bits_any_clear_missing_mask() -> None:
    """$bitsAnyClear requires mask parameter."""
    with pytest.raises(ValidationError):
        BitsAnyClear()  # type: ignore[call-arg]


# --- BitsAnySet Operator Tests ---


def test_bits_any_set() -> None:
    """$bitsAnySet operator with bitmask."""
    op = BitsAnySet(mask=35)
    assert op.model_dump() == {"$bitsAnySet": 35}


def test_bits_any_set_positions() -> None:
    """$bitsAnySet with bit positions."""
    op = BitsAnySet(mask=[1, 3, 5])
    assert op.model_dump() == {"$bitsAnySet": [1, 3, 5]}


def test_bits_any_set_missing_mask() -> None:
    """$bitsAnySet requires mask parameter."""
    with pytest.raises(ValidationError):
        BitsAnySet()  # type: ignore[call-arg]

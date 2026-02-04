"""Tests for array-related aggregation stages."""

import pytest
from pydantic import ValidationError

from mongo_aggro.stages import Unwind


def test_unwind_simple() -> None:
    """Simple unwind without options."""
    unwind = Unwind(path="items")
    assert unwind.model_dump() == {"$unwind": "$items"}


def test_unwind_with_dollar() -> None:
    """Unwind path already has $."""
    unwind = Unwind(path="$items")
    assert unwind.model_dump() == {"$unwind": "$items"}


def test_unwind_with_index() -> None:
    """Unwind with includeArrayIndex."""
    unwind = Unwind(path="items", include_array_index="idx")
    result = unwind.model_dump()
    assert result == {
        "$unwind": {
            "path": "$items",
            "includeArrayIndex": "idx",
        }
    }


def test_unwind_preserve_null() -> None:
    """Unwind with preserveNullAndEmptyArrays."""
    unwind = Unwind(path="items", preserve_null_and_empty=True)
    result = unwind.model_dump()
    assert result["$unwind"]["preserveNullAndEmptyArrays"] is True


def test_unwind_all_options() -> None:
    """Unwind with all options."""
    unwind = Unwind(
        path="items",
        include_array_index="itemIndex",
        preserve_null_and_empty=True,
    )
    result = unwind.model_dump()
    assert result == {
        "$unwind": {
            "path": "$items",
            "includeArrayIndex": "itemIndex",
            "preserveNullAndEmptyArrays": True,
        }
    }


def test_unwind_preserve_false() -> None:
    """Unwind with preserveNullAndEmptyArrays set to false."""
    unwind = Unwind(path="items", preserve_null_and_empty=False)
    result = unwind.model_dump()
    assert result["$unwind"]["preserveNullAndEmptyArrays"] is False


def test_unwind_missing_path() -> None:
    """Unwind requires path parameter."""
    with pytest.raises(ValidationError):
        Unwind()  # type: ignore[call-arg]


def test_unwind_rejects_extra_fields() -> None:
    """Unwind rejects unknown fields."""
    with pytest.raises(ValidationError):
        Unwind(path="items", unknown="value")  # type: ignore[call-arg]

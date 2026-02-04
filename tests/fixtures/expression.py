"""Expression-related test fixtures."""

import pytest

from mongo_aggro.expressions import F, Field


@pytest.fixture
def age_field() -> Field:
    """Return an age field reference."""
    return F("age")

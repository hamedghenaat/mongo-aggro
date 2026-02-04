"""Bitwise query operators for MongoDB aggregation."""

from typing import Any

from pydantic import Field

from mongo_aggro.operators.base import QueryOperator


class BitsAllClear(QueryOperator):
    """
    $bitsAllClear operator - matches where all bit positions are 0.

    Example:
        >>> BitsAllClear(mask=35).model_dump()
        {"$bitsAllClear": 35}

        >>> BitsAllClear(mask=[1, 5]).model_dump()
        {"$bitsAllClear": [1, 5]}
    """

    mask: int | list[int] = Field(
        ..., description="Bitmask or array of bit positions"
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return {"$bitsAllClear": self.mask}


class BitsAllSet(QueryOperator):
    """
    $bitsAllSet operator - matches where all bit positions are 1.

    Example:
        >>> BitsAllSet(mask=35).model_dump()
        {"$bitsAllSet": 35}
    """

    mask: int | list[int] = Field(
        ..., description="Bitmask or array of bit positions"
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return {"$bitsAllSet": self.mask}


class BitsAnyClear(QueryOperator):
    """
    $bitsAnyClear operator - matches where any bit position is 0.

    Example:
        >>> BitsAnyClear(mask=35).model_dump()
        {"$bitsAnyClear": 35}
    """

    mask: int | list[int] = Field(
        ..., description="Bitmask or array of bit positions"
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return {"$bitsAnyClear": self.mask}


class BitsAnySet(QueryOperator):
    """
    $bitsAnySet operator - matches where any bit position is 1.

    Example:
        >>> BitsAnySet(mask=35).model_dump()
        {"$bitsAnySet": 35}
    """

    mask: int | list[int] = Field(
        ..., description="Bitmask or array of bit positions"
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return {"$bitsAnySet": self.mask}


__all__ = ["BitsAllClear", "BitsAllSet", "BitsAnyClear", "BitsAnySet"]

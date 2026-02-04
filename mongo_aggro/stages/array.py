"""Array-related MongoDB aggregation pipeline stages.

This module contains stages for working with array fields, primarily Unwind.
"""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from mongo_aggro.base import BaseStage


class Unwind(BaseModel, BaseStage):
    """
    $unwind stage - deconstructs an array field.

    Example:
        >>> Unwind(path="cars").model_dump()
        {"$unwind": "$cars"}

        >>> # With options
        >>> Unwind(
        ...     path="items",
        ...     include_array_index="itemIndex",
        ...     preserve_null_and_empty=True
        ... ).model_dump()
        {"$unwind": {
            "path": "$items",
            "includeArrayIndex": "itemIndex",
            "preserveNullAndEmptyArrays": true
        }}
    """

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    path: str = Field(..., description="Array field path (without $)")
    include_array_index: str | None = Field(
        default=None,
        validation_alias="includeArrayIndex",
        serialization_alias="includeArrayIndex",
        description="Name of index field",
    )
    preserve_null_and_empty: bool | None = Field(
        default=None,
        validation_alias="preserveNullAndEmptyArrays",
        serialization_alias="preserveNullAndEmptyArrays",
        description="Output doc if array is null/empty/missing",
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        field_path = (
            f"${self.path}" if not self.path.startswith("$") else self.path
        )

        if (
            self.include_array_index is None
            and self.preserve_null_and_empty is None
        ):
            return {"$unwind": field_path}

        result: dict[str, Any] = {"path": field_path}
        if self.include_array_index is not None:
            result["includeArrayIndex"] = self.include_array_index
        if self.preserve_null_and_empty is not None:
            result["preserveNullAndEmptyArrays"] = self.preserve_null_and_empty
        return {"$unwind": result}


__all__ = [
    "Unwind",
]

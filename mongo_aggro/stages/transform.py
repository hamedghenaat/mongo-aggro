"""Document transformation MongoDB aggregation pipeline stages.

This module contains stages for transforming document structure:
AddFields, Set, Unset, ReplaceRoot, ReplaceWith, and Redact.
"""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class AddFields(BaseModel):
    """
    $addFields stage - adds new fields to documents.

    Example:
        >>> AddFields(fields={"isActive": True, "score": {"$sum": "$marks"}})
        {"$addFields": {"isActive": true, "score": {"$sum": "$marks"}}}
    """

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    fields: dict[str, Any] = Field(..., description="Fields to add")

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return {"$addFields": self.fields}


class Set(BaseModel):
    """
    $set stage - alias for $addFields.

    Example:
        >>> Set(fields={"status": "processed"}).model_dump()
        {"$set": {"status": "processed"}}
    """

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    fields: dict[str, Any] = Field(..., description="Fields to set")

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return {"$set": self.fields}


class Unset(BaseModel):
    """
    $unset stage - removes fields from documents.

    Example:
        >>> Unset(fields=["password", "secret"]).model_dump()
        {"$unset": ["password", "secret"]}

        >>> Unset(fields="temporaryField").model_dump()
        {"$unset": "temporaryField"}
    """

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    fields: str | list[str] = Field(..., description="Field(s) to remove")

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return {"$unset": self.fields}


class ReplaceRoot(BaseModel):
    """
    $replaceRoot stage - replaces document with specified embedded document.

    Example:
        >>> ReplaceRoot(new_root="$nested").model_dump()
        {"$replaceRoot": {"newRoot": "$nested"}}
    """

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    new_root: str | dict[str, Any] = Field(
        ...,
        validation_alias="newRoot",
        serialization_alias="newRoot",
        description="Expression for new root",
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return {"$replaceRoot": {"newRoot": self.new_root}}


class ReplaceWith(BaseModel):
    """
    $replaceWith stage - replaces document (alias for $replaceRoot).

    Example:
        >>> ReplaceWith(expression="$embedded").model_dump()
        {"$replaceWith": "$embedded"}
    """

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    expression: str | dict[str, Any] = Field(
        ..., description="Expression for new document"
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return {"$replaceWith": self.expression}


class Redact(BaseModel):
    """
    $redact stage - restricts document content based on stored info.

    Example:
        >>> Redact(expression={
        ...     "$cond": {
        ...         "if": {"$eq": ["$level", 5]},
        ...         "then": "$$PRUNE",
        ...         "else": "$$DESCEND"
        ...     }
        ... }).model_dump()
    """

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    expression: dict[str, Any] = Field(..., description="Redaction expression")

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return {"$redact": self.expression}


__all__ = [
    "AddFields",
    "Set",
    "Unset",
    "ReplaceRoot",
    "ReplaceWith",
    "Redact",
]

"""Change stream MongoDB aggregation pipeline stages.

This module contains stages for change stream operations:
ChangeStream and ChangeStreamSplitLargeEvent.
"""

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from mongo_aggro.base import BaseStage


class ChangeStream(BaseModel, BaseStage):
    """
    $changeStream stage - returns a change stream cursor.

    Must be the first stage in the pipeline.

    Example:
        >>> ChangeStream().model_dump()
        {"$changeStream": {}}

        >>> ChangeStream(full_document="updateLookup").model_dump()
        {"$changeStream": {"fullDocument": "updateLookup"}}
    """

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    full_document: (
        Literal["default", "updateLookup", "whenAvailable", "required"] | None
    ) = Field(
        default=None,
        serialization_alias="fullDocument",
        description="Full document option for update events",
    )
    full_document_before_change: (
        Literal["off", "whenAvailable", "required"] | None
    ) = Field(
        default=None,
        serialization_alias="fullDocumentBeforeChange",
        description="Include pre-image of modified document",
    )
    resume_after: dict[str, Any] | None = Field(
        default=None,
        serialization_alias="resumeAfter",
        description="Resume token to resume change stream",
    )
    start_after: dict[str, Any] | None = Field(
        default=None,
        serialization_alias="startAfter",
        description="Resume token to start after",
    )
    start_at_operation_time: Any | None = Field(
        default=None,
        serialization_alias="startAtOperationTime",
        description="Timestamp to start watching changes",
    )
    all_changes_for_cluster: bool | None = Field(
        default=None,
        serialization_alias="allChangesForCluster",
        description="Watch all changes for the cluster",
    )
    show_expanded_events: bool | None = Field(
        default=None,
        serialization_alias="showExpandedEvents",
        description="Show expanded change events",
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        result: dict[str, Any] = {}
        if self.full_document is not None:
            result["fullDocument"] = self.full_document
        if self.full_document_before_change is not None:
            result["fullDocumentBeforeChange"] = (
                self.full_document_before_change
            )
        if self.resume_after is not None:
            result["resumeAfter"] = self.resume_after
        if self.start_after is not None:
            result["startAfter"] = self.start_after
        if self.start_at_operation_time is not None:
            result["startAtOperationTime"] = self.start_at_operation_time
        if self.all_changes_for_cluster is not None:
            result["allChangesForCluster"] = self.all_changes_for_cluster
        if self.show_expanded_events is not None:
            result["showExpandedEvents"] = self.show_expanded_events
        return {"$changeStream": result}


class ChangeStreamSplitLargeEvent(BaseModel, BaseStage):
    """
    $changeStreamSplitLargeEvent stage - splits large change events.

    Must be the last stage in a $changeStream pipeline.

    Example:
        >>> ChangeStreamSplitLargeEvent().model_dump()
        {"$changeStreamSplitLargeEvent": {}}
    """

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return {"$changeStreamSplitLargeEvent": {}}


__all__ = [
    "ChangeStream",
    "ChangeStreamSplitLargeEvent",
]

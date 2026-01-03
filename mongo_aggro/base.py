"""Base classes for MongoDB aggregation pipeline stages."""

from abc import ABC, abstractmethod
from collections.abc import Iterator
from typing import Any

from pydantic import GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema


class BaseStage(ABC):
    """Abstract base class for all MongoDB aggregation pipeline stages."""

    @abstractmethod
    def model_dump(self) -> dict[str, Any]:
        """
        Convert the stage to its MongoDB dictionary representation.

        Returns:
            dict[str, Any]: MongoDB aggregation stage dictionary
        """
        pass


class Pipeline:
    """
    MongoDB aggregation pipeline builder.

    This class acts as a container for aggregation stages and can be
    directly passed to MongoDB's aggregate() method. It implements
    __iter__ to allow MongoDB drivers to iterate through the stages.

    Example:
        >>> pipeline = Pipeline()
        >>> pipeline.add_stage(Match(field="status", value="active"))
        >>> pipeline.add_stage(Group(id="$category", count={"$sum": 1}))
        >>> collection.aggregate(pipeline)

        >>> # Or with constructor
        >>> pipeline = Pipeline([
        ...     Match(field="status", value="active"),
        ...     Unwind(path="items")
        ... ])
    """

    def __init__(self, stages: list[BaseStage] | None = None) -> None:
        """
        Initialize the pipeline with optional initial stages.

        Args:
            stages: Optional list of initial pipeline stages
        """
        self._stages: list[BaseStage] = stages or []

    def add_stage(self, stage: BaseStage) -> "Pipeline":
        """
        Append a new stage to the pipeline.

        Args:
            stage: A pipeline stage instance

        Returns:
            Pipeline: Self for method chaining
        """
        self._stages.append(stage)
        return self

    def __iter__(self) -> Iterator[dict[str, Any]]:
        """
        Iterate through pipeline stages as dictionaries.

        This allows the pipeline to be directly passed to MongoDB's
        aggregate() method without calling any additional methods.

        Yields:
            dict[str, Any]: Each stage's MongoDB dictionary representation
        """
        for stage in self._stages:
            yield stage.model_dump()

    def __len__(self) -> int:
        """Return the number of stages in the pipeline."""
        return len(self._stages)

    def __getitem__(self, index: int) -> BaseStage:
        """Get a stage by index."""
        return self._stages[index]

    def to_list(self) -> list[dict[str, Any]]:
        """
        Convert the entire pipeline to a list of dictionaries.

        Returns:
            list[dict[str, Any]]: List of MongoDB stage dictionaries
        """
        return list(self)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        """
        Allow Pipeline to be used as a Pydantic field type.

        This enables using Pipeline in other Pydantic models,
        for example in Lookup's pipeline field.
        """
        return core_schema.is_instance_schema(cls)

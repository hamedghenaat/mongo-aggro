"""Atlas Search MongoDB aggregation pipeline stages.

This module contains stages for Atlas Search and Vector Search:
Search, SearchMeta, VectorSearch, ListSearchIndexes, and RankFusion.
"""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ListSearchIndexes(BaseModel):
    """
    $listSearchIndexes stage - lists Atlas Search indexes.

    Example:
        >>> ListSearchIndexes().model_dump()
        {"$listSearchIndexes": {}}

        >>> ListSearchIndexes(id="index_id").model_dump()
        {"$listSearchIndexes": {"id": "index_id"}}

        >>> ListSearchIndexes(name="index_name").model_dump()
        {"$listSearchIndexes": {"name": "index_name"}}
    """

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    id: str | None = Field(
        default=None,
        description="Search index ID to filter",
    )
    name: str | None = Field(
        default=None,
        description="Search index name to filter",
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        result: dict[str, Any] = {}
        if self.id is not None:
            result["id"] = self.id
        if self.name is not None:
            result["name"] = self.name
        return {"$listSearchIndexes": result}


class Search(BaseModel):
    """
    $search stage - Atlas full-text search.

    Example:
        >>> Search(index="default", text={"query": "coffee", "path": "title"})
        {"$search": {"index": "default", "text": {"query": "coffee", ...}}}
    """

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    index: str | None = Field(
        default=None,
        description="Name of the Atlas Search index",
    )
    text: dict[str, Any] | None = Field(
        default=None,
        description="Text search operator",
    )
    compound: dict[str, Any] | None = Field(
        default=None,
        description="Compound search operator",
    )
    autocomplete: dict[str, Any] | None = Field(
        default=None,
        description="Autocomplete search operator",
    )
    phrase: dict[str, Any] | None = Field(
        default=None,
        description="Phrase search operator",
    )
    wildcard: dict[str, Any] | None = Field(
        default=None,
        description="Wildcard search operator",
    )
    regex: dict[str, Any] | None = Field(
        default=None,
        description="Regex search operator",
    )
    near: dict[str, Any] | None = Field(
        default=None,
        description="Near search operator",
    )
    range: dict[str, Any] | None = Field(
        default=None,
        description="Range search operator",
    )
    exists: dict[str, Any] | None = Field(
        default=None,
        description="Exists search operator",
    )
    equals: dict[str, Any] | None = Field(
        default=None,
        description="Equals search operator",
    )
    more_like_this: dict[str, Any] | None = Field(
        default=None,
        serialization_alias="moreLikeThis",
        description="More like this search operator",
    )
    query_string: dict[str, Any] | None = Field(
        default=None,
        serialization_alias="queryString",
        description="Query string search operator",
    )
    highlight: dict[str, Any] | None = Field(
        default=None,
        description="Highlight options",
    )
    count: dict[str, Any] | None = Field(
        default=None,
        description="Count options",
    )
    return_stored_source: bool | None = Field(
        default=None,
        serialization_alias="returnStoredSource",
        description="Return stored source",
    )

    def _add_operators(self, result: dict[str, Any]) -> None:
        """Add search operators to result dict."""
        if self.text is not None:
            result["text"] = self.text
        if self.compound is not None:
            result["compound"] = self.compound
        if self.autocomplete is not None:
            result["autocomplete"] = self.autocomplete
        if self.phrase is not None:
            result["phrase"] = self.phrase
        if self.wildcard is not None:
            result["wildcard"] = self.wildcard
        if self.regex is not None:
            result["regex"] = self.regex
        if self.near is not None:
            result["near"] = self.near
        if self.range is not None:
            result["range"] = self.range

    def _add_advanced(self, result: dict[str, Any]) -> None:
        """Add advanced search options to result dict."""
        if self.exists is not None:
            result["exists"] = self.exists
        if self.equals is not None:
            result["equals"] = self.equals
        if self.more_like_this is not None:
            result["moreLikeThis"] = self.more_like_this
        if self.query_string is not None:
            result["queryString"] = self.query_string
        if self.highlight is not None:
            result["highlight"] = self.highlight
        if self.count is not None:
            result["count"] = self.count
        if self.return_stored_source is not None:
            result["returnStoredSource"] = self.return_stored_source

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        result: dict[str, Any] = {}
        if self.index is not None:
            result["index"] = self.index
        self._add_operators(result)
        self._add_advanced(result)
        return {"$search": result}


class SearchMeta(BaseModel):
    """
    $searchMeta stage - returns Atlas Search metadata.

    Example:
        >>> SearchMeta(index="default", count={"type": "total"}).model_dump()
        {"$searchMeta": {"index": "default", "count": {"type": "total"}}}
    """

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    index: str | None = Field(
        default=None,
        description="Name of the Atlas Search index",
    )
    count: dict[str, Any] | None = Field(
        default=None,
        description="Count options",
    )
    facet: dict[str, Any] | None = Field(
        default=None,
        description="Facet options",
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        result: dict[str, Any] = {}
        if self.index is not None:
            result["index"] = self.index
        if self.count is not None:
            result["count"] = self.count
        if self.facet is not None:
            result["facet"] = self.facet
        return {"$searchMeta": result}


class VectorSearch(BaseModel):
    """
    $vectorSearch stage - Atlas vector search (MongoDB 7.0.2+).

    Example:
        >>> VectorSearch(
        ...     index="vector_index",
        ...     path="embedding",
        ...     query_vector=[0.1, 0.2, 0.3],
        ...     num_candidates=100,
        ...     limit=10
        ... ).model_dump()
        {"$vectorSearch": {
            "index": "vector_index",
            "path": "embedding",
            "queryVector": [0.1, 0.2, 0.3],
            "numCandidates": 100,
            "limit": 10
        }}
    """

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    index: str = Field(
        ...,
        description="Name of the Atlas Vector Search index",
    )
    path: str = Field(
        ...,
        description="Field path containing the vector",
    )
    query_vector: list[float] = Field(
        ...,
        serialization_alias="queryVector",
        description="Query vector for similarity search",
    )
    num_candidates: int = Field(
        ...,
        serialization_alias="numCandidates",
        description="Number of candidates to consider",
    )
    limit: int = Field(
        ...,
        description="Maximum number of results to return",
    )
    filter: dict[str, Any] | None = Field(
        default=None,
        description="Pre-filter for vector search",
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        result: dict[str, Any] = {
            "index": self.index,
            "path": self.path,
            "queryVector": self.query_vector,
            "numCandidates": self.num_candidates,
            "limit": self.limit,
        }
        if self.filter is not None:
            result["filter"] = self.filter
        return {"$vectorSearch": result}


class RankFusion(BaseModel):
    """
    $rankFusion stage - combines ranked results from multiple pipelines.

    Example:
        >>> RankFusion(
        ...     input={"search": [...], "vector": [...]},
        ...     combination={"weights": {"search": 0.7, "vector": 0.3}}
        ... ).model_dump()
        {"$rankFusion": {
            "input": {"search": [...], "vector": [...]},
            "combination": {"weights": {"search": 0.7, "vector": 0.3}}
        }}
    """

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    input: dict[str, list[dict[str, Any]]] = Field(
        ...,
        description="Named input pipelines",
    )
    combination: dict[str, Any] | None = Field(
        default=None,
        description="Combination options",
    )
    score_details: bool | None = Field(
        default=None,
        serialization_alias="scoreDetails",
        description="Include score details",
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        result: dict[str, Any] = {"input": self.input}
        if self.combination is not None:
            result["combination"] = self.combination
        if self.score_details is not None:
            result["scoreDetails"] = self.score_details
        return {"$rankFusion": result}


__all__ = [
    "Search",
    "SearchMeta",
    "VectorSearch",
    "ListSearchIndexes",
    "RankFusion",
]

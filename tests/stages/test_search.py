"""Tests for Atlas Search aggregation stages."""

import pytest
from pydantic import ValidationError

from mongo_aggro.stages import (
    ListSearchIndexes,
    RankFusion,
    Search,
    SearchMeta,
    VectorSearch,
)

# --- ListSearchIndexes Tests ---


def test_list_search_indexes_empty() -> None:
    """ListSearchIndexes with no filter."""
    indexes = ListSearchIndexes()
    assert indexes.model_dump() == {"$listSearchIndexes": {}}


def test_list_search_indexes_by_id() -> None:
    """ListSearchIndexes by id."""
    indexes = ListSearchIndexes(id="index_id")
    assert indexes.model_dump() == {"$listSearchIndexes": {"id": "index_id"}}


def test_list_search_indexes_by_name() -> None:
    """ListSearchIndexes by name."""
    indexes = ListSearchIndexes(name="my_index")
    assert indexes.model_dump() == {"$listSearchIndexes": {"name": "my_index"}}


def test_list_search_indexes_rejects_extra() -> None:
    """ListSearchIndexes rejects unknown fields."""
    with pytest.raises(ValidationError):
        ListSearchIndexes(extra="value")  # type: ignore[call-arg]


# --- Search Tests ---


def test_search_text() -> None:
    """Search with text operator."""
    search = Search(index="default", text={"query": "coffee", "path": "title"})
    assert search.model_dump() == {
        "$search": {
            "index": "default",
            "text": {"query": "coffee", "path": "title"},
        }
    }


def test_search_compound() -> None:
    """Search with compound operator."""
    search = Search(
        index="default",
        compound={
            "must": [{"text": {"query": "coffee", "path": "title"}}],
            "should": [{"text": {"query": "organic", "path": "description"}}],
        },
    )
    assert search.model_dump() == {
        "$search": {
            "index": "default",
            "compound": {
                "must": [{"text": {"query": "coffee", "path": "title"}}],
                "should": [
                    {"text": {"query": "organic", "path": "description"}}
                ],
            },
        }
    }


def test_search_autocomplete() -> None:
    """Search with autocomplete operator."""
    search = Search(autocomplete={"query": "coff", "path": "title"})
    result = search.model_dump()
    assert result["$search"]["autocomplete"] == {
        "query": "coff",
        "path": "title",
    }


def test_search_phrase() -> None:
    """Search with phrase operator."""
    search = Search(phrase={"query": "hot coffee", "path": "description"})
    result = search.model_dump()
    assert result["$search"]["phrase"] == {
        "query": "hot coffee",
        "path": "description",
    }


def test_search_wildcard() -> None:
    """Search with wildcard operator."""
    search = Search(wildcard={"query": "coff*", "path": "title"})
    result = search.model_dump()
    assert result["$search"]["wildcard"] == {"query": "coff*", "path": "title"}


def test_search_regex() -> None:
    """Search with regex operator."""
    search = Search(regex={"query": "coff.*", "path": "title"})
    result = search.model_dump()
    assert result["$search"]["regex"] == {"query": "coff.*", "path": "title"}


def test_search_near() -> None:
    """Search with near operator."""
    search = Search(near={"path": "date", "origin": "2023-01-01", "pivot": 7})
    result = search.model_dump()
    assert "near" in result["$search"]


def test_search_range() -> None:
    """Search with range operator."""
    search = Search(range={"path": "price", "gte": 10, "lte": 100})
    result = search.model_dump()
    assert result["$search"]["range"] == {
        "path": "price",
        "gte": 10,
        "lte": 100,
    }


def test_search_exists() -> None:
    """Search with exists operator."""
    search = Search(exists={"path": "category"})
    result = search.model_dump()
    assert result["$search"]["exists"] == {"path": "category"}


def test_search_with_highlight() -> None:
    """Search with highlight options."""
    search = Search(
        text={"query": "coffee", "path": "description"},
        highlight={"path": "description"},
    )
    result = search.model_dump()
    assert result["$search"]["highlight"] == {"path": "description"}


def test_search_rejects_extra() -> None:
    """Search rejects unknown fields."""
    with pytest.raises(ValidationError):
        Search(unknown="value")  # type: ignore[call-arg]


# --- SearchMeta Tests ---


def test_search_meta() -> None:
    """SearchMeta stage."""
    meta = SearchMeta(index="default", count={"type": "total"})
    assert meta.model_dump() == {
        "$searchMeta": {"index": "default", "count": {"type": "total"}}
    }


def test_search_meta_facet() -> None:
    """SearchMeta with facet."""
    meta = SearchMeta(
        facet={
            "operator": {"text": {"query": "test", "path": "title"}},
            "facets": {"categories": {"type": "string", "path": "category"}},
        }
    )
    result = meta.model_dump()
    assert "facet" in result["$searchMeta"]


def test_search_meta_empty() -> None:
    """SearchMeta with no options."""
    meta = SearchMeta()
    assert meta.model_dump() == {"$searchMeta": {}}


def test_search_meta_rejects_extra() -> None:
    """SearchMeta rejects unknown fields."""
    with pytest.raises(ValidationError):
        SearchMeta(extra="value")  # type: ignore[call-arg]


# --- VectorSearch Tests ---


def test_vector_search() -> None:
    """VectorSearch stage."""
    search = VectorSearch(
        index="vector_index",
        path="embedding",
        query_vector=[0.1, 0.2, 0.3],
        num_candidates=100,
        limit=10,
    )
    assert search.model_dump() == {
        "$vectorSearch": {
            "index": "vector_index",
            "path": "embedding",
            "queryVector": [0.1, 0.2, 0.3],
            "numCandidates": 100,
            "limit": 10,
        }
    }


def test_vector_search_with_filter() -> None:
    """VectorSearch with filter."""
    search = VectorSearch(
        index="vector_index",
        path="embedding",
        query_vector=[0.1, 0.2, 0.3],
        num_candidates=100,
        limit=10,
        filter={"category": "tech"},
    )
    assert search.model_dump() == {
        "$vectorSearch": {
            "index": "vector_index",
            "path": "embedding",
            "queryVector": [0.1, 0.2, 0.3],
            "numCandidates": 100,
            "limit": 10,
            "filter": {"category": "tech"},
        }
    }


def test_vector_search_missing_required() -> None:
    """VectorSearch requires all mandatory fields."""
    with pytest.raises(ValidationError):
        VectorSearch(
            index="vector_index",
            path="embedding",
            # missing query_vector, num_candidates, limit
        )  # type: ignore[call-arg]


def test_vector_search_missing_index() -> None:
    """VectorSearch requires index."""
    with pytest.raises(ValidationError):
        VectorSearch(
            path="embedding",
            query_vector=[0.1],
            num_candidates=10,
            limit=5,
        )  # type: ignore[call-arg]


def test_vector_search_rejects_extra() -> None:
    """VectorSearch rejects unknown fields."""
    with pytest.raises(ValidationError):
        VectorSearch(
            index="idx",
            path="emb",
            query_vector=[0.1],
            num_candidates=10,
            limit=5,
            unknown="x",  # type: ignore[call-arg]
        )


# --- RankFusion Tests ---


def test_rank_fusion() -> None:
    """RankFusion stage."""
    fusion = RankFusion(
        input={
            "search": [{"$match": {"status": "active"}}],
            "vector": [{"$match": {"category": "tech"}}],
        },
        combination={"weights": {"search": 0.7, "vector": 0.3}},
    )
    assert fusion.model_dump() == {
        "$rankFusion": {
            "input": {
                "search": [{"$match": {"status": "active"}}],
                "vector": [{"$match": {"category": "tech"}}],
            },
            "combination": {"weights": {"search": 0.7, "vector": 0.3}},
        }
    }


def test_rank_fusion_minimal() -> None:
    """RankFusion with only input."""
    fusion = RankFusion(
        input={
            "a": [{"$match": {"x": 1}}],
            "b": [{"$match": {"y": 2}}],
        }
    )
    result = fusion.model_dump()
    assert result == {
        "$rankFusion": {
            "input": {
                "a": [{"$match": {"x": 1}}],
                "b": [{"$match": {"y": 2}}],
            }
        }
    }


def test_rank_fusion_with_score_details() -> None:
    """RankFusion with scoreDetails."""
    fusion = RankFusion(
        input={"a": [], "b": []},
        score_details=True,
    )
    result = fusion.model_dump()
    assert result["$rankFusion"]["scoreDetails"] is True


def test_rank_fusion_missing_input() -> None:
    """RankFusion requires input parameter."""
    with pytest.raises(ValidationError):
        RankFusion()  # type: ignore[call-arg]


def test_rank_fusion_rejects_extra() -> None:
    """RankFusion rejects unknown fields."""
    with pytest.raises(ValidationError):
        RankFusion(
            input={"a": []},
            extra="value",  # type: ignore[call-arg]
        )

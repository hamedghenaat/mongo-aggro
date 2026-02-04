"""Tests for string expression operators.

This module tests:
- ConcatExpr, SplitExpr
- ToLowerExpr, ToUpperExpr
- TrimExpr, LTrimExpr, RTrimExpr
- ReplaceOneExpr, ReplaceAllExpr
- RegexMatchExpr, RegexFindExpr, RegexFindAllExpr
- SubstrCPExpr, StrLenCPExpr, StrCaseCmpExpr
"""

import pytest
from pydantic import ValidationError

from mongo_aggro.expressions import (
    ConcatExpr,
    F,
    LTrimExpr,
    RegexFindAllExpr,
    RegexFindExpr,
    RegexMatchExpr,
    ReplaceAllExpr,
    ReplaceOneExpr,
    RTrimExpr,
    SplitExpr,
    StrCaseCmpExpr,
    StrLenCPExpr,
    SubstrCPExpr,
    ToLowerExpr,
    ToUpperExpr,
    TrimExpr,
)

# --- ConcatExpr Tests ---


def test_concat_expr() -> None:
    """ConcatExpr serialization."""
    expr = ConcatExpr(strings=[F("first"), " ", F("last")])
    assert expr.model_dump() == {"$concat": ["$first", " ", "$last"]}


def test_concat_expr_multiple_strings() -> None:
    """ConcatExpr with multiple string parts."""
    expr = ConcatExpr(strings=["Hello", " ", "World", "!"])
    assert expr.model_dump() == {"$concat": ["Hello", " ", "World", "!"]}


def test_concat_expr_missing_strings_raises() -> None:
    """ConcatExpr requires strings list."""
    with pytest.raises(ValidationError):
        ConcatExpr()  # type: ignore[call-arg]


# --- SplitExpr Tests ---


def test_split_expr() -> None:
    """SplitExpr serialization."""
    expr = SplitExpr(input=F("fullName"), delimiter=" ")
    assert expr.model_dump() == {"$split": ["$fullName", " "]}


def test_split_expr_missing_input_raises() -> None:
    """SplitExpr requires input."""
    with pytest.raises(ValidationError):
        SplitExpr(delimiter=" ")  # type: ignore[call-arg]


def test_split_expr_missing_delimiter_raises() -> None:
    """SplitExpr requires delimiter."""
    with pytest.raises(ValidationError):
        SplitExpr(input=F("text"))  # type: ignore[call-arg]


# --- Case Expressions Tests ---


def test_tolower_expr() -> None:
    """ToLowerExpr serialization."""
    expr = ToLowerExpr(input=F("name"))
    assert expr.model_dump() == {"$toLower": "$name"}


def test_toupper_expr() -> None:
    """ToUpperExpr serialization."""
    expr = ToUpperExpr(input=F("name"))
    assert expr.model_dump() == {"$toUpper": "$name"}


def test_tolower_expr_missing_input_raises() -> None:
    """ToLowerExpr requires input."""
    with pytest.raises(ValidationError):
        ToLowerExpr()  # type: ignore[call-arg]


# --- Trim Expressions Tests ---


def test_trim_expr() -> None:
    """TrimExpr serialization."""
    expr = TrimExpr(input=F("text"))
    assert expr.model_dump() == {"$trim": {"input": "$text"}}


def test_trim_expr_with_chars() -> None:
    """TrimExpr with custom chars."""
    expr = TrimExpr(input=F("text"), chars=" -")
    assert expr.model_dump() == {"$trim": {"input": "$text", "chars": " -"}}


def test_ltrim_expr() -> None:
    """LTrimExpr serialization."""
    expr = LTrimExpr(input=F("text"))
    assert expr.model_dump() == {"$ltrim": {"input": "$text"}}


def test_rtrim_expr() -> None:
    """RTrimExpr serialization."""
    expr = RTrimExpr(input=F("text"))
    assert expr.model_dump() == {"$rtrim": {"input": "$text"}}


def test_trim_expr_missing_input_raises() -> None:
    """TrimExpr requires input."""
    with pytest.raises(ValidationError):
        TrimExpr()  # type: ignore[call-arg]


# --- Replace Expressions Tests ---


def test_replace_one_expr() -> None:
    """ReplaceOneExpr serialization."""
    expr = ReplaceOneExpr(input=F("text"), find="old", replacement="new")
    assert expr.model_dump() == {
        "$replaceOne": {
            "input": "$text",
            "find": "old",
            "replacement": "new",
        }
    }


def test_replace_all_expr() -> None:
    """ReplaceAllExpr serialization."""
    expr = ReplaceAllExpr(input=F("text"), find="old", replacement="new")
    assert expr.model_dump() == {
        "$replaceAll": {
            "input": "$text",
            "find": "old",
            "replacement": "new",
        }
    }


def test_replace_one_missing_find_raises() -> None:
    """ReplaceOneExpr requires find."""
    with pytest.raises(ValidationError):
        ReplaceOneExpr(input=F("text"), replacement="new")  # type: ignore[call-arg]


# --- Regex Expressions Tests ---


def test_regex_match_expr() -> None:
    """RegexMatchExpr serialization."""
    expr = RegexMatchExpr(input=F("email"), regex=r"@.*\.com$")
    assert expr.model_dump() == {
        "$regexMatch": {"input": "$email", "regex": r"@.*\.com$"}
    }


def test_regex_match_expr_with_options() -> None:
    """RegexMatchExpr with options."""
    expr = RegexMatchExpr(input=F("text"), regex=r"pattern", options="i")
    result = expr.model_dump()
    assert result["$regexMatch"]["options"] == "i"


def test_regex_find_expr() -> None:
    """RegexFindExpr serialization."""
    expr = RegexFindExpr(input=F("text"), regex=r"\d+")
    assert expr.model_dump() == {
        "$regexFind": {"input": "$text", "regex": r"\d+"}
    }


def test_regex_find_all_expr() -> None:
    """RegexFindAllExpr serialization."""
    expr = RegexFindAllExpr(input=F("text"), regex=r"\w+")
    assert expr.model_dump() == {
        "$regexFindAll": {"input": "$text", "regex": r"\w+"}
    }


def test_regex_match_missing_regex_raises() -> None:
    """RegexMatchExpr requires regex."""
    with pytest.raises(ValidationError):
        RegexMatchExpr(input=F("text"))  # type: ignore[call-arg]


# --- Substring Expressions Tests ---


def test_substr_cp_expr() -> None:
    """SubstrCPExpr serialization."""
    expr = SubstrCPExpr(input=F("text"), start=0, length=5)
    assert expr.model_dump() == {"$substrCP": ["$text", 0, 5]}


def test_str_len_cp_expr() -> None:
    """StrLenCPExpr serialization."""
    expr = StrLenCPExpr(input=F("text"))
    assert expr.model_dump() == {"$strLenCP": "$text"}


def test_str_case_cmp_expr() -> None:
    """StrCaseCmpExpr serialization."""
    expr = StrCaseCmpExpr(first=F("a"), second=F("b"))
    assert expr.model_dump() == {"$strcasecmp": ["$a", "$b"]}


def test_substr_cp_missing_start_raises() -> None:
    """SubstrCPExpr requires start."""
    with pytest.raises(ValidationError):
        SubstrCPExpr(input=F("text"), length=5)  # type: ignore[call-arg]


def test_substr_cp_missing_length_raises() -> None:
    """SubstrCPExpr requires length."""
    with pytest.raises(ValidationError):
        SubstrCPExpr(input=F("text"), start=0)  # type: ignore[call-arg]

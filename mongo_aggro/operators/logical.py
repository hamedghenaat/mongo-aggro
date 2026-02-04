"""Logical query operators for MongoDB aggregation."""

from typing import Any

from pydantic import Field

from mongo_aggro.operators.base import QueryOperator


class And(QueryOperator):
    """
    Logical AND operator for combining multiple conditions.

    Example:
        >>> And(conditions=[
        ...     {"status": "active"},
        ...     {"age": {"$gt": 18}}
        ... ]).model_dump()
        {"$and": [{"status": "active"}, {"age": {"$gt": 18}}]}
    """

    conditions: list[dict[str, Any]] = Field(
        ..., description="List of conditions to AND together"
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return {"$and": self.conditions}


class Or(QueryOperator):
    """
    Logical OR operator for combining multiple conditions.

    Example:
        >>> Or(conditions=[
        ...     {"status": "active"},
        ...     {"status": "pending"}
        ... ]).model_dump()
        {"$or": [{"status": "active"}, {"status": "pending"}]}
    """

    conditions: list[dict[str, Any]] = Field(
        ..., description="List of conditions to OR together"
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return {"$or": self.conditions}


class Not(QueryOperator):
    """
    Logical NOT operator for negating a condition.

    Example:
        >>> Not(condition={"$regex": "^test"}).model_dump()
        {"$not": {"$regex": "^test"}}
    """

    condition: dict[str, Any] = Field(..., description="Condition to negate")

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return {"$not": self.condition}


class Nor(QueryOperator):
    """
    Logical NOR operator - matches documents that fail all conditions.

    Example:
        >>> Nor(conditions=[
        ...     {"price": {"$gt": 1000}},
        ...     {"rating": {"$lt": 3}}
        ... ]).model_dump()
        {"$nor": [{"price": {"$gt": 1000}}, {"rating": {"$lt": 3}}]}
    """

    conditions: list[dict[str, Any]] = Field(
        ..., description="List of conditions to NOR together"
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return {"$nor": self.conditions}


class Expr(QueryOperator):
    """
    $expr operator for using aggregation expressions in queries.

    Accepts both raw dicts and expression objects (EqExpr, AndExpr, etc.).
    Expression objects are automatically serialized via model_dump().

    Example:
        >>> Expr(expression={"$eq": ["$field1", "$field2"]}).model_dump()
        {"$expr": {"$eq": ["$field1", "$field2"]}}

        >>> from mongo_aggro.expressions import F, EqExpr
        >>> Expr(expression=(F("status") == "active")).model_dump()
        {"$expr": {"$eq": ["$status", "active"]}}
    """

    expression: Any = Field(
        ..., description="Aggregation expression (dict or ExpressionBase)"
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        from mongo_aggro.base import serialize_value

        return {"$expr": serialize_value(self.expression)}


__all__ = ["And", "Or", "Not", "Nor", "Expr"]

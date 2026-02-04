"""Query and expression operators for MongoDB aggregation."""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class QueryOperator(BaseModel):
    """Base class for query operators used in $match and other stages."""

    model_config = ConfigDict(
        populate_by_name=True,
        extra="forbid",
    )


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


# Comparison operators
class Eq(QueryOperator):
    """$eq comparison operator."""

    value: Any = Field(..., description="Value to compare")

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return {"$eq": self.value}


class Ne(QueryOperator):
    """$ne (not equal) comparison operator."""

    value: Any = Field(..., description="Value to compare")

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return {"$ne": self.value}


class Gt(QueryOperator):
    """$gt (greater than) comparison operator."""

    value: Any = Field(..., description="Value to compare")

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return {"$gt": self.value}


class Gte(QueryOperator):
    """$gte (greater than or equal) comparison operator."""

    value: Any = Field(..., description="Value to compare")

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return {"$gte": self.value}


class Lt(QueryOperator):
    """$lt (less than) comparison operator."""

    value: Any = Field(..., description="Value to compare")

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return {"$lt": self.value}


class Lte(QueryOperator):
    """$lte (less than or equal) comparison operator."""

    value: Any = Field(..., description="Value to compare")

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return {"$lte": self.value}


class In(QueryOperator):
    """$in operator - matches any value in the array."""

    values: list[Any] = Field(..., description="List of values to match")

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return {"$in": self.values}


class Nin(QueryOperator):
    """$nin operator - matches none of the values in the array."""

    values: list[Any] = Field(..., description="List of values to exclude")

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return {"$nin": self.values}


class Regex(QueryOperator):
    """$regex operator for pattern matching."""

    pattern: str = Field(..., description="Regular expression pattern")
    options: str | None = Field(
        default=None, description="Regex options (i, m, x, s)"
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        result: dict[str, Any] = {"$regex": self.pattern}
        if self.options:
            result["$options"] = self.options
        return result


class Exists(QueryOperator):
    """$exists operator - matches documents where field exists/doesn't."""

    exists: bool = Field(
        default=True, description="True if field should exist"
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return {"$exists": self.exists}


class Type(QueryOperator):
    """$type operator - matches documents where field is of specified type."""

    bson_type: str | int | list[str | int] = Field(
        ..., description="BSON type(s) to match"
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return {"$type": self.bson_type}


class ElemMatch(QueryOperator):
    """$elemMatch operator - matches array elements."""

    conditions: dict[str, Any] = Field(
        ..., description="Conditions for array elements"
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return {"$elemMatch": self.conditions}


class Size(QueryOperator):
    """$size operator - matches arrays with specific length."""

    size: int = Field(..., description="Array size to match")

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return {"$size": self.size}


class All(QueryOperator):
    """$all operator - matches arrays containing all specified elements."""

    values: list[Any] = Field(
        ..., description="Values that must all be present"
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return {"$all": self.values}


# --- Bitwise Query Operators ---


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


# --- Geospatial Query Operators ---


class GeoIntersects(QueryOperator):
    """
    $geoIntersects operator - matches geometries that intersect.

    Example:
        >>> GeoIntersects(geometry={
        ...     "type": "Polygon",
        ...     "coordinates": [[[-100, 60], [-100, 0], [100, 0], [100, 60]]]
        ... }).model_dump()
        {"$geoIntersects": {"$geometry": {...}}}
    """

    geometry: dict[str, Any] = Field(
        ..., description="GeoJSON geometry object"
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return {"$geoIntersects": {"$geometry": self.geometry}}


class GeoWithin(QueryOperator):
    """
    $geoWithin operator - matches geometries within a bounding region.

    Example:
        >>> GeoWithin(geometry={
        ...     "type": "Polygon",
        ...     "coordinates": [[[-100, 60], [-100, 0], [100, 0], [100, 60]]]
        ... }).model_dump()
        {"$geoWithin": {"$geometry": {...}}}

        >>> # Using legacy shapes
        >>> GeoWithin(box=[[-100, -100], [100, 100]]).model_dump()
        {"$geoWithin": {"$box": [[-100, -100], [100, 100]]}}
    """

    geometry: dict[str, Any] | None = Field(
        default=None, description="GeoJSON geometry object"
    )
    box: list[list[float]] | None = Field(
        default=None, description="Legacy box coordinates [[x1,y1], [x2,y2]]"
    )
    polygon: list[list[float]] | None = Field(
        default=None, description="Legacy polygon coordinates"
    )
    center: list[Any] | None = Field(
        default=None, description="Legacy center coordinates [[x,y], radius]"
    )
    center_sphere: list[Any] | None = Field(
        default=None,
        serialization_alias="centerSphere",
        description="Center sphere [[x,y], radius]",
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        result: dict[str, Any] = {}
        if self.geometry is not None:
            result["$geometry"] = self.geometry
        if self.box is not None:
            result["$box"] = self.box
        if self.polygon is not None:
            result["$polygon"] = self.polygon
        if self.center is not None:
            result["$center"] = self.center
        if self.center_sphere is not None:
            result["$centerSphere"] = self.center_sphere
        return {"$geoWithin": result}


class Near(QueryOperator):
    """
    $near operator - matches geospatial objects near a point.

    Example:
        >>> Near(
        ...     geometry={"type": "Point", "coordinates": [-73.9667, 40.78]},
        ...     max_distance=5000,
        ...     min_distance=1000
        ... ).model_dump()
        {"$near": {"$geometry": {...}, "$maxDistance": 5000, "$minDistance": 1000}}
    """

    geometry: dict[str, Any] | None = Field(
        default=None, description="GeoJSON point"
    )
    max_distance: float | None = Field(
        default=None,
        serialization_alias="$maxDistance",
        description="Maximum distance in meters",
    )
    min_distance: float | None = Field(
        default=None,
        serialization_alias="$minDistance",
        description="Minimum distance in meters",
    )
    # Legacy 2d index format
    legacy_point: list[float] | None = Field(
        default=None, description="Legacy [x, y] coordinates"
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        if self.legacy_point is not None:
            result: dict[str, Any] = {"$near": self.legacy_point}
            if self.max_distance is not None:
                result["$maxDistance"] = self.max_distance
            return result
        result = {}
        if self.geometry is not None:
            result["$geometry"] = self.geometry
        if self.max_distance is not None:
            result["$maxDistance"] = self.max_distance
        if self.min_distance is not None:
            result["$minDistance"] = self.min_distance
        return {"$near": result}


class NearSphere(QueryOperator):
    """
    $nearSphere operator - matches geospatial objects near a point on sphere.

    Example:
        >>> NearSphere(
        ...     geometry={"type": "Point", "coordinates": [-73.9667, 40.78]},
        ...     max_distance=5000
        ... ).model_dump()
        {"$nearSphere": {"$geometry": {...}, "$maxDistance": 5000}}
    """

    geometry: dict[str, Any] | None = Field(
        default=None, description="GeoJSON point"
    )
    max_distance: float | None = Field(
        default=None,
        serialization_alias="$maxDistance",
        description="Maximum distance in meters",
    )
    min_distance: float | None = Field(
        default=None,
        serialization_alias="$minDistance",
        description="Minimum distance in meters",
    )
    legacy_point: list[float] | None = Field(
        default=None, description="Legacy [x, y] coordinates"
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        if self.legacy_point is not None:
            result: dict[str, Any] = {"$nearSphere": self.legacy_point}
            if self.max_distance is not None:
                result["$maxDistance"] = self.max_distance
            return result
        result = {}
        if self.geometry is not None:
            result["$geometry"] = self.geometry
        if self.max_distance is not None:
            result["$maxDistance"] = self.max_distance
        if self.min_distance is not None:
            result["$minDistance"] = self.min_distance
        return {"$nearSphere": result}


# --- Miscellaneous Query Operators ---


class Mod(QueryOperator):
    """
    $mod operator - matches where field % divisor == remainder.

    Example:
        >>> Mod(divisor=4, remainder=0).model_dump()
        {"$mod": [4, 0]}
    """

    divisor: int = Field(..., description="The divisor value")
    remainder: int = Field(..., description="The remainder value")

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return {"$mod": [self.divisor, self.remainder]}


class JsonSchema(QueryOperator):
    """
    $jsonSchema operator - validates documents against JSON Schema.

    Example:
        >>> JsonSchema(json_schema={
        ...     "bsonType": "object",
        ...     "required": ["name", "email"],
        ...     "properties": {
        ...         "name": {"bsonType": "string"},
        ...         "email": {"bsonType": "string"}
        ...     }
        ... }).model_dump()
        {"$jsonSchema": {...}}
    """

    json_schema: dict[str, Any] = Field(
        ..., description="JSON Schema document"
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return {"$jsonSchema": self.json_schema}


class Where(QueryOperator):
    """
    $where operator - matches using JavaScript expression.

    Note: $where is slow and should be avoided when possible.

    Example:
        >>> Where(expression="this.credits == this.debits").model_dump()
        {"$where": "this.credits == this.debits"}
    """

    expression: str = Field(..., description="JavaScript expression string")

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return {"$where": self.expression}


class Text(QueryOperator):
    """
    $text operator - performs text search on indexed fields.

    Example:
        >>> Text(search="coffee shop", language="en").model_dump()
        {"$text": {"$search": "coffee shop", "$language": "en"}}
    """

    search: str = Field(..., description="Text to search for")
    language: str | None = Field(
        default=None, description="Language for text search"
    )
    case_sensitive: bool | None = Field(
        default=None,
        serialization_alias="$caseSensitive",
        description="Enable case sensitivity",
    )
    diacritic_sensitive: bool | None = Field(
        default=None,
        serialization_alias="$diacriticSensitive",
        description="Enable diacritic sensitivity",
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        result: dict[str, Any] = {"$search": self.search}
        if self.language is not None:
            result["$language"] = self.language
        if self.case_sensitive is not None:
            result["$caseSensitive"] = self.case_sensitive
        if self.diacritic_sensitive is not None:
            result["$diacriticSensitive"] = self.diacritic_sensitive
        return {"$text": result}

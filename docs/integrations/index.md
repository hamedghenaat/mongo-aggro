# ODM Integrations

Mongo Aggro is designed to work seamlessly with popular MongoDB ODMs
(Object-Document Mappers) in Python. This section covers integration
patterns with:

- **[Beanie](beanie.md)** - Async MongoDB ODM built on Pydantic and Motor
- **[MongoEngine](mongoengine.md)** - Full-featured ODM with Django support
- **[PyMongo](pymongo.md)** - Direct usage with the official MongoDB driver

## Quick Comparison

| Feature | Beanie | MongoEngine | PyMongo |
|---------|--------|-------------|---------|
| Async Support | ✅ Native | ❌ Sync only | ✅ Motor |
| Pydantic Integration | ✅ Native | ❌ Manual | ❌ Manual |
| Aggregation Support | ✅ Full | ✅ Full | ✅ Full |
| Type Hints | ✅ Full | ⚠️ Partial | ⚠️ Partial |

## Common Pattern

All integrations follow a similar pattern:

```python
from mongo_aggro import Pipeline, Match, Group, Sort

# Build your pipeline with type-safe stages
pipeline = Pipeline([
    Match(query={"status": "active"}),
    Group(id="$category", total={"$sum": "$amount"}),
    Sort(fields={"total": -1})
])

# Convert to list for any MongoDB driver
stages = pipeline.to_list()

# Or use with_sort() for pagination utilities
aggregation_input = pipeline.with_sort({"total": -1})
```

## Type Safety Benefits

Using Mongo Aggro with any ODM provides:

1. **IDE Autocomplete** - Full type hints for all stage parameters
2. **Validation** - Pydantic validates stage configurations at runtime
3. **Refactoring** - Safe refactoring with type checker support
4. **Documentation** - Self-documenting code with clear stage definitions

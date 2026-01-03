# Mongo Aggro

<p align="center">
  <strong>MongoDB Aggregation Pipeline Builder with Pydantic</strong>
</p>

<p align="center">
  <a href="https://github.com/hamedghenaat/mongo-aggro/actions"><img src="https://img.shields.io/github/actions/workflow/status/hamedghenaat/mongo-aggro/ci.yml?branch=main" alt="CI"></a>
  <a href="https://pypi.org/project/mongo-aggro/"><img src="https://img.shields.io/pypi/v/mongo-aggro" alt="PyPI"></a>
  <a href="https://pypi.org/project/mongo-aggro/"><img src="https://img.shields.io/pypi/pyversions/mongo-aggro" alt="Python Versions"></a>
  <a href="https://github.com/hamedghenaat/mongo-aggro/blob/main/LICENSE"><img src="https://img.shields.io/github/license/hamedghenaat/mongo-aggro" alt="License"></a>
</p>

---

**Mongo Aggro** is a Python library that provides a type-safe, Pydantic-based interface for building MongoDB aggregation pipelines. It offers strong type checking, IDE autocompletion, and a clean, Pythonic API.

## Features

- 🔒 **Type Safety** - Full Pydantic v2 support with proper type hints
- 🔗 **Seamless Integration** - Works directly with PyMongo's `aggregate()` method
- 📦 **25+ Stages** - All major MongoDB aggregation stages supported
- 📊 **18 Accumulators** - Sum, Avg, Min, Max, Push, and more
- 🔍 **Query Operators** - And, Or, In, Regex, and other operators
- 🎯 **IDE Support** - Full autocompletion and type checking in your IDE

## Quick Example

```python
from mongo_aggro import Pipeline, Match, Group, Sort, Limit, Sum, Avg

# Build a pipeline
pipeline = Pipeline([
    Match(query={"status": "active"}),
    Group(
        id="$category",
        accumulators={
            "total": {"$sum": "$amount"},
            "count": {"$sum": 1},
        }
    ),
    Sort(fields={"total": -1}),
    Limit(count=10),
])

# Use directly with PyMongo
results = collection.aggregate(pipeline)
```

## Installation

```bash
pip install mongo-aggro
```

Or with Poetry:

```bash
poetry add mongo-aggro
```

## Documentation

- [Getting Started](getting-started/installation.md) - Installation and setup
- [User Guide](guide/pipeline.md) - Learn how to use Mongo Aggro
- [Examples](examples/basic.md) - See practical examples
- [API Reference](api/pipeline.md) - Detailed API documentation

## License

MIT License - see [LICENSE](https://github.com/hamedghenaat/mongo-aggro/blob/main/LICENSE) for details.

# Contributing to Mongo Aggro

Thank you for your interest in contributing!

## Development Setup

### Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) for package management

### Setup

```bash
git clone https://github.com/hamedghenaat/mongo-aggro.git
cd mongo-aggro

# Install dependencies
uv sync --all-extras

# Install pre-commit hooks
uv run pre-commit install
```

## Development Workflow

```bash
# Run tests
make test

# Run linter
make lint

# Format code
make format

# Run all checks
make check
```

## Code Style

- **Ruff** for linting and formatting
- **79 character** line limit
- **Type hints** required on all functions
- **Google-style** docstrings

### Example

```python
def model_dump(self, **kwargs: Any) -> dict[str, Any]:
    """
    Convert stage to MongoDB dictionary.

    Args:
        **kwargs: Additional Pydantic arguments.

    Returns:
        MongoDB aggregation stage dictionary.

    Example:
        >>> Match(query={"status": "active"}).model_dump()
        {"$match": {"status": "active"}}
    """
    return {"$match": self.query}
```

## Adding Features

### New Stage

1. Add class in `mongo_aggro/stages.py`
2. Export in `mongo_aggro/__init__.py`
3. Add tests in `tests/test_stages.py`
4. Update documentation

### New Expression

1. Add class in `mongo_aggro/expressions.py`
2. Export in `mongo_aggro/__init__.py`
3. Add tests in `tests/test_expressions.py`

## Commit Style

Use conventional commits:
- `feat:` New features
- `fix:` Bug fixes
- `doc:` Documentation
- `ref:` Refactoring
- `ci:` CI/CD changes

```bash
git commit -m "feat: add new stage

- Add NewStage class
- Add tests
- Update documentation"
```

## Pull Request Process

1. Create feature branch
2. Make changes with tests
3. Run `make check`
4. Push and create PR
5. Address review comments

## Questions?

Open an issue for any questions.

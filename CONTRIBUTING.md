# Contributing to Mongo Aggro

Thank you for your interest in contributing to Mongo Aggro! This document provides guidelines and instructions for contributing.

## Development Setup

### Prerequisites

- Python 3.12 or higher
- [Poetry](https://python-poetry.org/) for dependency management
- [uv](https://github.com/astral-sh/uv) (optional, for faster package installation)

### Setting Up Your Development Environment

1. **Clone the repository**
   ```bash
   git clone https://github.com/hamedghenaat/mongo-aggro.git
   cd mongo-aggro
   ```

2. **Install dependencies**
   ```bash
   # Install all dependencies (dev + test)
   make install-all

   # Or using poetry directly
   poetry install --with dev,test
   ```

3. **Install pre-commit hooks**
   ```bash
   make pre-commit-install
   # Or
   poetry run pre-commit install
   ```

## Development Workflow

### Running Tests

```bash
# Run all tests
make test

# Run tests with coverage
make test-cov

# Run tests quickly (stop on first failure)
make test-fast
```

### Code Formatting and Linting

```bash
# Format code
make format

# Run linters
make lint

# Run all pre-commit hooks
make pre-commit
```

### Running All Checks

```bash
# Run format check + lint + test
make check
```

## Code Style

We follow these code style guidelines:

- **Black** for code formatting (line length: 88)
- **isort** for import sorting (black profile)
- **Ruff** for fast linting
- **mypy** for type checking

All code must pass these checks before being merged.

### Type Hints

All functions and methods should have type hints:

```python
def add_stage(self, stage: BaseStage) -> "Pipeline":
    """Add a stage to the pipeline."""
    self._stages.append(stage)
    return self
```

### Docstrings

Use Google-style docstrings:

```python
def model_dump(self, **kwargs: Any) -> dict[str, Any]:
    """
    Convert the stage to its MongoDB dictionary representation.

    Args:
        **kwargs: Additional arguments passed to Pydantic's model_dump.

    Returns:
        dict[str, Any]: MongoDB aggregation stage dictionary.

    Example:
        >>> Match(query={"status": "active"}).model_dump()
        {"$match": {"status": "active"}}
    """
    return {"$match": self.query}
```

## Adding New Features

### Adding a New Stage

1. Create the stage class in `mongo_aggro/stages.py`:

```python
class NewStage(BaseModel, BaseStage):
    """
    $newStage stage - description of what it does.

    Example:
        >>> NewStage(param="value").model_dump()
        {"$newStage": {"param": "value"}}
    """

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    param: str = Field(..., description="Parameter description")

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return {"$newStage": {"param": self.param}}
```

2. Export it in `mongo_aggro/__init__.py`

3. Add tests in `tests/test_stages.py`:

```python
def test_new_stage() -> None:
    """NewStage with basic usage."""
    stage = NewStage(param="value")
    assert stage.model_dump() == {"$newStage": {"param": "value"}}
```

### Adding a New Accumulator

1. Create the accumulator class in `mongo_aggro/accumulators.py`
2. Export it in `mongo_aggro/__init__.py`
3. Add tests in `tests/test_accumulators.py`

## Pull Request Process

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clean, well-documented code
   - Add tests for new functionality
   - Update documentation if needed

3. **Run all checks**
   ```bash
   make check
   ```

4. **Commit your changes**
   - Use clear, descriptive commit messages
   - Reference any related issues

5. **Push and create a Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **PR Review**
   - Ensure CI passes
   - Address any review comments
   - Keep the PR focused on a single feature/fix

## Reporting Issues

When reporting issues, please include:

- Python version
- mongo-aggro version
- Minimal code example to reproduce the issue
- Expected vs actual behavior
- Full error traceback (if applicable)

## Questions?

Feel free to open an issue for any questions about contributing.

Thank you for contributing! 🎉

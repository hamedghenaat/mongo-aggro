# Installation

## Requirements

- Python 3.12 or higher
- Pydantic 2.10+

## Install with pip

```bash
pip install mongo-aggro
```

## Install with Poetry

```bash
poetry add mongo-aggro
```

## Install with uv

```bash
uv add mongo-aggro
```

## Development Installation

If you want to contribute or modify the library:

```bash
# Clone the repository
git clone https://github.com/hamedghenaat/mongo-aggro.git
cd mongo-aggro

# Install with dev dependencies
poetry install --with dev,test

# Install pre-commit hooks
poetry run pre-commit install
```

## Verify Installation

```python
import mongo_aggro
print(mongo_aggro.__version__)
```

## Optional Dependencies

Mongo Aggro has no required dependencies other than Pydantic. However, you'll likely want to install PyMongo to use with MongoDB:

```bash
pip install pymongo
```

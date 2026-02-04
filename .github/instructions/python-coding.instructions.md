# Python Coding Guidance

1. Simplicity always wins—write readable, clean Python that adheres to PEP 8, as though Black and isort already ran. Wrap or break any docstring, comment, or f-string exceeding 79 characters into multiple lines.
2. Determine the highest Python version used in this repo, prefer that (or specify it if multiple versions exist), and leverage its modern type hints extensively. Favor typing tools (TypeVar, generics, Literal, etc.) or Pydantic models when available; avoid magic literals by defining named constants.
3. Prefer functional programming over OOP whenever feasible, defaulting to enums (IntEnum, StrEnum, etc.) over mappings and selecting the enum variant that matches the data. Keep every line ≤79 characters.
4. Detect and use the repo’s package manager—prefer `uv`, then `poetry`, then `pipenv`, then `pip`—and always rely on existing Makefile targets instead of inventing new commands when a Makefile exists.
5. Never use unparameterized collection types; always annotate what items they hold (e.g., `list[str]`, `dict[str, int | str]`). If the item types vary or are unknown, use `Any` (after importing it from `typing`) so the collection remains precise (e.g., `dict[str, Any]`).

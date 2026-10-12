"""Input parsing and validation helpers."""
import math
from .exceptions import InvalidInputError
from .operations import OperationFactory

COMMANDS = {"help", "history", "exit", "quit", "clear", "undo", "redo", "save", "load"}


def parse_number(value: str) -> float:
    """Convert text to a finite float or raise a friendly input error."""
    try:
        number = float(value.strip())
    except (ValueError, AttributeError) as exc:
        raise InvalidInputError(f"Invalid number: {value!r}") from exc
    if not math.isfinite(number):
        raise InvalidInputError("Please enter a finite number.")
    return number


def validate_operation(value: str) -> str:
    """Return a normalized supported operation or raise an input error."""
    if not isinstance(value, str) or not value.strip():
        raise InvalidInputError("Please enter an operation.")
    operation = value.strip().lower()
    try:
        OperationFactory.create(operation)
    except Exception as exc:
        # Convert unsupported-operation errors for users; propagate unrelated factory failures.
        from .exceptions import InvalidOperationError
        if isinstance(exc, InvalidOperationError):
            raise InvalidInputError(str(exc)) from exc
        raise
    return operation


def validate_command(value: str) -> str | None:
    """Return a recognized command, or None when input is not a command."""
    command = value.strip().lower()
    return command if command in COMMANDS else None

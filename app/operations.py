"""Arithmetic strategies and their factory."""
from abc import ABC, abstractmethod
import math
from .exceptions import DivisionByZeroError, InvalidOperationError


class Operation(ABC):
    """Interface implemented by every arithmetic strategy."""

    name = ""
    symbol = ""

    @abstractmethod
    def calculate(self, a: float, b: float) -> float:
        """Calculate a result from two numeric operands."""


class Add(Operation):
    name, symbol = "add", "+"

    def calculate(self, a: float, b: float) -> float:
        return a + b


class Subtract(Operation):
    name, symbol = "subtract", "-"

    def calculate(self, a: float, b: float) -> float:
        return a - b


class Multiply(Operation):
    name, symbol = "multiply", "*"

    def calculate(self, a: float, b: float) -> float:
        return a * b


class Divide(Operation):
    name, symbol = "divide", "/"

    def calculate(self, a: float, b: float) -> float:
        if b == 0:  # LBYL: check before performing division.
            raise DivisionByZeroError("Cannot divide by zero.")
        return a / b


class Power(Operation):
    name, symbol = "power", "**"

    def calculate(self, a: float, b: float) -> float:
        try:  # EAFP: attempt the operation and handle its exceptional cases.
            result = a ** b
        except (OverflowError, ZeroDivisionError, ValueError) as exc:
            raise InvalidOperationError(f"Power operation is undefined: {exc}") from exc
        if isinstance(result, complex):
            raise InvalidOperationError("Complex results are not supported.")
        if not math.isfinite(float(result)):
            raise InvalidOperationError("The result is not finite.")
        return float(result)


class Root(Operation):
    name, symbol = "root", "root"

    def calculate(self, a: float, b: float) -> float:
        """Return the b-th root of a; operand b is the root degree."""
        if b == 0:
            raise DivisionByZeroError("The root degree cannot be zero.")
        # Python's fractional power of a negative number is complex; handle real odd roots directly.
        if a < 0 and float(b).is_integer() and int(b) % 2 == 1:
            return -((-a) ** (1 / b))
        if a < 0:
            raise InvalidOperationError("Negative numbers require an odd integer root degree.")
        try:
            result = a ** (1 / b)
        except (OverflowError, ZeroDivisionError, ValueError) as exc:
            raise InvalidOperationError(f"Root operation is undefined: {exc}") from exc
        if isinstance(result, complex) or not math.isfinite(float(result)):
            raise InvalidOperationError("The result is not a finite real number.")
        return float(result)


class OperationFactory:
    """Create an operation strategy from its name or symbol."""
    _operations = {
        "+": Add, "add": Add,
        "-": Subtract, "subtract": Subtract,
        "*": Multiply, "multiply": Multiply,
        "/": Divide, "divide": Divide,
        "**": Power, "^": Power, "power": Power,
        "root": Root,
    }

    @classmethod
    def create(cls, operation: str) -> Operation:
        """Return the matching operation, case-insensitively."""
        try:
            operation_class = cls._operations[operation.strip().lower()]
        except (KeyError, AttributeError) as exc:
            raise InvalidOperationError(f"Unsupported operation: {operation!r}") from exc
        return operation_class()

    @classmethod
    def supported_operations(cls) -> tuple[str, ...]:
        """Return unique user-facing operation names."""
        return ("+", "-", "*", "/", "power", "root")

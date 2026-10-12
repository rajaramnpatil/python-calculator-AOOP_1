"""Application-specific exceptions."""


class CalculatorError(Exception):
    """Base exception for expected calculator errors."""


class InvalidOperationError(CalculatorError):
    """Raised when an operation name is not supported."""


class InvalidInputError(CalculatorError):
    """Raised when user input cannot be interpreted."""


class DivisionByZeroError(CalculatorError):
    """Raised when division or a root operation is undefined due to zero."""


class ConfigurationError(CalculatorError):
    """Raised when a configuration setting is invalid."""


class HistoryError(CalculatorError):
    """Raised when calculation history cannot be read or written."""

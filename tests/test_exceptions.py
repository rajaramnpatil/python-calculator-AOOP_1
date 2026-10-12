from app.exceptions import CalculatorError, InvalidOperationError, InvalidInputError, DivisionByZeroError, ConfigurationError, HistoryError

def test_exception_inheritance():
    assert issubclass(InvalidOperationError, CalculatorError)
    assert issubclass(InvalidInputError, CalculatorError)
    assert issubclass(DivisionByZeroError, CalculatorError)
    assert issubclass(ConfigurationError, CalculatorError)
    assert issubclass(HistoryError, CalculatorError)

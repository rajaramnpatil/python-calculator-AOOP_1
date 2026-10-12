import pytest
from app.exceptions import DivisionByZeroError, InvalidOperationError
from app.operations import Add, Subtract, Multiply, Divide, Power, Root, OperationFactory, Operation

@pytest.mark.parametrize("cls,a,b,expected", [
    (Add, 2, 3, 5), (Subtract, 5, 3, 2), (Multiply, 3, 4, 12),
    (Divide, 8, 2, 4), (Power, 2, 3, 8), (Root, 27, 3, 3), (Root, -8, 3, -2),
])
def test_operations(cls, a, b, expected):
    assert cls().calculate(a, b) == pytest.approx(expected)

def test_division_by_zero():
    with pytest.raises(DivisionByZeroError): Divide().calculate(1, 0)

def test_root_zero_degree():
    with pytest.raises(DivisionByZeroError): Root().calculate(8, 0)

def test_invalid_root():
    with pytest.raises(InvalidOperationError): Root().calculate(-4, 2)

def test_invalid_power_result():
    with pytest.raises(InvalidOperationError): Power().calculate(-1, 0.5)

def test_factory_aliases_and_bad_input():
    assert isinstance(OperationFactory.create(" + "), Add)
    assert isinstance(OperationFactory.create("POWER"), Power)
    assert OperationFactory.supported_operations() == ("+", "-", "*", "/", "power", "root")
    with pytest.raises(InvalidOperationError): OperationFactory.create("modulo")
    with pytest.raises(InvalidOperationError): OperationFactory.create(None)

def test_operation_is_abstract():
    with pytest.raises(TypeError): Operation()

@pytest.mark.parametrize("error", [OverflowError, ZeroDivisionError, ValueError])
def test_power_wraps_arithmetic_errors(error):
    # A controlled numeric protocol object covers each exception without relying on huge values.
    class RaisingPower:
        def __pow__(self, _exponent):
            raise error("failed power")

    with pytest.raises(InvalidOperationError, match="Power operation is undefined"):
        Power().calculate(RaisingPower(), 2)

def test_power_rejects_infinite_result():
    class InfinitePower:
        def __pow__(self, _exponent):
            return float("inf")

    with pytest.raises(InvalidOperationError, match="result is not finite"):
        Power().calculate(InfinitePower(), 2)

@pytest.mark.parametrize("result", [complex(1, 1), float("inf")])
def test_root_rejects_invalid_result(result):
    # Simulate unsupported power results to cover both complex and non-finite rejection.
    class UnusualRoot:
        def __lt__(self, _other):
            return False
        def __pow__(self, _exponent):
            return result

    with pytest.raises(InvalidOperationError, match="not a finite real number"):
        Root().calculate(UnusualRoot(), 2)

def test_root_wraps_arithmetic_errors():
    class RaisingRoot:
        def __lt__(self, _other):
            return False
        def __pow__(self, _exponent):
            raise ValueError("failed root")

    with pytest.raises(InvalidOperationError, match="Root operation is undefined"):
        Root().calculate(RaisingRoot(), 2)

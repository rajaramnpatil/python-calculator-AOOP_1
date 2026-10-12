import pytest
from unittest.mock import patch
from app.exceptions import InvalidInputError
from app.input_validators import parse_number, validate_operation, validate_command

@pytest.mark.parametrize("value,expected", [("2", 2.0), (" -3.5 ", -3.5), ("1e2", 100.0)])
def test_parse_number(value, expected): assert parse_number(value) == expected

@pytest.mark.parametrize("value", ["abc", "nan", "inf", "", None])
def test_parse_number_invalid(value):
    with pytest.raises(InvalidInputError): parse_number(value)

@pytest.mark.parametrize("value,expected", [(" + ", "+"), ("POWER", "power"), ("root", "root")])
def test_validate_operation(value, expected): assert validate_operation(value) == expected

@pytest.mark.parametrize("value", ["", "bad", None])
def test_validate_operation_invalid(value):
    with pytest.raises(InvalidInputError): validate_operation(value)

@pytest.mark.parametrize("value,expected", [("help", "help"), (" EXIT ", "exit"), ("xyz", None), ("", None)])
def test_validate_command(value, expected): assert validate_command(value) == expected

def test_validate_operation_reraises_unexpected_factory_error():
    # Non-operation errors must propagate instead of being rewritten as bad user input.
    with patch("app.input_validators.OperationFactory.create", side_effect=RuntimeError("factory failure")):
        with pytest.raises(RuntimeError, match="factory failure"):
            validate_operation("+")

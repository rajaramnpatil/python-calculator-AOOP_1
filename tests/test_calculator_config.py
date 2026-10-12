import pytest
from app.calculator_config import load_config
from app.exceptions import ConfigurationError

def test_defaults(monkeypatch):
    for key in ("CALCULATOR_HISTORY_FILE", "CALCULATOR_AUTO_SAVE", "CALCULATOR_PRECISION", "CALCULATOR_LOG_FILE"):
        monkeypatch.delenv(key, raising=False)
    config = load_config(None)
    assert str(config.history_file) == "calculator_history.csv"
    assert config.auto_save is True and config.precision == 6
    assert str(config.log_file) == "calculator.log"

def test_valid_environment(monkeypatch, tmp_path):
    monkeypatch.setenv("CALCULATOR_HISTORY_FILE", str(tmp_path / "x.csv"))
    monkeypatch.setenv("CALCULATOR_AUTO_SAVE", "off")
    monkeypatch.setenv("CALCULATOR_PRECISION", "3")
    config = load_config(None)
    assert config.auto_save is False and config.precision == 3

def test_empty_path(monkeypatch):
    monkeypatch.setenv("CALCULATOR_HISTORY_FILE", " ")
    with pytest.raises(ConfigurationError): load_config(None)

@pytest.mark.parametrize("value", ["maybe", "truthy"])
def test_bad_boolean(monkeypatch, value):
    monkeypatch.setenv("CALCULATOR_AUTO_SAVE", value)
    with pytest.raises(ConfigurationError): load_config(None)

@pytest.mark.parametrize("value", ["x", "-1", "16"])
def test_bad_precision(monkeypatch, value):
    monkeypatch.setenv("CALCULATOR_PRECISION", value)
    with pytest.raises(ConfigurationError): load_config(None)


def test_empty_log_path(monkeypatch):
    monkeypatch.setenv("CALCULATOR_LOG_FILE", " ")
    with pytest.raises(ConfigurationError):
        load_config(None)

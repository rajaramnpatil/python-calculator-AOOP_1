import logging
import runpy
import sys
import warnings
from unittest.mock import patch

from app.calculation import Calculator
from app.calculator_config import CalculatorConfig
from app.calculator_repl import main, run_repl
from app.exceptions import ConfigurationError, HistoryError
from app.history import CalculationHistory

def test_repl_commands(tmp_path):
    calc = Calculator(CalculationHistory(tmp_path / "history.csv"), auto_save=False)
    inputs = iter(["help", "history", "+ 2 3", "bad 1 2", "+ x 2", "undo", "redo", "save", "clear", "history", "load", "exit"])
    outputs = []
    run_repl(calc, input_fn=lambda _="": next(inputs), output_fn=outputs.append)
    joined = "\n".join(outputs)
    assert "Commands:" in joined
    assert "Result: 5" in joined
    assert "Error:" in joined
    assert "Goodbye!" in joined

def test_repl_invalid_syntax_and_eof():
    calc = Calculator(auto_save=False)
    inputs = iter(["", "+ 2", "save a b"])
    outputs = []
    def read(_=""):
        try: return next(inputs)
        except StopIteration: raise EOFError
    run_repl(calc, input_fn=read, output_fn=outputs.append)
    assert any("two numbers" in item for item in outputs)
    assert any("Usage:" in item for item in outputs)
    assert outputs[-1] == "Goodbye!"

def test_repl_quit_alias():
    outputs = []
    run_repl(Calculator(auto_save=False), input_fn=lambda _="": "quit", output_fn=outputs.append)
    assert outputs[-1] == "Goodbye!"

def test_repl_logs_full_operation_command():
    logger = logging.getLogger("calculator")
    inputs = iter(["+ 2 3", "exit"])
    with patch.object(logger, "info") as log_info:
        run_repl(Calculator(auto_save=False), input_fn=lambda _="": next(inputs), output_fn=lambda _: None)
    assert any(call.args == ("Received command: %s", "+ 2 3") for call in log_info.call_args_list)

def test_repl_save_and_load_history_errors():
    # Stub persistence failures so the REPL's user-facing error path is deterministic.
    class BrokenHistoryCalculator:
        def save(self, _path=None):
            raise HistoryError("save failed")
        def load(self, _path=None):
            raise HistoryError("load failed")

    inputs = iter(["save", "load", "exit"])
    outputs = []
    run_repl(BrokenHistoryCalculator(), input_fn=lambda _="": next(inputs), output_fn=outputs.append)
    assert "Error: save failed" in outputs
    assert "Error: load failed" in outputs

def test_main_success_uses_configured_history_when_no_override(monkeypatch, tmp_path):
    import app.calculator_repl as repl

    config = CalculatorConfig(tmp_path / "configured.csv", False, 4, tmp_path / "calculator.log")
    history = CalculationHistory(config.history_file)
    calls = []
    # Replace startup dependencies to verify routing without opening an interactive prompt.
    monkeypatch.setattr(sys, "argv", ["calculator_repl"])
    monkeypatch.setattr(repl, "load_config", lambda: config)
    monkeypatch.setattr(repl, "setup_logging", lambda _path: logging.getLogger("calculator"))
    monkeypatch.setattr(repl, "CalculationHistory", lambda path: (calls.append(path), history)[1])
    monkeypatch.setattr(repl, "run_repl", lambda calculator, precision: calls.append((calculator, precision)))
    main()
    assert calls[0] == str(config.history_file)
    assert calls[1][1] == 4

def test_main_history_override(monkeypatch, tmp_path):
    import app.calculator_repl as repl

    config = CalculatorConfig(tmp_path / "configured.csv", False, 6, tmp_path / "calculator.log")
    override = tmp_path / "override.csv"
    calls = []
    # The CLI argument should take precedence over the path from application config.
    monkeypatch.setattr(sys, "argv", ["calculator_repl", "--history-file", str(override)])
    monkeypatch.setattr(repl, "load_config", lambda: config)
    monkeypatch.setattr(repl, "setup_logging", lambda _path: logging.getLogger("calculator"))
    monkeypatch.setattr(repl, "CalculationHistory", lambda path: (calls.append(path), CalculationHistory(path))[1])
    monkeypatch.setattr(repl, "run_repl", lambda *_args, **_kwargs: None)
    main()
    assert calls == [str(override)]

def test_main_configuration_error(monkeypatch):
    import app.calculator_repl as repl

    printed = []
    # Isolate the exception handler's console message from logging's traceback output.
    monkeypatch.setattr(sys, "argv", ["calculator_repl"])
    monkeypatch.setattr(repl, "load_config", lambda: (_ for _ in ()).throw(ConfigurationError("bad config")))
    monkeypatch.setattr("builtins.print", printed.append)
    monkeypatch.setattr(logging.getLogger("calculator"), "exception", lambda *_args, **_kwargs: None)
    main()
    assert printed == ["Configuration/startup error: bad config"]

def test_module_entry_point_runs_main(monkeypatch, tmp_path):
    monkeypatch.setenv("CALCULATOR_HISTORY_FILE", str(tmp_path / "history.csv"))
    monkeypatch.setenv("CALCULATOR_AUTO_SAVE", "false")
    monkeypatch.setenv("CALCULATOR_PRECISION", "2")
    monkeypatch.setenv("CALCULATOR_LOG_FILE", str(tmp_path / "calculator.log"))
    monkeypatch.setattr(sys, "argv", ["calculator_repl"])
    logger = logging.getLogger("calculator")
    existing_handlers = set(logger.handlers)
    try:
        # run_module warns because this module was imported above; input immediately ends the REPL.
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", RuntimeWarning)
            with patch("builtins.input", side_effect=EOFError):
                runpy.run_module("app.calculator_repl", run_name="__main__", alter_sys=True)
    finally:
        # Do not leave a file handler pointing at this test's temporary directory.
        for handler in set(logger.handlers) - existing_handlers:
            logger.removeHandler(handler)
            handler.close()

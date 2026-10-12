from app.calculation import Calculator
from app.calculator_repl import run_repl
from app.history import CalculationHistory
import logging
from unittest.mock import patch

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

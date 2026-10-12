"""Interactive read-eval-print loop for the calculator."""
import argparse
import logging
from .calculation import Calculator
from .calculator_config import load_config
from .exceptions import CalculatorError, HistoryError
from .history import CalculationHistory
from .input_validators import parse_number, validate_command, validate_operation
from .logger_config import setup_logging

HELP_TEXT = """Commands: help, history, undo, redo, clear, save [file], load [file], exit
Operations: +, -, *, /, power (or **), root (second number is root degree)
Enter an operation followed by two numbers, for example: + 2 3
"""


def run_repl(calculator: Calculator, precision: int = 6, input_fn=input, output_fn=print) -> None:
    """Run the REPL; input/output functions can be replaced in tests."""
    logger = logging.getLogger("calculator")
    logger.info("Calculator REPL started")
    output_fn("Advanced Calculator. Type 'help' for commands.")
    while True:
        try:
            line = input_fn("calc> ").strip()
        except (EOFError, KeyboardInterrupt):
            logger.info("REPL stopped by EOF or keyboard interrupt")
            output_fn("Goodbye!")
            break
        if not line:
            continue
        parts = line.split()
        command = validate_command(parts[0])
        logger.info("Received command: %s", line)
        if command in {"exit", "quit"}:
            logger.info("Calculator REPL exited by user")
            output_fn("Goodbye!")
            break
        if command == "help":
            output_fn(HELP_TEXT)
            continue
        if command == "history":
            frame = calculator.history.dataframe
            output_fn("No calculation history." if frame.empty else frame.to_string(index=False))
            continue
        if command == "clear":
            calculator.clear()
            output_fn("History cleared.")
            continue
        if command == "undo":
            output_fn(f"Undo complete. Last result: {calculator.undo()}")
            continue
        if command == "redo":
            output_fn(f"Redo complete. Last result: {calculator.redo()}")
            continue
        if command in {"save", "load"}:
            path = parts[1] if len(parts) > 1 else None
            if len(parts) > 2:
                output_fn(f"Usage: {command} [file]")
                continue
            try:
                if command == "save":
                    output_fn(f"History saved to {calculator.save(path)}")
                else:
                    output_fn(f"Loaded {calculator.load(path)} history record(s).")
            except HistoryError as exc:
                logger.exception("History %s command failed", command)
                output_fn(f"Error: {exc}")
            continue
        try:
            if len(parts) != 3:
                output_fn("Enter an operation and two numbers, e.g. + 2 3. Type 'help' for help.")
                continue
            operation = validate_operation(parts[0])
            a, b = parse_number(parts[1]), parse_number(parts[2])
            result = calculator.calculate(operation, a, b)
            output_fn(f"Result: {result:.{precision}f}".rstrip("0").rstrip("."))
        except CalculatorError as exc:
            logger.warning("Calculation/input error: %s", exc)
            output_fn(f"Error: {exc}")


def main() -> None:
    """Load configuration and start the calculator REPL."""
    parser = argparse.ArgumentParser(description="Advanced modular calculator")
    parser.add_argument("--history-file", help="Override the history CSV path")
    args = parser.parse_args()
    try:
        config = load_config()
        logger = setup_logging(config.log_file)
        logger.info("Starting calculator application")
        history_path = args.history_file or str(config.history_file)
        history = CalculationHistory(history_path)
        history.load()
        calculator = Calculator(history=history, auto_save=config.auto_save)
        run_repl(calculator, precision=config.precision)
    except CalculatorError as exc:
        logging.getLogger("calculator").exception("Configuration/startup failed")
        print(f"Configuration/startup error: {exc}")


if __name__ == "__main__":
    main()

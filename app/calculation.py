"""Calculation service, observers, and calculator facade."""
from datetime import datetime, timezone
from typing import Any, Protocol
import logging
import math
from .calculator_memento import CalculatorMemento, MementoManager
from .exceptions import InvalidInputError
from .history import CalculationHistory
from .operations import OperationFactory

logger = logging.getLogger("calculator")


class CalculationObserver(Protocol):
    """Protocol for objects interested in successful calculations."""
    def update(self, record: dict[str, Any]) -> None: ...


class HistoryObserver:
    """Observer that records calculations and optionally auto-saves them."""
    def __init__(self, history: CalculationHistory, auto_save: bool = True) -> None:
        self.history = history
        self.auto_save = auto_save

    def update(self, record: dict[str, Any]) -> None:
        self.history.add(record)
        if self.auto_save:
            self.history.save()


class LoggingObserver:
    """Log successful calculations and retain messages for inspection/tests."""
    def __init__(self) -> None:
        self.messages: list[str] = []
        self.logger = logging.getLogger("calculator")

    def update(self, record: dict[str, Any]) -> None:
        message = (
            f"{record['operand_a']} {record['operation']} "
            f"{record['operand_b']} = {record['result']}"
        )
        self.messages.append(message)
        self.logger.info("Calculation: %s", message)


class CalculationService:
    """Execute strategies and notify registered observers."""
    def __init__(self) -> None:
        self._observers: list[CalculationObserver] = []

    def attach(self, observer: CalculationObserver) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: CalculationObserver) -> None:
        if observer in self._observers:
            self._observers.remove(observer)

    def calculate(self, operation: str, a: float, b: float) -> tuple[float, dict[str, Any]]:
        if not math.isfinite(a) or not math.isfinite(b):
            raise InvalidInputError("Operands must be finite numbers.")
        logger.info("Pattern: Factory | Object: OperationFactory.create")
        strategy = OperationFactory.create(operation)
        logger.info("Pattern: Strategy | Object: %s.calculate", type(strategy).__name__)
        result = strategy.calculate(a, b)
        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "operation": strategy.symbol,
            "operand_a": a,
            "operand_b": b,
            "result": result,
        }
        # A stable snapshot lets observers safely attach or detach during notification.
        for observer in tuple(self._observers):
            logger.info("Pattern: Observer | Object: %s.update", type(observer).__name__)
            observer.update(record)
        return result, record


class Calculator:
    """Facade coordinating arithmetic, observers, history, and mementos."""
    def __init__(self, history: CalculationHistory | None = None, auto_save: bool = True) -> None:
        self.history = history or CalculationHistory()
        self.service = CalculationService()
        self.history_observer = HistoryObserver(self.history, auto_save=auto_save)
        self.logging_observer = LoggingObserver()
        self.service.attach(self.history_observer)
        self.service.attach(self.logging_observer)
        self.mementos = MementoManager()
        self.last_result: float | None = None

    def _snapshot(self) -> CalculatorMemento:
        return CalculatorMemento(self.last_result, tuple(self.history.dataframe.to_dict("records")))

    def calculate(self, operation: str, a: float, b: float) -> float:
        """Perform a calculation, preserving the prior state for undo."""
        logger.info("Pattern: Facade | Object: Calculator.calculate")
        previous_state = self._snapshot()
        result, _ = self.service.calculate(operation, a, b)
        self.mementos.save(previous_state)
        self.last_result = result
        return result

    def undo(self) -> float | None:
        """Undo the most recent successful calculation."""
        logger.info("Pattern: Facade | Object: Calculator.undo")
        state = self.mementos.undo(self._snapshot())
        self._restore(state)
        return self.last_result

    def redo(self) -> float | None:
        """Redo the most recently undone calculation."""
        logger.info("Pattern: Facade | Object: Calculator.redo")
        state = self.mementos.redo(self._snapshot())
        self._restore(state)
        return self.last_result

    def _restore(self, state: CalculatorMemento) -> None:
        self.last_result = state.last_result
        self.history.replace_records(state.history_records)
        if self.history_observer.auto_save:
            self.history.save()

    def save(self, file_path: str | None = None) -> str:
        return str(self.history.save(file_path))

    def load(self, file_path: str | None = None) -> int:
        count = self.history.load(file_path)
        self.last_result = None if self.history.dataframe.empty else float(self.history.dataframe.iloc[-1]["result"])
        return count

    def clear(self) -> None:
        self.mementos.save(self._snapshot())
        self.history.clear()
        self.last_result = None
        if self.history_observer.auto_save:
            self.history.save()

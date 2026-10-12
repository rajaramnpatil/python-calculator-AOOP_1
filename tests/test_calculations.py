import pytest
import logging
from unittest.mock import patch
from app.calculation import Calculator, CalculationService, HistoryObserver, LoggingObserver
from app.exceptions import InvalidInputError
from app.history import CalculationHistory

class Observer:
    def __init__(self): self.records = []
    def update(self, record): self.records.append(record)

def test_service_observers_and_detach():
    service = CalculationService(); observer = Observer()
    service.attach(observer); service.attach(observer)
    result, record = service.calculate("+", 2, 3)
    assert result == 5 and len(observer.records) == 1
    assert record["operation"] == "+"
    service.detach(observer); service.detach(observer)
    service.calculate("+", 1, 1)
    assert len(observer.records) == 1

def test_service_rejects_nonfinite():
    with pytest.raises(InvalidInputError): CalculationService().calculate("+", float("inf"), 1)

def test_calculator_logs_patterns_and_observer_objects():
    logger = logging.getLogger("calculator")
    with patch.object(logger, "info") as log_info:
        Calculator(auto_save=False).calculate("+", 2, 3)
    messages = [call.args[0] % call.args[1:] if len(call.args) > 1 else call.args[0]
                for call in log_info.call_args_list]
    assert "Pattern: Facade | Object: Calculator.calculate" in messages
    assert "Pattern: Factory | Object: OperationFactory.create" in messages
    assert "Pattern: Strategy | Object: Add.calculate" in messages
    assert "Pattern: Observer | Object: HistoryObserver.update" in messages
    assert "Pattern: Observer | Object: LoggingObserver.update" in messages
    assert "Pattern: Memento | Object: MementoManager.save" in messages

def test_observers():
    history = CalculationHistory()
    history_observer = HistoryObserver(history, auto_save=False)
    logger = LoggingObserver()
    record = {"timestamp":"t", "operation":"+", "operand_a":2, "operand_b":3, "result":5}
    history_observer.update(record); logger.update(record)
    assert len(history.dataframe) == 1
    assert logger.messages == ["2 + 3 = 5"]

def test_calculator_undo_redo(tmp_path):
    calc = Calculator(CalculationHistory(tmp_path / "history.csv"), auto_save=False)
    assert calc.calculate("+", 2, 3) == 5
    assert len(calc.history.dataframe) == 1
    assert calc.undo() is None
    assert calc.history.dataframe.empty
    assert calc.redo() == 5
    assert len(calc.history.dataframe) == 1

def test_calculator_clear_save_load(tmp_path):
    path = tmp_path / "history.csv"
    calc = Calculator(CalculationHistory(path), auto_save=False)
    calc.calculate("*", 3, 4)
    assert calc.save() == str(path)
    other = Calculator(CalculationHistory(path), auto_save=False)
    assert other.load() == 1
    assert other.last_result == 12
    other.clear()
    assert other.history.dataframe.empty

def test_auto_save_observer(tmp_path):
    calc = Calculator(CalculationHistory(tmp_path / "history.csv"), auto_save=True)
    calc.calculate("+", 1, 2)
    assert (tmp_path / "history.csv").exists()

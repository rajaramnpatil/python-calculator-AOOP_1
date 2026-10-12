import pandas as pd
import pytest
from app.exceptions import HistoryError
from app.history import CalculationHistory, COLUMNS

RECORD = {"timestamp":"2026-01-01T00:00:00+00:00", "operation":"+", "operand_a":2, "operand_b":3, "result":5}

def test_add_copy_clear(tmp_path):
    history = CalculationHistory(tmp_path / "history.csv")
    history.add(RECORD)
    assert len(history.dataframe) == 1
    copy = history.dataframe
    copy.drop(index=0, inplace=True)
    assert len(history.dataframe) == 1
    history.clear()
    assert history.dataframe.empty

def test_missing_fields():
    with pytest.raises(HistoryError): CalculationHistory().add({"result": 2})

def test_save_and_load(tmp_path):
    path = tmp_path / "nested" / "history.csv"
    history = CalculationHistory(path)
    history.add(RECORD)
    assert history.save() == path
    loaded = CalculationHistory(path)
    assert loaded.load() == 1
    assert loaded.dataframe.iloc[0]["result"] == 5

def test_missing_file_clears_history(tmp_path):
    history = CalculationHistory(tmp_path / "missing.csv")
    history.add(RECORD)
    assert history.load() == 0
    assert history.dataframe.empty

def test_bad_columns(tmp_path):
    path = tmp_path / "bad.csv"
    pd.DataFrame([{"wrong": 1}]).to_csv(path, index=False)
    with pytest.raises(HistoryError): CalculationHistory(path).load()

def test_invalid_csv(tmp_path):
    path = tmp_path / "bad.csv"
    path.write_text('"unfinished')
    with pytest.raises(HistoryError): CalculationHistory(path).load()

def test_replace_records():
    history = CalculationHistory()
    history.replace_records([RECORD])
    assert list(history.dataframe.columns) == COLUMNS
    assert len(history.dataframe) == 1

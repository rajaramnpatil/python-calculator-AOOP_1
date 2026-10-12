"""pandas-backed calculation history with CSV persistence."""
from pathlib import Path
from typing import Any
import pandas as pd
from .exceptions import HistoryError

COLUMNS = ["timestamp", "operation", "operand_a", "operand_b", "result"]


class CalculationHistory:
    """Store calculation records in a DataFrame and persist them as CSV."""
    def __init__(self, file_path: str | Path = "calculator_history.csv") -> None:
        self.file_path = Path(file_path)
        self._frame = pd.DataFrame(columns=COLUMNS)

    @property
    def dataframe(self) -> pd.DataFrame:
        """Return a copy so callers cannot mutate internal history directly."""
        return self._frame.copy(deep=True)

    def add(self, record: dict[str, Any]) -> None:
        """Append a validated calculation record."""
        missing = set(COLUMNS) - set(record)
        if missing:
            raise HistoryError(f"Missing history fields: {', '.join(sorted(missing))}")
        row = {column: record[column] for column in COLUMNS}
        self._frame = pd.concat([self._frame, pd.DataFrame([row])], ignore_index=True)

    def replace_records(self, records: tuple[dict[str, Any], ...] | list[dict[str, Any]]) -> None:
        """Replace all history rows with snapshot records."""
        self._frame = pd.DataFrame(list(records), columns=COLUMNS)

    def clear(self) -> None:
        """Remove all rows from memory."""
        self._frame = pd.DataFrame(columns=COLUMNS)

    def save(self, file_path: str | Path | None = None) -> Path:
        """Save the current history to CSV."""
        target = Path(file_path) if file_path is not None else self.file_path
        try:
            target.parent.mkdir(parents=True, exist_ok=True)
            self._frame.to_csv(target, index=False)
        except (OSError, ValueError) as exc:
            raise HistoryError(f"Could not save history: {exc}") from exc
        return target

    def load(self, file_path: str | Path | None = None) -> int:
        """Load history from CSV, returning the number of records loaded."""
        target = Path(file_path) if file_path is not None else self.file_path
        if not target.exists():  # LBYL: a missing history file is not an error.
            self.clear()
            return 0
        try:  # EAFP: handle file and CSV parsing failures.
            frame = pd.read_csv(target)
            missing = set(COLUMNS) - set(frame.columns)
            if missing:
                raise HistoryError(f"History file is missing columns: {', '.join(sorted(missing))}")
            self._frame = frame[COLUMNS].copy()
        except HistoryError:
            raise
        except (OSError, ValueError, pd.errors.ParserError, pd.errors.EmptyDataError) as exc:
            raise HistoryError(f"Could not load history: {exc}") from exc
        return len(self._frame)

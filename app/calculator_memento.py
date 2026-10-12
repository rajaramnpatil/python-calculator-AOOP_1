"""Memento objects and undo/redo state management."""
from dataclasses import dataclass
import logging
from typing import Any

logger = logging.getLogger("calculator")


@dataclass(frozen=True)
class CalculatorMemento:
    """Immutable snapshot of the calculator's relevant state."""
    last_result: float | None
    history_records: tuple[dict[str, Any], ...]


class MementoManager:
    """Manage snapshots for undo and redo operations."""
    def __init__(self) -> None:
        self._undo_stack: list[CalculatorMemento] = []
        self._redo_stack: list[CalculatorMemento] = []

    def save(self, state: CalculatorMemento) -> None:
        """Save a state before a new change and clear redo history."""
        logger.info("Pattern: Memento | Object: MementoManager.save")
        self._undo_stack.append(state)
        # A new change starts a new timeline, so previously undone states are no longer valid.
        self._redo_stack.clear()

    def undo(self, current: CalculatorMemento) -> CalculatorMemento:
        """Restore the previous state or raise when unavailable."""
        logger.info("Pattern: Memento | Object: MementoManager.undo")
        if not self._undo_stack:
            return current
        self._redo_stack.append(current)
        return self._undo_stack.pop()

    def redo(self, current: CalculatorMemento) -> CalculatorMemento:
        """Restore the next state or return current when unavailable."""
        logger.info("Pattern: Memento | Object: MementoManager.redo")
        if not self._redo_stack:
            return current
        self._undo_stack.append(current)
        return self._redo_stack.pop()

    @property
    def can_undo(self) -> bool:
        return bool(self._undo_stack)

    @property
    def can_redo(self) -> bool:
        return bool(self._redo_stack)

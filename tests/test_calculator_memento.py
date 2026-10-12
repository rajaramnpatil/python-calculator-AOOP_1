from app.calculator_memento import CalculatorMemento, MementoManager

def state(result): return CalculatorMemento(result, tuple())

def test_undo_redo_and_flags():
    manager = MementoManager()
    original, changed = state(None), state(5)
    assert not manager.can_undo and not manager.can_redo
    manager.save(original)
    assert manager.can_undo and not manager.can_redo
    assert manager.undo(changed) == original
    assert manager.can_redo and not manager.can_undo
    assert manager.redo(original) == changed
    assert manager.can_undo and not manager.can_redo

def test_empty_undo_redo_return_current():
    manager = MementoManager()
    current = state(2)
    assert manager.undo(current) == current
    assert manager.redo(current) == current

def test_save_clears_redo():
    manager = MementoManager()
    first, second = state(1), state(2)
    manager.save(first)
    manager.undo(second)
    manager.save(state(3))
    assert not manager.can_redo

"""Configure application logging to a file."""
import logging
from pathlib import Path


def setup_logging(log_file: str | Path = "calculator.log") -> logging.Logger:
    """Set up a file logger and return the calculator application logger.

    Repeated calls with the same file do not add duplicate handlers.
    """
    target = Path(log_file)
    target.parent.mkdir(parents=True, exist_ok=True)
    resolved_target = target.resolve()

    logger = logging.getLogger("calculator")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    already_configured = any(
        isinstance(handler, logging.FileHandler)
        and Path(handler.baseFilename).resolve() == resolved_target
        for handler in logger.handlers
    )
    if not already_configured:
        handler = logging.FileHandler(resolved_target, encoding="utf-8")
        handler.setLevel(logging.INFO)
        handler.setFormatter(logging.Formatter(
            "%(asctime)s %(levelname)s %(name)s: %(message)s"
        ))
        logger.addHandler(handler)

    return logger

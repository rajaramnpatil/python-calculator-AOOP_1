"""Environment-based application configuration."""
import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv
from .exceptions import ConfigurationError


@dataclass(frozen=True)
class CalculatorConfig:
    history_file: Path
    auto_save: bool
    precision: int
    log_file: Path = Path("calculator.log")


def _parse_bool(value: str, key: str) -> bool:
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    raise ConfigurationError(f"{key} must be a boolean value (true/false).")


def load_config(env_file: str | Path | None = ".env") -> CalculatorConfig:
    """Load and validate configuration, using defaults when unset."""
    if env_file is not None:
        # Keep explicitly exported environment variables higher priority than .env values.
        load_dotenv(dotenv_path=env_file, override=False)
    history_value = os.getenv("CALCULATOR_HISTORY_FILE", "calculator_history.csv").strip()
    if not history_value:
        raise ConfigurationError("CALCULATOR_HISTORY_FILE cannot be empty.")
    try:
        precision = int(os.getenv("CALCULATOR_PRECISION", "6"))
    except ValueError as exc:
        raise ConfigurationError("CALCULATOR_PRECISION must be an integer from 0 to 15.") from exc
    # Validate the display precision before it reaches REPL number formatting.
    if not 0 <= precision <= 15:
        raise ConfigurationError("CALCULATOR_PRECISION must be between 0 and 15.")
    auto_save = _parse_bool(os.getenv("CALCULATOR_AUTO_SAVE", "true"), "CALCULATOR_AUTO_SAVE")
    log_value = os.getenv("CALCULATOR_LOG_FILE", "calculator.log").strip()
    if not log_value:
        raise ConfigurationError("CALCULATOR_LOG_FILE cannot be empty.")
    return CalculatorConfig(Path(history_value), auto_save, precision, Path(log_value))

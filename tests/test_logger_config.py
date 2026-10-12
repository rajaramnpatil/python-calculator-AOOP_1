import logging

from app.logger_config import setup_logging


def test_setup_logging_writes_to_file(tmp_path):
    log_file = tmp_path / "logs" / "calculator.log"
    logger = setup_logging(log_file)
    try:
        logger.info("test log entry")
        for handler in logger.handlers:
            handler.flush()
        assert "test log entry" in log_file.read_text(encoding="utf-8")
    finally:
        for handler in list(logger.handlers):
            if isinstance(handler, logging.FileHandler) and handler.baseFilename == str(log_file.resolve()):
                logger.removeHandler(handler)
                handler.close()


def test_setup_logging_does_not_add_duplicate_handler(tmp_path):
    log_file = tmp_path / "calculator.log"
    logger = setup_logging(log_file)
    before = len(logger.handlers)
    setup_logging(log_file)
    assert len(logger.handlers) == before
    for handler in list(logger.handlers):
        if isinstance(handler, logging.FileHandler) and handler.baseFilename == str(log_file.resolve()):
            logger.removeHandler(handler)
            handler.close()

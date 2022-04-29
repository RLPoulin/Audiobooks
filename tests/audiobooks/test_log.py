import logging

from audiobooks.log import log_manager


def test_log_manager_level():
    assert log_manager.level == "INFO"


def test_get_logger():
    log = log_manager.get_logger(__name__, "INFO")
    assert isinstance(log, logging.Logger)
    assert log.name == "test_log"
    assert log.level == logging.INFO
    assert log_manager.get_logger(__name__) == log


def test_set_logger_level():
    log = log_manager.get_logger(__name__, "INFO")
    assert log.level == logging.INFO
    log_manager.set_logger_level(__name__, "DEBUG")
    assert log.level == logging.DEBUG


def test_set_all_levels():
    log_manager.set_all_levels("WARNING")
    assert log_manager.get_logger(__name__).level == logging.WARNING
    assert log_manager.get_logger("audiobooks.log").level == logging.WARNING


def test_shutdown():
    log_manager.shutdown()
    assert log_manager.loggers == {}

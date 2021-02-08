import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def func():
    logger.critical("a critical error")
    logger.debug("a debug message")

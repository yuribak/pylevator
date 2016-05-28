import logging
from logging import FileHandler

LEVEL_TRACE = 2


def getLogger(logger_name, file_name):
    logger = logging.getLogger(logger_name)
    logger.addHandler(FileHandler(file_name, mode='wb'))
    logger.setLevel(LEVEL_TRACE)

    def trace(s, *args):
        logger.log(LEVEL_TRACE, s, *args)

    logger.trace = trace

    return logger




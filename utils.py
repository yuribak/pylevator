import logging
from logging import FileHandler
import time

LEVEL_TRACE = 2


def getLogger(logger_name, file_name):
    logger = logging.getLogger(logger_name)
    logger.addHandler(FileHandler(file_name, mode='wb'))
    logger.setLevel(LEVEL_TRACE)

    def trace(s, *args):
        logger.log(LEVEL_TRACE, s, *args)

    logger.trace = trace

    return logger


class Timer(object):

    TIMERS = {}

    @staticmethod
    def timer(timer_name):
        return Timer.TIMERS.setdefault(timer_name, Timer())

    def __init__(self):
        self.start = time.time()
        self.offset = 0

    def time(self):
        return time.time() - self.start + self.offset

    def skip(self, s):
        self.offset += s


t = Timer()
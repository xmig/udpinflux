"""
Logging Stub
"""
from logging import getLevelName
from logging import (FATAL, ERROR, WARN, INFO, DEBUG, NOTSET)


class EmptyLogger(object):
    def __init__(self, log_level=FATAL+1):
        self.log_level = log_level

    def setLevel(self, level):
        self.log_level = level

    def getLevel(self):
        return self.log_level

    def _mess(self, level, mess):
        pass

    def log(self, mess):    self._mess(DEBUG, mess)
    def debug(self, mess):  self._mess(DEBUG, mess)
    def info(self, mess):   self._mess(INFO, mess)
    def warn(self, mess):   self._mess(WARN, mess)
    def warning(self, mess):self._mess(WARN, mess)
    def error(self, mess):  self._mess(ERROR, mess)
    def fatal(self, mess):  self._mess(FATAL, mess)


class PrintLogger(EmptyLogger):
    def __init__(self, log_level=DEBUG):
        super().__init__(log_level)

    def _mess(self, level, mess):
        if self.log_level <= level:
            print(mess)


def set_log_level(level_str, logger):
    """ Set up application log level
    :param level_str: <str> one of: FATAL, ERROR, WARN, INFO, DEBUG, NOTSET
    :return: None
    """
    for level in (FATAL, ERROR, WARN, INFO, DEBUG, NOTSET):
        if level_str.upper() == getLevelName(level):
            logger.setLevel(level)
            if level <= DEBUG:
                print("Log level {}".format(level_str))
            return
    print("Cannot set up log level as '{}'".format(level_str))



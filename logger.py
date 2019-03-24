#!/usr/bin/env python
import os.path
import logging
import logging.handlers
import conf


class logger(object):

    def __init__(self):

        logF = conf.LOG_FILE_NAME
        logPath = os.path.join(conf.LOG_DIR_PATH, logF)

        logger = logging.getLogger(__name__)
        logger.setLevel(level=conf.LOG_LEVEL)

        if not logger.handlers:
            formatter = logging.Formatter(conf.LOG_FORMAT, conf.DATE_FORMAT)

            # 1/log to console
            log2console = logging.StreamHandler()
            log2console.setFormatter(formatter)

            # 2a/log to file
            # log2file = logging.FileHandler(logPath)
            # log2file.setFormatter(formatter)

            # 2b/log to file with time rotate
            # log2fileTRot = logging.handlers.TimedRotatingFileHandler(
            #    logPath, when='midnight', interval=1, backupCount=10)
            # log2fileTRot.setFormatter(formatter)

            # 2c/log to file with file rotate
            log2fileFRot = logging.handlers.RotatingFileHandler(
                logPath, maxBytes=1*1024*1024, backupCount=10)
            log2fileFRot.setFormatter(formatter)

            logger.addHandler(log2console)
            # logger.addHandler(log2file)
            # logger.addHandler(log2fileTRot)
            logger.addHandler(log2fileFRot)

        self._logger = logger

    def get(self):
        return self._logger

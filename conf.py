#!/usr/bin/env python
import os
import logging.handlers
from datetime import datetime


NEXTLINE = '\n'

today = datetime.now()

# Define file name
IN_DIR_NAME = 'input'
OUT_DIR_NAME = 'output'
BATCH_DIR_NAME = today.strftime('%Y%m%d_%H%M')

# Define path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
IN_DIR_PATH = os.path.join(ROOT_DIR, IN_DIR_NAME)
OUT_DIR_PATH = os.path.join(ROOT_DIR, OUT_DIR_NAME)
BATCH_DIR_PATH = os.path.join(ROOT_DIR, OUT_DIR_PATH, BATCH_DIR_NAME)

# Log config
LOG_FORMAT = '%(asctime)s.%(msecs)03d %(module)-8s %(funcName)-8s %(levelname)-8s %(message)s'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

LOG_FILE_NAME = 'mylog.log'
LOG_LEVEL = logging.CRITICAL

LOG_DIR_NAME = 'log'
LOG_DIR_PATH = os.path.join(ROOT_DIR, LOG_DIR_NAME)
#!/usr/bin/env python
import os
import logging.handlers
from datetime import datetime


NEXTLINE = '\n'

today = datetime.now()

# Define file name
BATCH_NAME = today.strftime('%Y%m%d_%H%M')
FG2XLS_IN_DIR = 'fg2xls_input'
FG2XLS_OUT_DIR = 'fg2xls_output'

FGCONFGEN_BAS_DIR = 'fgconfgen_baseline'
FGCONFGEN_REQ_DIR = 'fgconfgen_req'


# Define path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
FG2XLS_IN_PATH = os.path.join(ROOT_DIR, FG2XLS_IN_DIR)
FG2XLS_OUT_PATH = os.path.join(ROOT_DIR, FG2XLS_OUT_DIR)
BATCH_PATH = os.path.join(ROOT_DIR, FG2XLS_OUT_PATH, BATCH_NAME)

FGCONFGEN_BAS_PATH = os.path.join(ROOT_DIR, FGCONFGEN_BAS_DIR)
FGCONFGEN_REQ_PATH = os.path.join(ROOT_DIR, FGCONFGEN_REQ_DIR)

# Log config
LOG_FORMAT = '%(asctime)s.%(msecs)03d %(module)-8s %(funcName)-8s %(levelname)-8s %(message)s'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

LOG_FILE_NAME = 'mylog.log'
LOG_LEVEL = logging.CRITICAL

LOG_DIR_NAME = 'log'
LOG_DIR_PATH = os.path.join(ROOT_DIR, LOG_DIR_NAME)
#!/usr/bin/env python
# by kkyick2
# import pkg
import os
import sys
from os import listdir
from os.path import isfile, join
from shutil import copy2
# import 3rd parties pkg
# import project pkg
from tools import logger
import conf
from fg2csv.fg2csv import fg2csv
from tools.csv2xlsx import csv2xlsx
from tools.vdomcutter import vdomcutter


def mkdir(path):
    """
        Create a directory
        @param path : full path folder to be create
        @rtype: na
    """
    logger1 = logger.logger().get()
    # create fg2xls_output batch folder
    try:
        os.makedirs(path)
        logger1.info('create dir: ' + path)
    except OSError as e:
        logger1.warning('fail create dir: ' + path)
        logger1.warning(e)
        if not os.path.isdir(path):
            raise
    return


def getdir2filelist(path):
    """
        Create a List that contain the filename in the folder
        @param path : full path folder that contain files
        @rtype: return a list of filename
    """
    return [f for f in listdir(path) if isfile(join(path, f))]


def start():
    """
        start() to enter script  task
        create directory, py2csv, csv2xlsx, vdomcutter
        @param: na
        @rtype: na
    """
    # define logger
    logger1 = logger.logger().get()
    logger1.info('start script: '+__name__)
    print ('start script: '+__name__)

    # define conf file list from fg2xls_input folder
    confList = []
    try:
        confList = getdir2filelist(conf.FG2XLS_IN_PATH)
        logger1.info('read fg2xls_input: ' + conf.FG2XLS_IN_PATH)
        logger1.info('read config files: ' + str(confList))
        if not confList:
            logger1.warning('Terminate, fg2xls_input folder empty!')
            sys.exit('Terminate, fg2xls_input folder empty!')
    except OSError as e:
        logger1.warning(e)

    # create fg2xls_output batch folder
    mkdir(conf.BATCH_PATH)

    # loop each config file in fg2xls_input file
    for filename in confList:

        # define configFileName's full path
        config_file = os.path.join(conf.FG2XLS_IN_PATH, filename)

        # create result folder
        result_dir = os.path.join(conf.BATCH_PATH, filename)
        mkdir(result_dir)

        # convent config to csv
        logger1.info('convent conf to csv: ' + filename)
        print ('convent conf to csv: ' + filename)
        fg2csv(config_file, result_dir)

        # convent csv to xlsx
        logger1.info('convent csv to xlsx: ' + filename)
        print ('convent csv to xlsx: ' + filename)
        return_xls_path = csv2xlsx(filename, result_dir, result_dir)

        # cut fgconfig to multi vdom txt
        logger1.info('cutvdom to txt: ' + filename)
        print ('cutvdom to txt: ' + filename)
        vdomcutter(filename, config_file, result_dir)

        # copy original config to fg2xls_output folder
        copy2(config_file, result_dir)

        # copy conf.xls to baseline folder
        copy2(return_xls_path, conf.FGCONFGEN_BAS_PATH)

    logger1.info('end script: '+__name__)
    print ('end script: '+__name__)
    return


if __name__ == "__main__":
    start()
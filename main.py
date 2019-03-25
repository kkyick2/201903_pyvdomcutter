#!/usr/bin/env python
# by kkyick2
# import pkg
import os
import sys
from os import listdir
from os.path import isfile, join
# import 3rd parties pkg
# import project pkg
import conf
import logger
from fg2csv.fg2csv import fg2csv
from csv2xlsx import csv2xlsx
from vdomcutter import vdomcutter


def mkdir(path):
    """
        Create a directory
        @param path : full path folder to be create
        @rtype: na
    """
    logger1 = logger.logger().get()
    # create output batch folder
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

    # define conf file list from input folder
    confList = []
    try:
        confList = getdir2filelist(conf.IN_DIR_PATH)
        logger1.info('read input: ' + conf.IN_DIR_PATH)
        logger1.info('read config files: ' + str(confList))
        if not confList:
            logger1.warning('Terminate, input folder empty!')
            sys.exit('Terminate, input folder empty!')
    except OSError as e:
        logger1.warning(e)

    # create output batch folder
    mkdir(conf.BATCH_DIR_PATH)

    # loop each config file in input file
    for filename in confList:

        # define configFileName's path
        config_file = os.path.join(conf.IN_DIR_PATH, filename)

        # create result folder
        result_dir = os.path.join(conf.BATCH_DIR_PATH, filename)
        mkdir(result_dir)

        # convent config to csv
        logger1.info('convent conf to csv: ' + filename)
        print ('convent conf to csv: ' + filename)
        fg2csv(config_file, result_dir)

        # convent csv to xlsx
        logger1.info('convent csv to xlsx: ' + filename)
        print ('convent csv to xlsx: ' + filename)
        csv2xlsx(result_dir, result_dir, filename)

        # cut fgconfig to multi vdom txt
        logger1.info('cutvdom to txt: ' + filename)
        print ('cutvdom to txt: ' + filename)
        vdomcutter(config_file, result_dir)

    logger1.info('end script: '+__name__)
    print ('end script: '+__name__)
    return


if __name__ == "__main__":
    start()
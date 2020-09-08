#!/usr/bin/env python
# by kkyick2
# import pkg
import os
import re
from shutil import copy2
# import 3rd parties pkg
# import project pkg
from . import logger


def vdomcutter(filename, infile, outdir):
    """
        fg2xls_input a fg config and cut each vdom to txt file
        @param filename : filename of the config
        @param infile : fg2xls_input file full path of the fg config
        @param outdir : fg2xls_output folder: full path for the fg2xls_output folder
        @rtype: na
    """
    logger1 = logger.logger().get()

    # 1/ find version of the fortigate
    firstline = ''
    version = ''
    with open(infile, 'r') as inF:
        firstline = inF.readline()
        #print(firstline)
        MODEL = 'MODEL'
        VERSION = 'VERSION'
        BUILD = 'BUILD'
        OTHER = 'OTHER'
        # config-version=FGT61E-6.0.6-FW-build0272-190716:opmode=0:vdom=0:user=col
        p_firstline = re.compile('^\s*#config-version=+(?P<MODEL>\S+)-(?P<VERSION>\S+)-FW-(?P<BUILD>\S+):(?P<OTHER>.*)$', re.IGNORECASE)
        if p_firstline.search(firstline):
            model = p_firstline.search(firstline).group(MODEL)
            version = p_firstline.search(firstline).group(VERSION)
            build = p_firstline.search(firstline).group(BUILD)
            other = p_firstline.search(firstline).group(OTHER)
            print('info: ', model, ' | ', version, ' | ', build, ' | ', other)

    # 2/ read the file as data
    with open(infile, 'r') as inF:
        data = inF.read()
    # find the vdom name in conf to a list
    p_foundvdom = re.findall(r'\n*(config\svdom.*?\nconfig\ssystem\ssettings)\n*', data, re.M | re.S)
    # find the content of each vdom to a list
    p_foundcontent = re.findall(r'\n*(config\svdom.*?\nend\nend\n)\n*', data, re.M | re.S)

    # 3/ create vdom list and cut vdom
    vdomList = []
    for i in range(0, len(p_foundvdom)):
        name = p_foundvdom[i].split('\n')[1].rstrip()[5:]
        vdomList.append(name)
    logger1.info('cut', len(vdomList), 'vdom to txt: ', str(vdomList))
    print('cut', len(vdomList), 'vdom to txt: ', str(vdomList))

    # 4/ check fortigate version
    '''
    below are sytenx for fortigate version >=6, 
    --------------------
    end
    end

    config vdom
    edit root
    --------------------
    below are sytenx for fortigate version below 5, 
    --------------------
    end

    end

    config vdom
    edit root
    --------------------
    '''
    index = 0
    # for fortigate version <6, index is 1'
    if int(version[0]) <6:
        index = 1

    # 5/ write each vdom to txt in fg2xls_output folder
    # print(len(p_foundcontent), ' | ', len(p_foundvdom))
    for i in range(1, len(p_foundcontent) + index):
        with open(os.path.join(outdir, filename + '_' + vdomList[i - 1] + '.txt'), 'w') as outF:
            outF.write(p_foundcontent[i - 1])
    # copy original config to fg2xls_output folder
    # copy2(infile, outdir)
    print(' ')
    return

#!/usr/bin/env python
# by kkyick2
# import pkg
import os
import re
from shutil import copy2


# import 3rd parties pkg
# import project pkg
# from . import logger


def vdomcutter(filename, infile, outdir):
    """
        fg2xls_input a fg config and cut each vdom to txt file
        @param filename : filename of the config
        @param infile : fg2xls_input file full path of the fg config
        @param outdir : fg2xls_output folder: full path for the fg2xls_output folder
        @rtype: na
    """
    # logger1 = logger.logger().get()
    # ================================================
    # 1/ find version of the fortigate
    version = ''
    with open(infile, 'r') as inF:
        firstline = inF.readline()
        # print(firstline)
        MODEL = 'MODEL'
        VERSION = 'VERSION'
        BUILD = 'BUILD'
        OTHER = 'OTHER'
        # config-version=FGT61E-6.0.6-FW-build0272-190716:opmode=0:vdom=0:user=col
        p_firstline = re.compile(
            '^\s*#config-version=+(?P<MODEL>\S+)-(?P<VERSION>\S+)-FW-(?P<BUILD>\S+):(?P<OTHER>.*)$', re.IGNORECASE)
        if p_firstline.search(firstline):
            model = p_firstline.search(firstline).group(MODEL)
            version = p_firstline.search(firstline).group(VERSION)
            build = p_firstline.search(firstline).group(BUILD)
            other = p_firstline.search(firstline).group(OTHER)
            print('Info: ', model, ' | ', version, ' | ', build, ' | ', other)

    # ================================================

    '''
    --------------------
    Sytenx for fortigate version below <6, 
    --------------------
    config global           | p_foundcontent_g[0]
    ..                      |
    end                     |
                            |
    end                     |
                            |
    config vdom             | p_foundcontent[0]
    edit root               |
    config system settings  |
    ...
    --------------------
    Sytenx for fortigate version >=6:
    --------------------
    config global           | p_foundcontent[0]
    ..                      |
    end                     |
    end                     |
                            |
    config vdom             | p_foundcontent[1]
    edit root               |
    config ssystem object-tagging
    ...
    --------------------
    '''
    # 2/ read the file as data
    with open(infile, 'r') as inF:
        data = inF.read()

    # 3A/ handle fortigate version <6'
    if int(version[0]) < 6:
        # find vdom name
        p_foundvdom = re.findall(r'\n*(config\svdom.*?\nconfig\ssystem\ssettings)\n*', data, re.M | re.S)
        # find content of each vdom
        p_foundcontent = re.findall(r'\n*(config\svdom\nedit\s[^\n]+\nconfig\ssystem\ssettings.*?\nend\nend\n)\n*', data, re.M | re.S)
        # find content of global
        p_foundcontent_g = re.findall(r'\n*(config\svdom.*?\nend\n\nend\n)\n*', data, re.M | re.S)

    # 3B/ handle fortigate version >=6'
    else:
        # find vdom name
        p_foundvdom = re.findall(r'\n*(config\svdom.*?\nconfig\ssystem\sobject-tagging)\n*', data, re.M | re.S)
        # find content of each vdom + global
        p_foundcontent = re.findall(r'\n*(config\svdom.*?\nend\nend\n)\n*', data, re.M | re.S)
        # find content of global (no use for version >=6)
        p_foundcontent_g = []

    # ================================================
    # 4/ create vdom list
    vdomList = []
    for i in range(0, len(p_foundvdom)):
        name = p_foundvdom[i].split('\n')[1].rstrip()[5:]
        vdomList.append(name)
    # logger1.info('cut', len(vdomList), 'vdom to txt: ', str(vdomList))
    print('content|vdom: ', len(p_foundcontent),'+',len(p_foundcontent_g), '|', len(p_foundvdom), '+ global || ', len(vdomList), 'vdom: ', str(vdomList), '+ global')

    # ================================================
    # 5A/ write each vdom to txt in fg2xls_output folder, for fortigate version <6'
    if int(version[0]) < 6:
        with open(os.path.join(outdir, filename + '_global.txt'), 'w') as outF0:
            outF0.write(p_foundcontent_g[0])  ##Global Vdom

        for i in range(0, len(p_foundcontent)):
            # print(i, ' | ', index, ' | ', vdomList[i - 1])
            with open(os.path.join(outdir, filename + '_' + vdomList[i - 1] + '.txt'), 'w') as outF:
                outF.write(p_foundcontent[i - 1])

    # 5B/ write each vdom to txt in fg2xls_output folder, for fortigate version >=6'
    else:
        for i in range(0, len(p_foundcontent)):
            # print(i, ' | ', index, ' | ', vdomList[i - 1])
            with open(os.path.join(outdir, filename + '_global.txt'), 'w') as outF0:
                outF0.write(p_foundcontent[0])  ##Global Vdom

            with open(os.path.join(outdir, filename + '_' + vdomList[i - 1] + '.txt'), 'w') as outF:
                outF.write(p_foundcontent[i])
    return

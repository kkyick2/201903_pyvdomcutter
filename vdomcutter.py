#!/usr/bin/env python
# by kkyick2
# import pkg
import os
import re
# import 3rd parties pkg
# import project pkg
import logger


def vdomcutter(infile, outdir):
    """
        input a fg config and cut each vdom to txt file
        @param infile : input filename of the fg config
        @param outdir : output folder: full path for the output folder
        @rtype: na
    """
    logger1 = logger.logger().get()
    with open(infile, 'r') as inF:
        data = inF.read()

    # find the vdom name in conf to a list
    p_foundvdom = re.findall(r'\n*(config\svdom.*?\nconfig\ssystem\ssettings)\n*', data, re.M | re.S)
    # find the content of each vdom to a list
    p_foundcontent = re.findall(r'\n*(config\svdom.*?\nend\nend\n)\n*', data, re.M | re.S)

    # create a vdom list
    vdomList = []
    for i in range(0, len(p_foundvdom)):
        name = p_foundvdom[i].split('\n')[1].rstrip()[5:]
        vdomList.append(name)
    logger1.info('cut vdom config to txt: ' + str(vdomList))
    # write to each file
    for i in range(1, len(p_foundcontent) + 1):
        with open(os.path.join(outdir, vdomList[i - 1] + '.txt'), 'w') as outF:
            outF.write(p_foundcontent[i - 1])
    return

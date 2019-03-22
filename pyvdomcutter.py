#!/usr/bin/env python
# by kkyick2
import re


def main(input_file):
    """
        Dat main
    """
    with open(input_file, 'r') as inF:
        data = inF.read()

    # find the vdom name in conf to a list
    foundvdom = re.findall(r'\n*(config\svdom.*?\nconfig\ssystem\ssettings)\n*', data, re.M | re.S)
    # find the content of each vdom to a list
    foundcontent = re.findall(r'\n*(config\svdom.*?\nend\nend\n)\n*', data, re.M | re.S)

    # create a vdom list
    vdomList = []
    for i in range(0, len(foundvdom)):
        name = foundvdom[i].split('\n')[1].rstrip()[5:]
        vdomList.append(name)

    # write to each file
    for i in range(1, len(foundcontent) + 1):
        print vdomList[i - 1]
        with open(vdomList[i - 1] + '.txt', 'w') as outF:
            outF.write(foundcontent[i - 1])

    return



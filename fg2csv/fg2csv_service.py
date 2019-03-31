#!/usr/bin/env python
# 20190322 | add vdom definition block | kkyick2 modify
# -*- coding: utf-8 -*-

# This file is part of fg2csv.
#
# Copyright (C) 2014, Thomas Debize <tdebize at mail.com>
# All rights reserved.
#
# fg2csv is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# fg2csv is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with fg2csv.  If not, see <http://www.gnu.org/licenses/>.

import re
import os
import sys
import csv

# OptionParser imports
from optparse import OptionParser

# Options definition
option_0 = {'name': ('-i', '--fg2xls_input-file'), 'help': '<INPUT_FILE>: Fortigate configuration file. Ex: fgfw.cfg',
            'nargs': 1}
option_1 = {'name': ('-o', '--fg2xls_output-file'), 'help': '<OUTPUT_FILE>: fg2xls_output csv file (default \'./policies-out.csv\')',
            'default': 'policies-out.csv', 'nargs': 1}
option_2 = {'name': ('-n', '--newline'),
            'help': '<NEWLINE> : insert a newline between each policy for better readability', 'action': 'store_true',
            'default': False}
option_3 = {'name': ('-s', '--skip-header'), 'help': '<SKIP_HEADER> : do not print the csv header',
            'action': 'store_true', 'default': False}

options = [option_0, option_1, option_2, option_3]

# Handful patterns

# -- Entering vdom definition block
p_entering_vdom = re.compile('^\s*config vdom$', re.IGNORECASE)
p_vdom_name = re.compile('^\s*edit\s+(?P<vdom_name>\w+)', re.IGNORECASE)

# -- Entering policy definition block
p_entering_policy_block = re.compile('^\s*config firewall service custom$', re.IGNORECASE)

# -- Exiting policy definition block
p_exiting_policy_block = re.compile('^end$', re.IGNORECASE)

# -- Commiting the current policy definition and going to the next one
p_policy_next = re.compile('^next$', re.IGNORECASE)

# -- Policy number
p_policy_number = re.compile('^\s*edit\s+"(?P<policy_number>.*)"$', re.IGNORECASE)

# -- Policy setting
p_policy_set = re.compile('^\s*set\s+(?P<policy_key>\S+)\s+(?P<policy_value>.*)$', re.IGNORECASE)

# Functions
def parse(fd):
    """
        Parse the data according to several regexes

        @param fd:	fg2xls_input file descriptor
        @rtype:	return a list of policies ( [ {'id' : '1', 'srcintf' : 'internal', ...}, {'id' : '2', 'srcintf' : 'external', ...}, ... ] )
                and the list of unique seen keys ['id', 'srcintf', 'dstintf', ...]
    """
    global p_entering_vdom, p_vdom_name, p_entering_policy_block, p_exiting_policy_block, p_policy_next, p_policy_number, p_policy_set

    vdom_name = None

    in_vdom_block = False
    in_policy_block = False

    policy_list = []
    policy_elem = {}

    order_keys = []

    with open(fd, 'rb') as fd_input:
        for line in fd_input:
            line = line.lstrip().rstrip().strip()

            # We match a vdom block "config vdom"
            if p_entering_vdom.search(line):
                in_vdom_block = True

            # We are in a vdom block, get the vdom name
            if p_vdom_name.search(line) and in_vdom_block is True:
                vdom_name = p_vdom_name.search(line).group('vdom_name')
                if not ('vdom' in order_keys): order_keys.append('vdom')
                in_vdom_block = False

            # We match a policy block
            if p_entering_policy_block.search(line):
                in_policy_block = True

            # We are in a policy block
            if in_policy_block:
                if p_policy_number.search(line):
                    policy_number = p_policy_number.search(line).group('policy_number')
                    policy_elem['vdom'] = vdom_name
                    policy_elem['name'] = policy_number
                    if not ('name' in order_keys): order_keys.append('name')

                # We match a setting
                if p_policy_set.search(line):
                    policy_key = p_policy_set.search(line).group('policy_key')
                    if not (policy_key in order_keys): order_keys.append(policy_key)

                    policy_value = p_policy_set.search(line).group('policy_value').strip()
                    policy_value = re.sub('["]', '', policy_value)

                    policy_elem[policy_key] = policy_value

                # We are done with the current policy id
                if p_policy_next.search(line):
                    policy_list.append(policy_elem)
                    policy_elem = {}

            # We are exiting the policy block
            if p_exiting_policy_block.search(line):
                in_policy_block = False

    return (policy_list, order_keys)


def generate_csv(results, keys, fd, newline, skip_header):
    """
        Generate a plain ';' separated csv file

        @param fd : fg2xls_output file descriptor
    """
    if results and keys:
        with open(fd, 'wb') as fd_output:
            spamwriter = csv.writer(fd_output)

            if not (skip_header):
                spamwriter.writerow(keys)

            for policy in results:
                output_line = []

                for key in keys:
                    if key in policy.keys():
                        output_line.append(policy[key])
                    else:
                        output_line.append('')

                spamwriter.writerow(output_line)
                if newline: spamwriter.writerow('')

        fd_output.close()

    return


def main(options, arguments):
    """
        Dat main
    """
    if (options.input_file == None):
        parser.error('Please specify a valid fg2xls_input file')

    results, keys = parse(options.input_file)
    generate_csv(results, keys, options.output_file, options.newline, options.skip_header)

    return


def main2(input_file, output_file, newline, skip_header):
    """
        Dat main
    """
    if (input_file == None):
        parser.error('Please specify a valid fg2xls_input file')

    results, keys = parse(input_file)
    generate_csv(results, keys, output_file, newline, skip_header)

    return


if __name__ == "__main__":
    parser = OptionParser()
    for option in options:
        param = option['name']
        del option['name']
        parser.add_option(*param, **option)

    options, arguments = parser.parse_args()
    main(options, arguments)

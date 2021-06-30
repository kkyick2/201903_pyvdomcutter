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
import parser
import re
import os
import sys
import csv

# OptionParser imports
from optparse import OptionParser


# backwards compatibility for python3 and python2 csv writer
def open_csv(filename, mode):
    """
    Open a csv file in proper mode depending on Python verion.
    with open (outfilename, 'wb') as outF: 					# this code is for python2
    with open (outfilename, 'w', newline='') as outF:	 	# this code is for python3
    """
    return open(filename, mode=mode + 'b') if sys.version_info[0] == 2 else open(filename, mode=mode, newline='')


# Parse the data according to several regexes
def parse(fd):
    """
        Parse the data according to several regexes
        @param fd:	fg2xls_input file descriptor
        @rtype:	return a list of policies and list of unique seen keys
        policy_list = [ {'id' : '1', 'srcintf' : 'internal', ...}, {'id' : '2', 'srcintf' : 'external', ...}, ... ]
        order_keys = ['id', 'srcintf', 'dstintf', ...]
        policy_elem = { xxx }
    """
    """                                         0
    config vdom                                 1
    edit PTH1HKATS1                             1
    ...                                         1
    config firewall DoS-policy                  1>2
        edit 1                                  2
            set interface "W.HKATS"             2
            set srcaddr "all"                   2
            set dstaddr "all"                   2
            set service "ALL"                   2
            config anomaly                      2>3
                edit "tcp_syn_flood"            3
                    set status enable           3
                    set log enable              3
                    set action block            3
                    set threshold 1000          3
                next                            3
                edit "tcp_port_scan"            3
                    set status enable           3
                    set log enable              3
                    set action block            3
                    set threshold 5000          3
                next                            3
            end                                 3>2
        next                                    2
        edit 2                                  2
            set interface "W.HKATS"             2
            set srcaddr "all"                   2
            set dstaddr "all"                   2
            set service "ALL"                   2
            config anomaly                      2>3
                edit "tcp_syn_flood"            3
                    set status enable           3
                    set log enable              3
                    set action block            3
                    set threshold 1000          3
                next                            3
                edit "tcp_port_scan"            3
                    set status enable           3
                    set log enable              3
                    set action block            3
                    set threshold 5000          3
                next                            3
            end                                 3>2
        next                                    2
    end                                         2>1
    end                                         1>0
    """
    # -- Entering vdom definition block
    p1_vdom_enter = re.compile('^\s*config vdom$', re.IGNORECASE)
    p1_vdom_name = re.compile('^\s*edit\s+(?P<vdom_name>\w+)', re.IGNORECASE)

    # -- Entering dos-policy definition block
    p2_policy_enter = re.compile('^\s*config firewall DoS-policy$', re.IGNORECASE)
    # -- Exiting dos-policy definition block
    p2_policy_end = re.compile('^end$', re.IGNORECASE)
    # -- Commiting the current policy definition and going to the next one
    p2_policy_next = re.compile('^next$', re.IGNORECASE)
    # -- dos-Policy number
    p2_policy_number = re.compile('^\s*edit\s+(?P<policy_number>\d+)', re.IGNORECASE)
    # -- dos-Policy setting
    p2_policy_set = re.compile('^\s*set\s+(?P<policy_key>\S+)\s+(?P<policy_value>.*)$', re.IGNORECASE)

    # -- Entering anomaly block
    p3_anomaly_enter = re.compile('^\s*config anomaly$', re.IGNORECASE)
    # -- Exiting anomaly block
    p3_anomaly_end = re.compile('^end$', re.IGNORECASE)
    # -- Commiting the current anomaly and going to the next one
    p3_anomaly_next = re.compile('^next$', re.IGNORECASE)
    # -- anomaly type
    p3_anomaly_type = re.compile('^\s*edit\s+(?P<anomaly_type>\S+)', re.IGNORECASE)
    # -- anomaly setting
    p3_anomaly_set = re.compile('^\s*set\s+(?P<anomaly_key>\S+)\s+(?P<anomaly_value>.*)$', re.IGNORECASE)

    # 0begin
    # 1vdom
    # 2dos-policy
    # 3anomaly
    block = 0
    vdom_name = None
    in_vdom_block = False

    policy_list = []
    policy_elem = {}
    order_keys = []

    policy_elem_dos = {}
    policy_elem_ano = {}

    with open_csv(fd, 'r') as fd_input:
        for line in fd_input:
            line = line.lstrip().rstrip().strip()
            # ==========================================================
            # print debug use
            # print(block, ' | ', line)
            # ==========================================================
            # 0 begin
            # detect "config vdom"
            if p1_vdom_enter.search(line):
                in_vdom_block = True
                block = 1
            # detect "edit <vdom_name>"
            if p1_vdom_name.search(line) and in_vdom_block is True:
                vdom_name = p1_vdom_name.search(line).group('vdom_name')
                if not ('vdom' in order_keys): order_keys.append('vdom')
                in_vdom_block = False
            # ==========================================================
            # enter 1 vdom
            if block == 1:
                # detect "config firewall DoS-policy", 1>2
                if p2_policy_enter.search(line):
                    block = 2
                    continue
            # ==========================================================
            # enter 2 dos-policy
            if block == 2:
                # detect "edit x", 2
                if p2_policy_number.search(line):
                    policy_number = p2_policy_number.search(line).group('policy_number')
                    policy_elem['vdom'] = vdom_name
                    policy_elem['id'] = policy_number
                    if not ('id' in order_keys): order_keys.append('id')

                # detect "set xxx yyy", 2
                if p2_policy_set.search(line):
                    policy_key = p2_policy_set.search(line).group('policy_key')
                    policy_value = p2_policy_set.search(line).group('policy_value').strip()
                    policy_value = re.sub('["]', '', policy_value)
                    policy_elem[policy_key] = policy_value
                    if not (policy_key in order_keys): order_keys.append(policy_key)
                    # policy_elem_final = policy_elem_dos + policy_elem_ano
                    policy_elem_dos = policy_elem.copy()

                # detect next dos-policy, 2
                if p2_policy_next.search(line):
                    # done policy row, append to policy_elem
                    continue
                # detect end of dos-policy, 2>1
                if p2_policy_end.search(line):
                    block = 1
                    continue
                # detect "config anomaly" 2>3
                if p3_anomaly_enter.search(line):
                    block = 3
                    continue
            # ==========================================================
            # enter 3 anomaly
            if block == 3:
                # detect edit "tcp_syn_flood", 3
                if p3_anomaly_type.search(line):
                    anomaly_type = p3_anomaly_type.search(line).group('anomaly_type')
                    anomaly_type = re.sub('["]', '', anomaly_type)
                    policy_elem['anomaly_type'] = anomaly_type
                    if not ('anomaly_type' in order_keys): order_keys.append('anomaly_type')
                # detect "set xxx yyy", 3
                if p3_anomaly_set.search(line):
                    anomaly_key = p3_anomaly_set.search(line).group('anomaly_key')
                    anomaly_value = p3_anomaly_set.search(line).group('anomaly_value').strip()
                    anomaly_value = re.sub('["]', '', anomaly_value)
                    policy_elem[anomaly_key] = anomaly_value
                    if not (anomaly_key in order_keys): order_keys.append(anomaly_key)
                    # policy_elem_final = policy_elem_dos + policy_elem_ano
                    policy_elem_ano = policy_elem.copy()

                # detect next anomaly, 3
                if p3_anomaly_next.search(line):
                    # this is end of output row, append the element dict to list
                    ####################################################
                    # policy_elem_final = policy_elem_dos + policy_elem_ano
                    policy_elem_final = {**policy_elem_dos, **policy_elem_ano}
                    # print(policy_elem_dos)
                    # print(policy_elem_ano)
                    # print(policy_elem_final)
                    # done policy row, append to policy_elem
                    policy_list.append(policy_elem_final)
                    policy_elem = {}
                    ####################################################
                # detect end of anomaly, 3>2
                if p3_anomaly_end.search(line):
                    block = 2

    return policy_list, order_keys


def generate_csv(results, keys, fd, newline, skip_header):
    """
        Generate a plain ';' separated csv file

        @param fd : fg2xls_output file descriptor
    """
    if results and keys:
        with open_csv(fd, 'a') as fd_output:
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

    results, keys = parse(options.input_file)
    generate_csv(results, keys, options.output_file, options.newline, options.skip_header)

    return


def main2(input_file, output_file, newline, skip_header):
    """
        Dat main
    """
    results, keys = parse(input_file)
    generate_csv(results, keys, output_file, newline, skip_header)

    return


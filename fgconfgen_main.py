#!/usr/bin/env python
# by kkyick2
# import pkg
from collections import Iterable, OrderedDict
# import 3rd parties pkg
import openpyxl
# import project pkg
from tools import logger
import conf

NEXTLINE = '\r\n'


def write_row(outF, row):
    outF.write(row)


def xls2_policy_list(infile, sheet, vdom):
    """
        @param:	infile: full path of the xlsx, accept two format
                    1) if have vdom column, filter the input para vdom after output
                    2) if no vdom column, assume all policy in same vdom
                sheet: xlsx sheet name
                vdom: for filter only this vdom to output list
    """
    logger1 = logger.logger().get()
    # workbook object is created
    wb_obj = openpyxl.load_workbook(infile)
    sheet_obj = wb_obj.get_sheet_by_name(sheet)
    max_col = sheet_obj.max_column
    max_row = sheet_obj.max_row
    print('start: p_xls2dictList: (vdom, sheet): {},{}'.format(vdom, sheet))
    logger1.info('start: p_xls2dictList: (vdom, sheet): {},{}'.format(vdom, sheet))
    logger1.info('***** vdom: all - raw sheet size with heading col,row: {},{}'.format(max_col, max_row))

    order_keys = []  # [vdom, id, name, ...]
    policy_elem = {}  # {vdom:root, id:1,name: policy1, ... }
    policy_list = []  # [{vdom:root, id:1,name: policy1, ... }, {vdom:root, id:2,name: policy2, ... }, ... }

    # loop for each row V in xlsx
    for y in range(1, max_row + 1):
        # loop for each column -> in xlsx
        for x in range(1, max_col + 1):
            cell_obj = sheet_obj.cell(row=y, column=x)
            # 1st row is key
            if y is 1:
                order_keys.append(cell_obj.value)
            # 2nd row is content
            else:
                policy_key = order_keys[x - 1]
                policy_elem[policy_key] = cell_obj.value
                #  logger1.debug('cell({}, {}): (key|val) is: {} | {}'
                #              .format(str(x),str(y),str(policy_key),str(cell_obj.value)))
        if len(policy_elem) > 0:
            # 1) if have vdom column, filter input vdom only for output
            if 'vdom' in order_keys:
                if policy_elem['vdom'] == vdom:
                    policy_list.append(policy_elem)
            # 2) if no vdom column, assume all policy in same vdom for output
            else:
                policy_list.append(policy_elem)
        # end of the policy, clear the dictionary and loop next one
        policy_elem = {}

    # after consolidate the sheet, result in policy_list
    logger1.info('***** {}, {} -- Total {} items'.format(vdom,sheet,len(policy_list)))
    print ('***** {}, {} -- Total {} items'.format(vdom,sheet,len(policy_list)))
    logger1.info('end')
    return policy_list, order_keys


def gen_conf_policy(dictList, keys, vdom):
    """
        @param:	policydictList: a list of policies in dictionary format
                    [ {'id' : '1', 'srcintf' : 'internal', ...}, {'id' : '2', 'srcintf' : 'external', ...}, ... ]
                keys: a list of unique seen keys
                    ['id', 'srcintf', 'dstintf', ...]
                vdom: vdom name for output "config vdom, edit <vdom>"
    """
    logger1 = logger.logger().get()
    print('start: gen_conf_policy: (vdom): {}, Total policy to gen is {}'.format(vdom,len(dictList)))
    logger1.info('start: gen_conf_policy: (vdom): {}, Total policy to gen is {}'.format(vdom,len(dictList)))
    logger1.info('***** User input vdom is: ' + vdom )
    if 'vdom' in keys:
        logger1.info('***** requirement xls vdom is: ' + str(dictList[0]['vdom']))
    else:
        logger1.info('***** requirement xls do not have vdom, skip vdom key')

    if dictList and keys:
        logger1.info('gen config to txt')
        with open( vdom + '_conf.txt', 'wb') as outF:
            # First section [config vdom, edit <vdom>, config firewall policy]
            write_row(outF, 'config vdom' + NEXTLINE)
            write_row(outF, 'edit ' + vdom + NEXTLINE)
            write_row(outF, 'config firewall policy ' + NEXTLINE)

            # loop for each policy in dictionary format, {'vdom:'root,'id':'999,'ippool':None,'uuid':'948a...' .}
            for policydict in dictList:
                # loop for each key to follow the order
                for key in keys:
                    if key in policydict.keys() and policydict[key]:
                        # skip vdom column in xlsx
                        if key == 'vdom':
                            continue
                        # edit <id>
                        elif key == 'id':
                            write_row(outF, 'edit ' + str(policydict[key]) + NEXTLINE)
                        elif key == 'name' or key == 'comments':
                            write_row(outF, 'set ' + str(key) + ' "' + str(policydict[key]) + '"'+ NEXTLINE)
                        elif key == 'uuid':
                            continue
                        elif key == 'Config Change Date':
                            continue
                        else:
                            write_row(outF, 'set ' + str(key) + ' ' + str(policydict[key]) + NEXTLINE)
                # End of each policy [next]
                write_row(outF, "next" + NEXTLINE)
                write_row(outF, NEXTLINE)
            # End section [end]
            write_row(outF, "end" + NEXTLINE)
    logger1.info('end')


def xls2_obj_list(infile, sheet, vdom, key):
    """
        @param:	infile: full path of the xlsx, accept two format
                    1) if have vdom column, filter the input para vdom after output
                    2) if no vdom column, assume all policy in same vdom
                sheet: xlsx sheet name
                vdom: for filter only this vdom to output list
    """
    logger1 = logger.logger().get()
    print('start: p_getobjList: (vdom, sheet, key): {},{},{}'.format(vdom,sheet,key))
    logger1.info('start: p_getobjList: (vdom, sheet, key): {},{},{}'.format(vdom,sheet,key))

    # workbook object is created
    wb_obj = openpyxl.load_workbook(infile)
    sheet_obj = wb_obj.get_sheet_by_name(sheet)
    max_col = sheet_obj.max_column
    max_row = sheet_obj.max_row

    order_keys = []  # [vdom, id, name, ...]
    policy_elem = {}  # {vdom:root, id:1,name: policy1, ... }
    policy_list = []  # [{vdom:root, id:1,name: policy1, ... }, {vdom:root, id:2,name: policy2, ... }, ... }

    # loop for each row V in xlsx
    for y in range(1, max_row + 1):
        # loop for each column -> in xlsx
        for x in range(1, max_col + 1):
            cell_obj = sheet_obj.cell(row=y, column=x)
            # 1st row is key
            if y is 1:
                order_keys.append(cell_obj.value)
            # 2nd row is content
            else:
                policy_key = order_keys[x - 1]
                policy_elem[policy_key] = cell_obj.value
        if len(policy_elem) > 0:
            # 1) if have vdom column, filter input vdom only for output
            if 'vdom' in order_keys:
                if policy_elem['vdom'] == vdom:
                    policy_list.append(policy_elem)
            # 2) if no vdom column, assume all policy in same vdom for output
            else:
                policy_list.append(policy_elem)
        # end of the policy, clear the dictionary and loop next one
        policy_elem = {}
    # after consolidate the sheet, result in policy_list
    returnList = []
    for dict in policy_list:
        returnList.append(dict[key])
    logger1.info('***** {}, {}, {} -- Total {} items'.format(vdom,sheet,key,len(returnList)))
    print('***** {}, {}, {} -- Total {} items'.format(vdom,sheet,key,len(returnList)))
    logger1.info('end')
    return returnList


def flatten_list(l):
    """
        flatten List
    """
    return [y for x in l for y in x]


def remove_dup_list(l):
    """
        Remove duplicate elements from list
    """
    returnList = []
    # Iterate over the original list and for each element
    # add it to uniqueList, if its not already there.
    for elem in l:
        if elem not in returnList:
            returnList.append(elem)
    return returnList


def raw2_uniq_list(key, req_polList):

    logger1 = logger.logger().get()
    logger1.info('start: raw2_uniq_list')
    req_rawList = []
    for dict in req_polList:
        req_rawList.append(str(dict[key]).split())
    req_flatList = flatten_list(req_rawList)
    req_uniqList = remove_dup_list(req_flatList)
    logger1.debug('before remove duplicate: {}'.format(req_flatList))
    logger1.debug('after remove duplicate: {}'.format(req_uniqList))
    logger1.info('*****{} obj, before remove duplicate: {} in xls, after remove duplicate: {}'.format(key,len(req_flatList),len(req_uniqList)))

    return req_uniqList


def analyze_bas_mis(req_key, bas_List, req_uniqList):

    logger1 = logger.logger().get()
    logger1.info('start: analyze_bas_mis_obj')

    missingObjList = []
    for req_item in req_uniqList:
        if req_item in bas_List:
            continue
        else:
            missingObjList.append(req_item)
            print 'Item not in baseline: {}'.format(req_item)
    logger1.debug('baseline obj: {}'.format(bas_List))
    logger1.debug('reqiremt obj: {}'.format(req_uniqList))
    logger1.info('No. of baseline {} obj: {} - No. of req obj: {}'.format(req_key, len(bas_List),len(req_uniqList)))
    logger1.info('***** No. of Missing obj: {}'.format(len(missingObjList)))
    return missingObjList


def start():

    # define logger
    logger1 = logger.logger().get()
    logger1.info('start script: '+__name__)

    # info1/baseline, xls
    bas_conf = 'CPFW03_20190323_0454.conf.xlsx'
    bas_conf_sheet = '07policy'

    # info2/gen conf, xls requirement
    req_conf = 'CP03CASH2_20190328a.xlsx'
    req_conf_sheet = 'Policy'
    # define the vdom name
    vdom = 'CP03OTPC'

    print('************************************************')
    print('*** baseline conf: {}'.format(bas_conf))
    print('*** requiremt xls: {}'.format(req_conf))
    print('*** doing vdom: {}'.format(vdom))
    print('************************************************')
    print('************ task for baseline *****************')
    # 1/baseline, xls to List for checking
    bas_intList = xls2_obj_list(bas_conf, '01int', vdom, 'name')
    bas_addList = xls2_obj_list(bas_conf, '04addr', vdom, 'name')
    bas_serList = xls2_obj_list(bas_conf, '06service', vdom, 'name')

    print('************ task for gen conf *****************')
    # 2/gen conf, xls requirement to txt
    req_polList, keys = xls2_policy_list(req_conf, req_conf_sheet, vdom)
    gen_conf_policy(req_polList, keys, vdom)

    print('************ task for find missing object *****************')
    # 3/analyze baseline missing obj
    print '*********************'
    req_key = 'service'
    print '*** task for ' + req_key
    req_uniqList = raw2_uniq_list(req_key, req_polList)
    bas_missList = analyze_bas_mis(req_key, bas_serList, req_uniqList)
    print bas_missList

    print '*********************'
    req_key = 'srcaddr'
    print '*** task for ' + req_key
    req_uniqList_srcaddr = raw2_uniq_list(req_key, req_polList)

    print '*********************'
    req_key = 'dstaddr'
    print '*** task for ' + req_key
    req_uniqList_dstaddr = raw2_uniq_list(req_key, req_polList)

    print '*********************'
    req_key = 'srcaddr_and_dstaddr'
    print '*** task for ' + req_key
    addrList = req_uniqList_srcaddr + req_uniqList_dstaddr
    addrList = remove_dup_list(addrList)
    bas_missList = analyze_bas_mis(req_key, bas_serList, addrList)
    print bas_missList

    print '*********************'
    req_key = 'srcintf'
    print '*** task for ' + req_key
    req_uniqList_srcintf = raw2_uniq_list(req_key, req_polList)

    print '*********************'
    req_key = 'dstintf'
    print '*** task for ' + req_key
    req_uniqList_dstintf = raw2_uniq_list(req_key, req_polList)

    print '*********************'
    req_key = 'srcintf_and_dstintf'
    print '*** task for ' + req_key
    intfList = req_uniqList_srcintf + req_uniqList_dstintf
    intfList = remove_dup_list(intfList)
    bas_missList = analyze_bas_mis(req_key, bas_serList, intfList)
    print bas_missList

    logger1.info('end: '+__name__)


if __name__ == "__main__":
    start()
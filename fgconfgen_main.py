#!/usr/bin/env python
# by kkyick2
# import pkg
import os
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
                # logger1.debug('cell({}, {}): (key|val) is: {} | {}'.format(str(x),str(y),str(policy_key),str(cell_obj.value)))
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
    # output file name
    outfile = vdom + '_policy.txt'

    logger1 = logger.logger().get()
    print('start: gen_conf_policy: (vdom): {}, Total item to gen is {}'.format(vdom,len(dictList)))
    logger1.info('start: gen_conf_policy: (vdom): {}, Total item to gen is {}'.format(vdom,len(dictList)))
    print('***** output file {}'.format(outfile))
    if 'vdom' in keys:
        logger1.info('***** requirement xls vdom is: ' + str(dictList[0]['vdom']))
    else:
        logger1.info('***** requirement xls do not have vdom, skip vdom key')

    if dictList and keys:
        logger1.info('gen config to txt')
        with open(outfile, 'wb') as outF:
            # First section [config vdom, edit <vdom>, config firewall policy]
            write_row(outF, 'config vdom' + NEXTLINE)
            write_row(outF, 'edit ' + vdom + NEXTLINE)
            write_row(outF, 'config firewall policy' + NEXTLINE)

            # loop for each policy in dictionary format, {'vdom:'root,'id':'999,'ippool':None,'uuid':'948a...' .}
            for policydict in dictList:
                # loop for each key to follow the order
                for key in keys:
                    if key in policydict.keys() and policydict[key]:
                        # skip vdom column in xlsx
                        if key == 'vdom':
                            continue
                        elif key == 'uuid':
                            continue
                        elif key == 'Config Change Date':
                            continue
                        # edit <id>
                        elif key == 'id':
                            write_row(outF, 'edit ' + str(policydict[key]) + NEXTLINE)
                        elif key == 'name' or key == 'comments':
                            write_row(outF, 'set ' + str(key) + ' "' + str(policydict[key]) + '"'+ NEXTLINE)
                        elif key == 'srcaddr' or key == 'dstaddr' or key == 'service':
                            # remove object's next line and space from xls
                            obj_list = str(policydict[key]).split()
                            string = ""
                            for obj in obj_list:
                                if string is "":
                                    string = '"' + obj + '"'
                                else:
                                    string = string + ' "' + obj + '"'
                            write_row(outF, 'set ' + str(key) + ' ' + string + ''+ NEXTLINE)
                        else:
                            write_row(outF, 'set ' + str(key) + ' "' + str(policydict[key]) + '"'+ NEXTLINE)
                # End of each policy [next]
                write_row(outF, "next" + NEXTLINE)
                write_row(outF, NEXTLINE)
            # End section [end]
            write_row(outF, "end" + NEXTLINE)
    logger1.info('end')
    return


def gen_conf_service(list, vdom):

    # output file name
    outfile = vdom + '_service.txt'

    logger1 = logger.logger().get()
    print('start: gen_conf_service: (vdom): {}, Total item to gen is {}'.format(vdom,len(list)))
    logger1.info('start: gen_conf_service: (vdom): {}, Total item to gen is {}'.format(vdom,len(list)))
    print('***** output file {}'.format(outfile))

    with open(outfile, 'wb') as outF:
        # First section [config vdom, edit <vdom>]
        write_row(outF, 'config vdom' + NEXTLINE)
        write_row(outF, 'edit ' + vdom + NEXTLINE)
        write_row(outF, 'config firewall service category' + NEXTLINE)
        write_row(outF, 'edit "HKEX_USE"' + NEXTLINE)
        write_row(outF, 'next' + NEXTLINE)
        write_row(outF, 'end' + NEXTLINE)
        write_row(outF, NEXTLINE)
        write_row(outF, 'config firewall service custom' + NEXTLINE)

        # loop for each item
        for item in list:
            write_row(outF, 'edit "' + str(item) + '"'+ NEXTLINE)
            write_row(outF, 'set category "HKEX_USE"' + NEXTLINE)
            if item.startswith('tcp/') or item.startswith('TCP/'):
                #print 'tcp'
                write_row(outF, 'set tcp-portrange ' + item.split('/')[1] + NEXTLINE)
                write_row(outF, 'next' + NEXTLINE)
                write_row(outF, NEXTLINE)
            elif item.startswith('udp/') or item.startswith('UDP/'):
                #print 'udp'
                write_row(outF, 'set udp-portrange ' + item.split('/')[1] + NEXTLINE)
                write_row(outF, 'next' + NEXTLINE)
                write_row(outF, NEXTLINE)
            else:
                print item + ' <-- !! Not tcp/udp object, need manuel edit'
                write_row(outF, 'set !!!!! need manuel edit !!!!!!! ' + NEXTLINE)
                write_row(outF, 'next' + NEXTLINE)
                write_row(outF, NEXTLINE)
        write_row(outF, 'end' + NEXTLINE)
    logger1.info('end')
    return


def gen_conf_address(list, vdom):

    # output file name
    outfile = vdom + '_address.txt'

    logger1 = logger.logger().get()
    print('start: gen_conf_address: (vdom): {}, Total item to gen is {}'.format(vdom,len(list)))
    logger1.info('start: gen_conf_address: (vdom): {}, Total item to gen is {}'.format(vdom,len(list)))
    print('***** output file {}'.format(outfile))

    logger1.info('end')
    return


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
    logger1.info('***** Total: {} items in {} {}'.format(len(returnList),vdom,sheet))
    print('***** Total: {} items in {} {}'.format(len(returnList),vdom,sheet))
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
    logger1.info('end')
    return req_uniqList


def analyze_bas_mis(req_key, bas_List, req_uniqList):

    logger1 = logger.logger().get()
    print('--- [' + req_key + '] ----------------------------------------------------------')
    print('start: analyze_bas_mis_obj: (key,bas_len,req_len) is ({},{},{})'.format(req_key,len(bas_List),len(req_uniqList)))
    logger1.info('start: analyze_bas_mis_obj: (key,bas_len,req_len) is ({},{},{})'.format(req_key,len(bas_List),len(req_uniqList)))

    missingObjList = []
    for req_item in req_uniqList:
        if req_item in bas_List:
            continue
        else:
            missingObjList.append(req_item)
            print 'Item not in baseline: {}'.format(req_item)

    # analyze result
    logger1.debug('baseline obj: {}'.format(bas_List))
    logger1.debug('reqiremt obj: {}'.format(req_uniqList))
    logger1.info('*** No of obj in (key,baseline,req,missing) is ({},{},{},{})'.format(req_key,len(bas_List),len(req_uniqList),len(missingObjList)))
    logger1.info('end')
    # print('*** baseline obj: {}'.format(bas_List))
    # print('*** reqiremt obj: {}'.format(req_uniqList))
    print('*** No of obj in (key,baseline,req,missing) is ({},{},{},{})'.format(req_key,len(bas_List),len(req_uniqList),len(missingObjList)))
    print('-------------------------------------------------------------------------------')
    print('')
    return missingObjList


def start():

    # define logger
    logger1 = logger.logger().get()
    logger1.info('start script: '+__name__)

    # info1/baseline, xls
    bas_conf = 'CTFW03_20190324_0727.conf.xlsx'
    bas_conf_sheet = '07policy'

    # info2/gen conf, xls requirement, vdom name
    req_conf = 'CT03CASH2_20190328a.xlsx'
    req_conf_sheet = 'Policy'
    vdom = 'CT03CASH2'

    # define full path
    bas_conf_path = os.path.join(conf.FGCONFGEN_BAS_PATH, bas_conf)
    req_conf_path = os.path.join(conf.FGCONFGEN_REQ_PATH, req_conf)

    print('======================= script arg input ==================================')
    print('=== baseline conf: {}'.format(bas_conf))
    print('=== requiremt xls: {}'.format(req_conf))
    print('=== requiremt tab: {}'.format(req_conf_sheet))
    print('=== doing vdom: {}'.format(vdom))
    print('===========================================================================')
    print('')

    print('====================== 1/Task: baseline check =============================')
    # 1/baseline, xls to List for checking
    bas_intList = xls2_obj_list(bas_conf_path, '01int', vdom, 'name')
    bas_zonList = xls2_obj_list(bas_conf_path, '02zone', vdom, 'name')
    bas_addList = xls2_obj_list(bas_conf_path, '04addr', vdom, 'name')
    bas_serList = xls2_obj_list(bas_conf_path, '06service', vdom, 'name')
    print('')

    print('=================== 2/Task: gen policy conf ===============================')
    # 2/gen conf, xls requirement to txt
    req_polList, keys = xls2_policy_list(req_conf_path, req_conf_sheet, vdom)
    gen_conf_policy(req_polList, keys, vdom)
    print('')

    print('=================== 3/Task: find missing object in baseline ===============')
    # 3/analyze baseline missing obj
    req_key = 'service'
    req_uniqList = raw2_uniq_list(req_key, req_polList)
    missing_service = analyze_bas_mis(req_key, bas_serList, req_uniqList)

    req_key = 'srcaddr'
    req_uniqList_srcaddr = raw2_uniq_list(req_key, req_polList)
    req_key = 'dstaddr'
    req_uniqList_dstaddr = raw2_uniq_list(req_key, req_polList)
    req_key = 'srcaddr_and_dstaddr'
    addrList = req_uniqList_srcaddr + req_uniqList_dstaddr
    addrList = remove_dup_list(addrList)
    missing_address = analyze_bas_mis(req_key, bas_addList, addrList)

    req_key = 'srcintf'
    req_uniqList_srcintf = raw2_uniq_list(req_key, req_polList)
    req_key = 'dstintf'
    req_uniqList_dstintf = raw2_uniq_list(req_key, req_polList)
    req_key = 'zone'
    intfList = req_uniqList_srcintf + req_uniqList_dstintf
    intfList = remove_dup_list(intfList)
    missing_zone = analyze_bas_mis(req_key, bas_zonList, intfList)
    print('')

    print('=================== 4/Task: gen missing service conf ====================')
    gen_conf_service(missing_service,vdom)
    print('')

    print('=================== 5/Task: gen missing address conf ====================')
    gen_conf_address(missing_address,vdom)
    print('')

    logger1.info('end: '+__name__)


if __name__ == "__main__":
    start()
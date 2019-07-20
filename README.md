# 201903_pyvdomcutter

## requirement:
python2.7
xlsxwriter

## usage - put xls to folder
1. put "fgt conf" to folder "fg2xls_input"
2. put "requirement xlsx" to folder "fgconfgen_req"
3. Remark1: requirement xlsx should have below column
{id,name,srcintf,dstintf,srcaddr,dstaddr,action,schedule,service,utm-status,logtraffic,ips-sensor,nat,ippool,poolname}
4. Remark2: reqirement xlsx should have sheet name "Policy"

## fg2xls.py -> this script will gen a baseline xlsx
1. execute fg2xls_main.py
2. (csv,xlsx)  in folder "fg2xls_output"
3. (xlsx) in folder "fgconfgen_baseline"

## fg2confgen.py ->this script will find missing objects and gen conf
1. set arg in main 1/baseline xlsx, 2/requirement xlsx, 3/vdom
2. execute fgconfgen_main.py
3. (txt) policy config in root folder
4. (txt) missing object config in root folder
5. Remark1: cmd will show missing object {service,address,zone,route}
6. Remark2: txt conf gen {policy,service,address}

## 
- kkyick2


## update
- 20190325
- 20190330
- 20190409
- 20190411
- 20190416
- 20190425
- 20190523 add duplicate policy name check
- 20190720 testing python2.7 and python3.7 compatibility

# 201903_pyvdomcutter

## requirement:
- python2.7.x

- python3.7.x

- xlsxwriter

## usage1 - Fortigate config to excel
### Step1: input
1. put "fgt conf" to folder "fg2xls_input"
2. run fg2xls.py
3. Per vdom conf and excel output in folder "fg2xls_output"
4. excel output in folder "fgconfgen_baseline"

## usage2 - Generate fortigate config base on input xls
### Step1: put config, xls to folders
1. put "fgt conf" to folder "fg2xls_input"
2. put "requirement xlsx" to folder "fgconfgen_req"
3. Remark1: requirement xlsx should have below column
{id,name,srcintf,dstintf,srcaddr,dstaddr,action,schedule,service,utm-status,logtraffic,ips-sensor,nat,ippool,poolname}
4. Remark2: reqirement xlsx should have sheet name "Policy"

### Step2: fg2xls.py -> this script will gen a baseline xlsx
1. execute fg2xls_main.py
2. (csv,xlsx)  in folder "fg2xls_output"
3. (xlsx) in folder "fgconfgen_baseline"

### Step3: fg2confgen.py ->this script will find missing objects and gen conf
1. set arg in main 1/baseline xlsx, 2/requirement xlsx, 3/vdom
2. execute fgconfgen_main.py
3. (txt) policy config in root folder
4. (txt) missing object config in root folder
5. Remark1: cmd will show missing object {service,address,zone,route}
6. Remark2: txt conf gen {policy,service,address}

## 
- kkyick2


## update
- 20190523 add duplicate policy name check
- 20190722 tested python2.7.13 compatibility
- 20191205 tested python3.7.5 compatibility
- 20200723 tested sdn3 requirement, need edit ips profile, int-asso on addr obj comment out
- 20200909 update vdomcutter.py , tested config-version=FG1K5D-6.0.9, config-version=FG1K5D-5.04, both version ok
- 20210109 update fgconfgen_main.py , add gen_route, gen_interface function, not tested yet 
- 20210629 update vdomcutter.py , add split global function
- 20210629 update fg2csv.py , add fg2csv_mcaddr.py, fg2csv_mcpolicy.py

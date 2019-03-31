__author__ = 'ykk'

import os
import fg2csv_addr
import fg2csv_addrgrp
import fg2csv_interface
import fg2csv_ippool
import fg2csv_policy
import fg2csv_route
import fg2csv_service
import fg2csv_vip
import fg2csv_zone


def fg2csv(infile, outdir):
    """
        fg2xls_input a fg config and convent the sections in csv
        @param infile : fg2xls_input filename of the fg config
        @param outdir : fg2xls_output folder: full path for the fg2xls_output folder
        @rtype: na
    """
    fg2csv_interface.main2(infile, os.path.join(outdir, '01int.csv'), False, False)
    fg2csv_zone.main2(infile, os.path.join(outdir, '02zone.csv'), False, False)
    fg2csv_route.main2(infile, os.path.join(outdir, '03route.csv'), False, False)
    fg2csv_addr.main2(infile, os.path.join(outdir, '04addr.csv'), False, False)
    fg2csv_addrgrp.main2(infile, os.path.join(outdir, '05addrgrp.csv'), False, False)
    fg2csv_service.main2(infile, os.path.join(outdir, '06service.csv'), False, False)
    fg2csv_policy.main2(infile, os.path.join(outdir, '07policy.csv'), False, False)
    fg2csv_ippool.main2(infile, os.path.join(outdir, '08ippool.csv'), False, False)
    fg2csv_vip.main2(infile, os.path.join(outdir, '09vip.csv'), False, False)

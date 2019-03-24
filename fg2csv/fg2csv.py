__author__ = 'ykk'

import os
import fg2csv_policy
import fg2csv_route
import fg2csv_addr
import fg2csv_addrgrp
import fg2csv_service
import fg2csv_interface
import fg2csv_zone


def fg2csv(infile, outdir):
    """
        input a fg config and convent the sections in csv
        @param infile : input filename of the fg config
        @param outdir : output folder: full path for the output folder
        @rtype: na
    """
    fg2csv_interface.main2(infile, os.path.join(outdir, '1int.csv'), False, False)
    fg2csv_zone.main2(infile, os.path.join(outdir, '2zone.csv'), False, False)
    fg2csv_route.main2(infile, os.path.join(outdir, '3route.csv'), False, False)
    fg2csv_addr.main2(infile, os.path.join(outdir, '4addr.csv'), False, False)
    fg2csv_addrgrp.main2(infile, os.path.join(outdir, '5addrgrp.csv'), False, False)
    fg2csv_service.main2(infile, os.path.join(outdir, '6service.csv'), False, False)
    fg2csv_policy.main2(infile, os.path.join(outdir, '7policy.csv'), False, False)

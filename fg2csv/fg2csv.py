__author__ = 'ykk'

import os
from . import fg2csv_addr
from . import fg2csv_addrgrp
from . import fg2csv_interface
from . import fg2csv_ippool
from . import fg2csv_policy
from . import fg2csv_route
from . import fg2csv_service
from . import fg2csv_vip
from . import fg2csv_zone
from . import fg2csv_mcaddr
from . import fg2csv_mcpolicy
from . import fg2csv_dospolicy


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

    fg2csv_mcaddr.main2(infile, os.path.join(outdir, '10mcaddr.csv'), False, False)
    fg2csv_mcpolicy.main2(infile, os.path.join(outdir, '11mcpolicy.csv'), False, False)
    fg2csv_dospolicy.main2(infile, os.path.join(outdir, '12dospolicy.csv'), False, False)

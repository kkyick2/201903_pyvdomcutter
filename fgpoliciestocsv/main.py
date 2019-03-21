__author__ = 'ykk'

import fgpoliciestocsv

option = {
    'output_file': 'out.csv',
    'skip_header': False,
    'newline': False,
    'input_file': 'CT01HSN.txt',
}
fgpoliciestocsv.main2('CT01HSN.txt','out.csv',False,False)
#!/usr/bin/env python
# by kkyick2
import csv, os
import xlsxwriter

# set encoding to utf8
import importlib
import sys


if sys.version[0] == '2':
    # if python2.7
    reload(sys)
    sys.setdefaultencoding("utf-8")
elif sys.version[0] == '3':
    # if python3
    importlib.reload(sys)


def csv2xlsx(filename, indir, outdir):
    """
        Generate a multi worksheet xlsx file from a folder contain csv files
        @param filename : filename of the config for fg2xls_output use
        @param indir : fg2xls_input folder: full path of the csv contained folder
        @param outdir : fg2xls_output folder: full path for xlxs fg2xls_output folder
        @rtype: na
    """
    csv_folder = indir
    xls_folder = outdir
    return_xls_path = os.path.join(xls_folder, filename + '.xlsx')
    workbook = xlsxwriter.Workbook(return_xls_path)

    for sheet in os.listdir(csv_folder):
        if sheet.endswith('.csv'):
            worksheet = workbook.add_worksheet(sheet[:-4])
            with open(csv_folder +"/" + sheet, 'r') as f:
                reader = csv.reader(f)
                for r, row in enumerate(reader):
                    for c, col in enumerate(row):
                        worksheet.write(r, c, col)
            worksheet.autofilter('A1:Z1')
    workbook.close()
    return return_xls_path


if __name__ == "__main__":
    csv2xlsx("test/", "test/", 'out.xlsx')
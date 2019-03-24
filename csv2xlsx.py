#!/usr/bin/env python
# by kkyick2
import csv, os
import xlsxwriter


def csv2xlsx(indir, outdir, outfname):
    """
        Generate a multi worksheet xlsx file from a folder contain csv files
        @param indir : input folder: full path of the csv contained folder
        @param outdir : output folder: full path for xlxs output folder
        @param outfname : filename of the xlsx
        @rtype: na
    """
    csv_folder = indir
    xls_folder = outdir
    workbook = xlsxwriter.Workbook(os.path.join(xls_folder, outfname + '.xlsx'))

    for sheet in os.listdir(csv_folder):
        if sheet.endswith('.csv'):
            worksheet = workbook.add_worksheet(sheet[:-4])
            with open(csv_folder +"/" + sheet, 'rb') as f:
                reader = csv.reader(f)
                for r, row in enumerate(reader):
                    for c, col in enumerate(row):
                        worksheet.write(r, c, col)
            worksheet.autofilter('A1:Z1')
    workbook.close()
    return


if __name__ == "__main__":
    csv2xlsx("test/", "test/", 'out.xlsx')
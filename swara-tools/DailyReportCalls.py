import os, sys
sys.path.append("../lib")
from livdatmoblibIN import *
from livdatreports import *

if __name__=="__main__":
    dr=DailyReport()
    dr.filldates(datetime(2012,7,1),datetime(2013,3,31))
    circles=CSVFile()
    circles.importfile("/home/mojoarjun/CSV/HIVOSCIRCLES.csv")
    for row in circles.matrix:
        dr.colnames=dr.colnames + [row["TELECOM CIRCLE"]]
    dr.colnames=dr.colnames+["Total"]
    print dr.colnames
    dr.fillzeros()
    
    for row in dr.matrix:
        curfile=CSVFile()
        curfile.importfile("/home/mojoarjun/CSV/HIVOSDAILYCALLLOGS/Calls-%s.csv" %row["DATE"])
        for innerrow in curfile.matrix:
            row['Total']=row['Total']+1
            row[innerrow["TELECOM CIRCLE"]]=row[innerrow["TELECOM CIRCLE"]]+1
    dr.exportfile("/home/mojoarjun/CSV/HivosDailyReport.csv")

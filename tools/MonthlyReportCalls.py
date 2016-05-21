import os, sys
sys.path.append("../lib")
from livdatmoblibIN import *
from livdatreports import *
from datetime import date
if __name__=="__main__":
    mr=MonthlyReport()
    mr.filldates(date(2012,7,1),date(2013,3,31))
    circles=CSVFile()
    circles.importfile("/home/mojoarjun/CSV/HIVOSCIRCLES.csv")
    for row in circles.matrix:
        mr.colnames=mr.colnames + [row["TELECOM CIRCLE"]]
    mr.colnames=mr.colnames+["Total"]
    print mr.colnames
    mr.fillzeros()
    
    for row in mr.matrix:
        curfile=CSVFile()
        curfile.importfile("/home/mojoarjun/CSV/HIVOSMONTHLYCALLLOGS/Calls-%s.csv" %row["MONTH"])
        for innerrow in curfile.matrix:
            row['Total']=row['Total']+1
            row[innerrow["TELECOM CIRCLE"]]=row[innerrow["TELECOM CIRCLE"]]+1
    mr.exportfile("/home/mojoarjun/CSV/HivosMonthlyCallReport.csv")

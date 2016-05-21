import os, sys
sys.path.append("../lib")
from livdatmoblibIN import *
from livdatreports import *
from datetime import date
if __name__=="__main__":
    mr=MonthlyReport()
    mr.filldates(date(2012,7,1),date(2013,3,31))
    c=CSVFile()
    c.importfile("/home/mojoarjun/CSV/HIVOSCALLLOG-CIRCLE.CSV")
    os.system("mkdir /home/mojoarjun/CSV/HIVOSMONTHLYCALLLOGS")
    for row in mr.matrix:
        os.system("echo 'user,timeOfCall,id,TELECOM CIRCLE' >  /home/mojoarjun/CSV/HIVOSMONTHLYCALLLOGS/Calls-%s.csv" %(row['MONTH']))
        os.system("cat /home/mojoarjun/CSV/HIVOSCALLLOG-CIRCLE.CSV | grep %s >>  /home/mojoarjun/CSV/HIVOSMONTHLYCALLLOGS/Calls-%s.csv" %(row['MONTH'],row['MONTH']))

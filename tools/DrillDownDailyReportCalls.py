import os, sys
sys.path.append("../lib")
from livdatmoblibIN import *
from livdatreports import *

if __name__=="__main__":
    dr=DailyReport()
    dr.filldates(datetime(2012,7,1),datetime(2013,3,31))
    c=CSVFile()
    c.importfile("/home/mojoarjun/CSV/HIVOSCALLLOG-CIRCLE.CSV")
    os.system("mkdir /home/mojoarjun/CSV/HIVOSDAILYCALLLOGS")
    for row in dr.matrix:
        os.system("echo 'user,timeOfCall,id,TELECOM CIRCLE' >  /home/mojoarjun/CSV/HIVOSDAILYCALLLOGS/Calls-%s.csv" %(row['DATE']))
        os.system("cat /home/mojoarjun/CSV/HIVOSCALLLOG-CIRCLE.CSV | grep %s >>  /home/mojoarjun/CSV/HIVOSDAILYCALLLOGS/Calls-%s.csv" %(row['DATE'],row['DATE']))

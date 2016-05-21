import os, sys
sys.path.append("../lib")
from livdatmoblibIN import *
from livdatreports import *
from datetime import date
if __name__=="__main__":
    f=MobileNumberList()
    f.importfile("/home/mojoarjun/CSV/HIVOSPOSTLOG.CSV")
    p=f.add_circle("user")
    p.exportfile("/home/mojoarjun/CSV/HIVOSPOSTLOG-CIRCLES.CSV")
    

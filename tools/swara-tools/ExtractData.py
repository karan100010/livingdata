import os, sys
sys.path.append("../lib")
from livdatmoblibIN import *

if __name__=="__main__":
    c=MobileNumberList()
    c.importfile("/home/mojoarjun/CSV/HIVOSCALLLOG.CSV")
    t=c.add_circle("user")
    t.exportfile("/home/mojoarjun/CSV/HIVOSCALLLOG-CIRCLE.CSV")
    


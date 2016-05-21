import sys,os,json
import csv
sys.path.append("../lib")
from livdatcsvlib import *
from livdatmaplib import *
if __name__=="__main__":
    csv=CSVFile()
    csv.importfile("/home/mojoarjun/CSV/loctest.csv")
    csv2=csv.exportcols(["LOCATION"])
    jsonop= json.dumps(csv2, cls=CSVJSONEncoder, indent=4, separators=(",",":"))
    for row in csv2.matrix:
        print row['LOCATION']
    print jsonop


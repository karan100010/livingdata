import os,sys
sys.path.append("../lib")
from livdatcsvlib import *
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
class DailyReport(CSVFile):
    def __init__(self):
        self.matrix=[]
        self.filename=""
        self.colnames=["DATE"]
        self.idfield="DATE"
    
    def filldates(self,startdate,enddate):
        self.startdate=startdate
        self.enddate=enddate
        while startdate<=enddate:
            dictionary={}
            dictionary["DATE"]=startdate.strftime("%Y-%m-%d")
            startdate=startdate+timedelta(days=1)
            self.matrix.append(dictionary)
    def fillzeros(self):
       for row in self.matrix:
           for col in self.colnames:
               if col!="DATE":
                   row[col]=0

class MonthlyReport(CSVFile):
    def __init__(self):
        self.matrix=[]
        self.filename=""
        self.colnames=["MONTH"]
        self.idfield="MONTH"
    
    def filldates(self,startdate,enddate):
        self.startdate=startdate
        self.enddate=enddate
        while startdate<=enddate:
            dictionary={}
            dictionary["MONTH"]=startdate.strftime("%Y-%m")
            print startdate
            startdate=startdate+relativedelta(months=+1)
            self.matrix.append(dictionary)
    def fillzeros(self):
       for row in self.matrix:
           for col in self.colnames:
               if col!="MONTH":
                   row[col]=0

import os,sys, datetime
from dateutil import relativedelta
sys.path.append("/opt/livingdata/lib")
from livdattable import *
from xlutils.copy import copy
class DataPoint:
	def __init__(self):
		self.timestamp=None
		self.value=None
		self.source=None
class GSMSubfigure(DataPoint):
	def __init__(self):
		DataPoint.__init__(self)
		self.circlecat=None
		self.circle=None


def getmonthfromfilename(filename):
	monthstr=filename.split("-")[len(filename.split("-"))-1].split(".")[0]
	return monthstr

def getqedate(qname):
    qemonth=qname.split("-")[1]
    qedate=datetime.datetime.strptime(qemonth,"%b%y")+relativedelta.relativedelta(months=1)-relativedelta.relativedelta(days=1)
    return qedate.strftime("%Y-%m-%d")
    
if __name__=="__main__":
	t=importExcelFile("/home/swara/ARPUSAPR08-SEP15.xls")
	p=Table()
	p.colnames=['QEDATE','CIRCLE','OPERATOR','QREV']
	matrix=[]
	for sheet in t:
		for row in sheet.matrix:
			for col in sheet.colnames:
				dictionary={}
				if row['OPERATOR']!="" and row['CIRCLE']!="":
					dictionary['OPERATOR']=row['OPERATOR']
					dictionary['CIRCLE']=row['CIRCLE']
					if "REV" in col:
						dictionary['QEDATE']=getqedate(col)
						dictionary['QREV']=row[col]
						matrix.append(dictionary)
				else:
					print row
	p.matrix=matrix
	p.exportfile("output.csv")

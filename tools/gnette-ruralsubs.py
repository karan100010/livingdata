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


    
if __name__=="__main__":
	#t=importExcelFile("/home/swara/RURAL08-15.xls")
	sheet=Table()
	sheet.importfile("/home/swara/TT.csv")
	
	p=Table()
	p.colnames=['DATE','CIRCLECAT','CIRCLE','OPERATOR','SUBSRURAL']
	matrix=[]
	#for sheet in t:
	for row in sheet.matrix:
		for col in sheet.colnames:
			dictionary={}
			if row['OPERATOR']!="0" and row['CIRCLE']!="0":
				dictionary['OPERATOR']=row['OPERATOR']
				dictionary['CIRCLE']=row['CIRCLE']
				dictionary['CIRCLECAT']=row['CIRCLECAT']
				if col not in ['CIRCLECAT','CIRCLE','OPERATOR']:
					#print col
					dictionary['DATE']=col
					print row[col]
					dictionary['SUBSRURAL']=int(row[col].replace(",",""))
					matrix.append(dictionary)
			else:
				print row
	p.matrix=matrix
	p.exportfile("output.csv")

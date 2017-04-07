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
	alldatapoints=Table()
	alldatapoints.colnames=['DATE','CIRCLECAT','CIRCLE','OPERATOR','SUBS']
	
	files=os.popen("ls ~/*.xls").read().strip().split("\n")
	for filename in files:
		wb=xlrd.open_workbook(filename,encoding_override='utf-8')
		workbook=copy(wb)
		firstsheet=workbook.get_sheet(0)
		firstsheet.write(0,0,"CIRCLECAT")
		workbook.save(filename)
		p=importExcelFile(filename)
		datapoints=p[0]
		datapoints.removeblankrows()
		thismonth=None
		thismonthts=None
		colnamets1=None
		colnamets=None
		filenamets=datetime.datetime.strptime(getmonthfromfilename(filename),"%b%y")
		for colname in datapoints.colnames:
			oldcolname=colname
			colname=colname.replace("April","Apr")
			colname=colname.replace("August","Aug")
			colname=colname.replace("March","Mar")
			colname=colname.replace("June","Jun")
			colname=colname.replace("July","Jul")
			colname=colname.replace("September","Sep")
			colname=colname.replace("October","Oct")
			colname=colname.replace("November","Nov")
			colname=colname.replace("December","Dec")
			colname=colname.replace("January","Jan")
			colname=colname.replace("February","Feb")
			if "'0" in colname:
				colname=colname.replace("'0","'200")
			if "'1" in colname:
				colname=colname.replace("'1","'201")
			colname=colname.lstrip().rstrip()
			#print oldcolname, colname
			try:
				colnamets=datetime.datetime.strptime(colname.replace("TTD","").replace("-","").lstrip().rstrip(),"%b\'%Y")
			except:
				continue
		
			#print filenamets,colnamets
			if filenamets==colnamets:
				thismonth=oldcolname
				thismonthts=filenamets+relativedelta.relativedelta(months=1)-relativedelta.relativedelta(days=1)
		#print filename,datapoints.colnames, getmonthfromfilename(filename), thismonth
		if thismonth==None:
			print filename,colname
			break
		thiscat=None
		lastcat=None
		thiscircle=None
		lastcircle=None
		circlelist=[]
		circlecatlist=[]
		for row in datapoints.matrix:
			if "NB" in row['CIRCLECAT'].lstrip().rstrip()=="":
				continue
			else:
				if row['CIRCLECAT'].lstrip().rstrip()=="" or row['CIRCLECAT']==None:
					thiscat=lastcat
					row['CIRCLECAT']=thiscat
				else:
					thiscat=row['CIRCLECAT'].lstrip().rstrip()
					circlecatlist.append(thiscat)
				print thiscat
				lastcat=thiscat
			if row['City/Circle'].lstrip().rstrip()=="":
					thiscircle=lastcircle
					row['City/Circle']=thiscircle
			else:
				thiscircle=row['City/Circle'].lstrip().rstrip()
				circlelist.append(thiscircle)
			print thiscircle
			lastcircle=thiscircle
		print set(circlelist),set(circlecatlist)
		cleandatapoints=datapoints.exportcols(['CIRCLECAT','City/Circle','Operators',thismonth])
	
		for row in cleandatapoints.matrix:
			if "All" not in str(row['CIRCLECAT']).lstrip().rstrip() and str(row['Operators']).lstrip().rstrip()!='' and str(row[thismonth]).lstrip().rstrip()!='NA' and str(row[thismonth]).lstrip().rstrip()!='' and row['CIRCLECAT'] != None:
				dictionary={}
				dictionary['CIRCLECAT']=row['CIRCLECAT'].lstrip().rstrip()
				dictionary['CIRCLE']=row['City/Circle'].lstrip().rstrip()
				dictionary['DATE']=thismonthts.strftime("%Y-%b-%d")
				dictionary['OPERATOR']=row['Operators'].lstrip().rstrip()	
				dictionary['SUBS']=row[thismonth]
				alldatapoints.matrix.append(dictionary)
		
			else:
				print row
	

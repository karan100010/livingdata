import os,sys, datetime
from dateutil import relativedelta
sys.path.append("/opt/livingdata/lib")
from livdattable import *
from xlutils.copy import copy
import json
opfilename="/opt/gnette-data/indiatelecomcirclebitswithcirclename.json"
circlefile="/opt/gnette-data/CIRCLEDETAIL.csv"
statecirclefile="/opt/gnette-data/STATETOCIRCLE.csv"
def lookupcirclenameforstate(state):
	t=Table()
	t.importfile(statecirclefile)
	for row in t.matrix:
		if row['NAME']==state:
			return row['CIRCLE']


def lookupdispnameforcircle(circle):
	t=Table()
	t.importfile(circlefile)
	for row in t.matrix:
		if row['CIRCLESHORTNAME']==circle:
			return row['CIRCLEDISPNAME']



def writeoutput(fldata,filename):
	f=open(filename,"w")
	f.write(json.dumps(fldata))
	f.close()

if __name__=="__main__":
	f=open("/opt/gnette-data/indiatelecomcirclebits.json","r+")
	fldata=json.load(f)
	f.close()
	names=[]
	for feature in fldata['features']:
		state= feature['properties']['NAME_1']
		print state
		circle=lookupcirclenameforstate(state)
		print circle
		circledisp=lookupdispnameforcircle(circle)
		feature['properties']['CIRCLE']=circle
		feature['properties']['CIRCLEDISPNAME']=circledisp
	writeoutput(fldata,opfilename)

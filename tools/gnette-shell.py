import os,sys, datetime
from dateutil import relativedelta
sys.path.append("/opt/livingdata/lib")
from livdattable import *
from xlutils.copy import copy
from livdatdb import *

if __name__=="__main__":
	d=Database("/home/swara/gnette.conf")
	
	query="select distinct(operator) from gsm_arpus where month(qedate)=9 and year(qedate)=2015"
	op=d.getQueryAsTable(query)
	operators_arpus=[i[0] for i in op]
	query="select distinct(operator) from gsm_subs where month(date)=9 and year(date)=2015"
	op=d.getQueryAsTable(query)
	operators_subs=[i[0] for i in op]
	query="select distinct(operator) from gsm_subs_rural where month(date)=9 and year(date)=2015"
	op=d.getQueryAsTable(query)
	operators_subsrural=[i[0] for i in op]
   	
   	
   	
   	query="select distinct(circle) from gsm_arpus where month(qedate)=9 and year(qedate)=2015"
	op=d.getQueryAsTable(query)
	circles_arpus=[i[0] for i in op]
	query="select distinct(circle) from gsm_subs where month(date)=9 and year(date)=2015"
	op=d.getQueryAsTable(query)
	circles_subs=[i[0] for i in op]
	query="select distinct(circle) from gsm_subs_rural where month(date)=9 and year(date)=2015"
	op=d.getQueryAsTable(query)
	circles_subsrural=[i[0] for i in op]
   	


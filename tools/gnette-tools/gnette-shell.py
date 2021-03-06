'''
LIVINGDATA - COLLABORATIVE DYNAMIC DATASETS (C) 2016 ARJUN VENKATRAMAN

THIS PROGRAM IS FREE SOFTWARE: YOU CAN REDISTRIBUTE IT AND/OR MODIFY IT UNDER THE 
TERMS OF THE GNU GENERAL PUBLIC LICENSE AS PUBLISHED BY THE FREE SOFTWARE FOUNDATION, 
EITHER VERSION 3 OF THE LICENSE, OR (AT YOUR OPTION) ANY LATER VERSION.

THIS PROGRAM IS DISTRIBUTED IN THE HOPE THAT IT WILL BE USEFUL, BUT WITHOUT ANY 
WARRANTY; WITHOUT EVEN THE IMPLIED WARRANTY OF MERCHANTABILITY OR FITNESS FOR A 
PARTICULAR PURPOSE. SEE THE GNU GENERAL PUBLIC LICENSE FOR MORE DETAILS.

YOU SHOULD HAVE RECEIVED A COPY OF THE GNU GENERAL PUBLIC LICENSE ALONG WITH THIS PROGRAM. 
IF NOT, SEE HTTP://WWW.GNU.ORG/LICENSES/.

'''
import os,sys, datetime
from dateutil import relativedelta
sys.path.append("../lib")
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
   	


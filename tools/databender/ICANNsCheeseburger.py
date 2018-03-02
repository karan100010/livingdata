#!/usr/bin/python
import os,sys, pandas, matplotlib
sys.path.append("/opt/livingdata/lib")
from livdatbender import *
from livdatcube import *
from sklearn.feature_extraction.text import CountVectorizer

def wordcounter():
	word_vectorizer = CountVectorizer(ngram_range=(1,3), analyzer='word')
	for year in d.cubedatadf.index:
		sparse_matrix = word_vectorizer.fit_transform(d.cubedatadf.yeardata[year].Customer)
		frequencies=sum(sparse_matrix).toarray()[0] 
		freqdf=pandas.DataFrame(frequencies, index=word_vectorizer.get_feature_names(), columns=[year]).sort_values(by=year)
		print freqdf

def show_multi_payees():
	d.logger.info("Showing customers who have more than 2 entries in a year")
	for customer in custdatadf.index:
		for year in d.cubedatadf.index:
			subcube=d.cubedatadf.yeardata[year].loc[d.cubedatadf.yeardata[year]["Customer"]==customer]
			if len(subcube)>numentries:
				d.logger.info("Year "+str(year)+" Customer : " + customer)
				print subcube[["Customer","CountryChecked","Class","ClassLong","Total"]]
				
				
def get_all_recs_for_cust(customer,cube):
    #print customer
    subcube=pandas.DataFrame(columns=cube.cubedatadf.yeardata[2012].columns)
    for year in cube.cubedatadf.index:
        yearrecs=cube.cubedatadf.yeardata[year].loc[cube.cubedatadf.yeardata[year]['Customer']==customer]
        yearrecs['Year']=year
        subcube=subcube.append(yearrecs)
    return subcube




jughead=DataBender(sys.argv[1],headless=True,launchbrowser=False)
d=DataCube(name=sys.argv[2],src="remote",remotesheetname=sys.argv[2],databender=jughead)
d.initmemory()
print "The datacube is stored in a variable named d and the bender is called jughead"	


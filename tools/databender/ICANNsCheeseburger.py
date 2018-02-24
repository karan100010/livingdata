#!/usr/bin/python
import os,sys, pandas, matplotlib
sys.path.append("/opt/livingdata/lib")
from livdatbender import *
from livdatcube import *
'''
cube={}
years=['2012',"2013","2014","2015","2016"]
for year in years:
    print year
    cube[year]=pandas.read_csv("ICANN"+year+"-totalverified.csv")
    
cubeseries=pandas.Series(cube)
cubedf=pandas.DataFrame()
cubedf['yeardata']=cubeseries

typedict={"IDN":"Internationalized Domain Names","RAR":"Registrar","RIR":"Regional Internet Registry","RYC":"ccTLD","RYG":"Registry","RYN":"Registry","SPN":"Sponsor","OTH":"Other"}

    
for year in cubedf.index:
	cubedf.yeardata[year]['ClassLong']=cubedf.yeardata[year].Class.apply(lambda p:typedict[p])
'''

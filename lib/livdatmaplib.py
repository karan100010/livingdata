import os,sys
sys.path.append("../lib")
from livdatcsvlib import *
import json,requests,urllib
from geopy import geocoders


def geocode_field_from_CSV(csv,fieldname):
  g = geocoders.GoogleV3()
	#print g.api_key
  print "Hello"
  finalcsv=CSVFile()
  finalcsv.colnames=["SEARCHKEY","LOCATION","LAT","LONG"]
  searchkeylist=[]
  for line in csv.matrix:
    searchkeylist.append(line[fieldname])
  searchkeys=set(searchkeylist)
  for searchkey in searchkeys:
    dictionary={}
    dictionary["SEARCHKEY"]=searchkey
    try:
      place, (lat, lng) = g.geocode(searchkey)
      print "Ran a geocode"
      dictionary["LOCATION"]=place
      dictionary["LAT"]=lat
      dictionary["LONG"]=lng
    except:
      print "Bad Geocode"
      dictionary["LOCATION"]=""
      dictionary["LAT"]=""
      dictionary["LONG"]=""
    finalcsv.matrix.append(dictionary)
  return finalcsv

def add_loc_lat_long(csv,fieldname):
	locfile=geocode_field_from_CSV(csv,fieldname)
	finalcsv=CSVFile()
	finalcsv.colnames=csv.colnames
	finalcsv.colnames=finalcsv.colnames+["LOCATION","LAT","LONG"]
	for row in csv.matrix:
		dictionary=row
		for loc in locfile.matrix:
			if dictionary[fieldname]==loc["SEARCHKEY"]:
				location=loc["LOCATION"]
				lat=loc["LAT"]
				lng=loc["LONG"]
		dictionary["LOCATION"]=location
		dictionary["LAT"]=lat
		dictionary["LONG"]=lng
		finalcsv.matrix.append(dictionary)
	return finalcsv
				

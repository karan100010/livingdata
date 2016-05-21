import csv
import urllib2, urllib


def getGFTQueryAsCSV(query,key):
  request_url = 'https://www.google.com/fusiontables/api/query' 
  url = "%s?%s" % (request_url, urllib.urlencode({'sql': query, 'key': key}))
  serv_req = urllib2.Request(url=url)
  serv_resp = urllib2.urlopen(serv_req)
  reader = csv.reader(serv_resp)
  return reader

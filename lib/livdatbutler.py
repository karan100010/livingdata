import os,sys
sys.path.append("/opt/SoMA/python/lib")

from libsoma import *
import pygsheets
from bs4 import BeautifulSoup

class DataButler(SoMACyborg):
	def __init__(self,*args, **kwargs):
		super(Butler,self).__init__(*args, **kwargs)
	
	def create_new_ssheet(self,title,folderid=None):
		for ssheet in self.gc.list_ssheets():
			if ssheet['name']==title:
				print "Sheet exists...try a different name"
				return None
		self.gc.create(title,parent_id=folderid)
		for ssheet in self.gc.list_ssheets():
			if ssheet['name']==title:
				print "Sheet %s created" %title
				return self.gc.open_by_key(ssheet['id'])
	
	def get_ssheet(self,title):
		for ssheet in self.gc.list_ssheets():
			if ssheet['name']==title:
				print "Sheet exists...fetching"
				return self.gc.open_by_key(ssheet['id'])
		print "Sheet does not exist...is your name correct"
		return None

	
	def get_json_feed(self,feedurl):
		return None
		


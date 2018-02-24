import os,sys,pandas
sys.path.append("/opt/SoMA/python/lib")

from libsoma import *
import pygsheets
from bs4 import BeautifulSoup

def get_as_dict(df):
    if "key" not in df.columns:
        print "Cannot do...no key column"
        return None
    if "value" not in df.columns:
        print "Cannot do...no values column"
    df.index=df.key
    dfval=df.value
    dfdict=dfval.to_dict()
    return dfdict


class DataCube(object):
	
	
	
	
	def __init__(self,src="local",localpath=None,remotesheetkey=None,remotesheetname=None,databender=None):
		# Identify the source, local or remote and init accordingly
		#If source is local - 
		self.jsonprofile={}
		if src=='local':
			if localpath==None:
				print "If source is local, a path must be provided"
				return None
			self.initlocal(localpath)
		#If source is remote
		if src=='remote':
			if remotesheetkey==None and remotesheetname==None:
				print "If source is remote, a sheet name or sheet key must be provided"
				return None
			if databender == None:
				print "If source is remote, a bender is needed"
				return None
			self.initremote(remotesheetname,remotesheetkey,databender)
		
			
		
	def show_profile(self):
		print get_color_json(self.jsonprofile)
	
	def save_profile(self):
		if "cubepath" in self.jsonprofile.keys():
			self.jsonfile=os.path.join(self.cubepath,"cube.json")
			self.set_property("jsonfile",self.jsonfile)
		else:
			print "No local path specified"
			return None
		with open(self.jsonfile,"w") as f:
			f.write(json.dumps(self.jsonprofile,indent=4,sort_keys=True))
	
	def get_property(self,propertyname):
		if propertyname in self.jsonprofile.keys():
			return self.jsonprofile[propertyname]
		else:
			return None
	
	def set_property(self,propertyname,value):
		self.jsonprofile[propertyname]=value
	
	def initlocal (self,localpath=None):
		
		if localpath==None:
			print "If source is local, a path must be provided"
			return None
		self.cubepath=localpath
		self.set_property('cubepath',self.cubepath)
		self.cubedeffilepath=os.path.join(self.cubepath,"cubedef.csv")	
		self.set_property('cubedeffilepath',self.cubedeffilepath)
		self.cubedictsfilepath=os.path.join(self.cubepath,"cubedicts.json")
		self.set_property('cubedictsfilepath',self.cubedictsfilepath)
		print "Initing local"
		if not os.path.exists(self.cubepath):
			print "Making directory",self.cubepath
			os.mkdir(self.cubepath)
			#self.df=pandas.DataFrame()
		if os.path.exists(os.path.join(self.cubepath,"cubedef.csv")):
			self.cubedef=pandas.read_csv(os.path.join(self.cubepath,"cubedef.csv"))
			self.cubedefdict=get_as_dict(self.cubedef)
		else:
			self.cubedef=pandas.DataFrame(columns=['key','value'])
			keys=pandas.Series(['index','cubename','dictionary_prefix','datasheet_prefix','columns'])
			self.cubedef.key=keys
			self.cubedef.to_csv(os.path.join(self.cubepath,"cubedef.csv"),index=False)
		
		
		self.local=True	
	
	def initremote(self,remotesheetname=None,remotesheetkey=None,databender=None):
		if remotesheetkey==None and remotesheetname==None:
			print "If source is remote, a sheet name or sheet key must be provided"
			self.remote=False
			return None
		if databender == None:
			print "If source is remote, a bender is needed"
			self.remote=False
			return None
			
		if remotesheetkey != None:
			print "We can has sheetkey", remotesheetkey
			self.cubesheetkey=remotesheetkey
			self.cubesheet=databender.get_ssheet_by_key(self.cubesheetkey)
			self.cubesheetname=self.cubesheet.title
		else:
			self.cubesheetname=remotesheetname
			self.cubesheet=databender.get_ssheet_by_name(self.cubesheetname)
			self.cubesheetkey=self.cubesheet.id
		self.set_property("cubesheetname",self.cubesheetname)
		self.set_property("cubesheetkey",self.cubesheetkey)
		self.remote=True

	def initmemory (self):
		print "Initing memory"
		self.cubedicts = {}
		

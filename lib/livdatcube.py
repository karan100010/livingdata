import os,sys,pandas
sys.path.append("/opt/SoMA/python/lib")

from libsoma import *
import pygsheets
from bs4 import BeautifulSoup

def get_worksheet_names(ssheet):
	sheetnames=[]
	for ws in ssheet.worksheets():
		sheetnames.append(ws.title)
	return sheetnames

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

def string_to_range(string):
	if "range" in string:
		rangedef=string.replace("range(","").replace(")","").split(",")
		indexrange=range(int(rangedef[0]),int(rangedef[1]))
		return indexrange
	return None
	
class DataCube(object):
	def __init__(self,src="local",localpath=None,remotesheetkey=None,remotesheetname=None,databender=None):
		# Identify the source, local or remote and init accordingly
		#If source is local - 
		self.jsonprofile={}
		self.local=False
		self.remote=False
		self.src=src
		self.set_property("local",self.local)
		self.set_property("remote",self.remote)
		self.set_property("src",self.src)
		self.cubecalcsheets={}
		
		self.cubedefdict={}
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
	
	def initlocal(self,localpath=None):
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
			print "Please enter a cube definition in the file " + os.path.join(self.cubepath,"cubedef.csv")
			
		self.local=True	
		self.set_property("local",self.local)
		
	def initremote(self,remotesheetname=None,remotesheetkey=None,databender=None):
		self.cubesheetname=remotesheetname
		self.cubesheetkey=remotesheetkey
		if self.cubesheetkey==None and self.cubesheetname==None:
			print "If source is remote, a sheet name or sheet key must be provided"
			self.remote=False
			return None
		if databender == None:
			print "If source is remote, a bender is needed"
			self.remote=False
			return None	
		
		cubesheetdict={}
		cubesheetdict['id']=self.cubesheetkey
		cubesheetdict['name']=self.cubesheetname
		cubesheetdict=databender.lookup_ssheet(cubesheetdict)
		print "Looked up sheetdict",cubesheetdict
		if cubesheetdict['id']!=None and cubesheetdict['name']==None:
			print "Specified id doesnt exist and no name specified"
			self.remote=False
			return None
		if cubesheetdict['id']==None and cubesheetdict['name'] !=None:
			print "Creating sheet..."
			databender.gc.create(title=cubesheetdict['name'])
		self.cubesheet=databender.get_ssheet(name=cubesheetdict['name'])
		self.cubesheetname=self.cubesheet.title
		self.cubesheetkey=self.cubesheet.id
		print "Initing remote"
		self.set_property("cubesheetname",self.cubesheetname)
		self.set_property("cubesheetkey",self.cubesheetkey)
		
		#print self.cubesheet.worksheets()
		try:
			self.cubedef=self.cubesheet.worksheet_by_title("cubedef").get_as_df()
			self.cubedefdict=get_as_dict(self.cubedef)
		except:
			print "Could not get cubedef....trying to create"
			try:
				self.cubesheet.add_worksheet(title="cubedef")
				self.cubedef=pandas.DataFrame(columns=['key','value'])
				keys=pandas.Series(['index','cubename','dictionary_prefix','datasheet_prefix','columns'])
				self.cubedef.key=keys
				self.cubesheet.worksheet_by_title("cubedef").set_dataframe(self.cubedef,(1,))
				print "Please enter a cube definition in the worksheet cubedef at https://docs.google.com/spreadsheets/d"+self.cubesheet.id
			except Exception as e:
				print "Could not create worksheet because", e
			
		
		self.remote=True
		self.set_property("remote",self.remote)
		
		return None
	def initmemory (self):
		print "Initing memory"
		self.build_cube()
		
	def build_cube(self):
		if self.get_property(self.src)==False:
			print "Cannot build cube, specified source is not connected, init local or remote successfully first"
			return None
		self.cubename=self.cubedefdict['cubename']
		self.set_property("cubename",self.cubename)
		self.save_profile()
		print "Prefixes"
		for key,value in self.cubedefdict.iteritems():
			if "_prefix" in key:
				print key, value
				self.set_property(key,value)
		print "Index"
		self.set_property("index",self.cubedefdict['index'])
		indexrange=string_to_range(self.cubedefdict['index'])
		print indexrange
		
		print "Columns"
		columnrange=self.cubedefdict['columns'].split(",")
		print columnrange
		self.cubedatadf=pandas.DataFrame(columns=columnrange,index=indexrange)
		print self.cubedatadf
	
	def check_cube_data(self):
		checked=True
		for i in self.cubedatadf.index:
			for col in self.cubedatadf.columns:
				datasheetname=self.get_property("datasheet_prefix")+"_"+str(i)+"_"+col
				if self.src=="local":
					datafilename=datasheetname+".csv"
					if os.path.exists(os.path.join(self.get_property("cubepath"),datafilename)):
						print datafilename + " exists...checked!"
					else:
						print datafilename + " does not exists...:(!"
						checked=False
				if self.src=="remote":
					if datasheetname in get_worksheet_names(self.cubesheet):
						print datasheetname + " exists...checked!"
					else:
						print datasheetname + " does not exists...:(!"
						checked=False
		return checked
	def load_cube_data(self):
		print self.cubedatadf
		for i in self.cubedatadf.index:
			for col in self.cubedatadf.columns:
				datasheetname=self.get_property("datasheet_prefix")+"_"+str(i)+"_"+col
				if self.src=="local":
					datafilename=datasheetname+".csv"
					if os.path.exists(os.path.join(self.get_property("cubepath"),datafilename)):
						print i,col
						self.cubedatadf[col][i]=pandas.read_csv(datafilename)
				if self.src=="remote":
					if datasheetname in get_worksheet_names(self.cubesheet):
						print i,col
						self.cubedatadf[col][i]=self.cubesheet.worksheet_by_title(datasheetname).get_as_df()
	def load_cube_calcsheets(self):
		calcsheets=[]
		if self.src=="local":
			for fn in os.listdir(self.cubepath):
				ws=fn.replace(".csv","")
				if ws.split("_")[0]==self.cubename:
					calcsheets.append(ws)
			for sheet in calcsheets:
				self.cubecalcsheets[sheet]=pandas.read_csv(os.path.join(self.cubepath,sheet+".csv"))
		if self.src=="remote":
			for ws in get_worksheet_names(self.cubesheet):
				if ws.split("_")[0]==self.cubename:
					calcsheets.append(ws)
			for sheet in calcsheets:
				self.cubecalcsheets[sheet]=self.cubesheet.worksheet_by_title(sheet).get_as_df()
	def load_cube_dicts(self):
		if self.src=="local":
			if os.path.exists(self.cubedictsfilepath):
				with open(self.cubedictsfilepath,"r") as cubedictsjson:
					self.cubedicts=json.loads(cubedictsjson.read())
			else:
				self.cubedicts={}
		if self.src=="remote":
			self.cubedicts={}
			dictsheets=[]
			for ws in get_worksheet_names(self.cubesheet):
				if ws.split("_")[0]==self.get_property("dictionary_prefix"):
					dictsheets.append(ws)
			for ws in dictsheets:
				self.cubedicts[ws]=get_as_dict(self.cubesheet.worksheet_by_title(ws).get_as_df())
		
		
	def save_local(self):
		print "Saving local"
		self.cubedef.to_csv(self.cubedeffilepath,index=False,encoding="utf8")
		with open(self.cubedictsfilepath,"w") as cubedictsjson:
			cubedictsjson.write(json.dumps(self.cubedicts))
		for i in self.cubedatadf.index:
			for col in self.cubedatadf.columns:
				self.cubedatadf[col][i].to_csv(os.path.join(self.cubepath,self.get_property("datasheet_prefix")+"_"+str(i)+"_"+col),encoding="utf8")
		for key in self.cubecalcsheets.keys():
			print "Saving "+ key +".csv"
			self.cubecalcsheets[key].to_csv(os.path.join(self.cubepath,key+".csv"),encoding="utf8")
			
		self.save_profile()
		
	def save_remote(self):
		print "Saving remote"
	

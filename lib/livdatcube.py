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
        return None
    df.index=df.key
    dfval=df.value
    dfdict=dfval.to_dict()
    return dfdict
def get_as_df(dictionary):
	df=pandas.DataFrame(columns=['key','value'],index=dictionary.keys())
	df.key=df.index
	#print pandas.Series(dictionary.values(),index=df.index)
	df.value=pandas.Series(dictionary.values(),index=df.index)
	return df
def string_to_range(string):
	if "range" in string:
		rangedef=string.replace("range(","").replace(")","").split(",")
		indexrange=range(int(rangedef[0]),int(rangedef[1]))
		return indexrange
	return None
	
class DataCube(object):
	def __init__(self,name=None,src="local",localpath=None,remotesheetkey=None,remotesheetname=None,databender=None):
		# Identify the source, local or remote and init accordingly
		#If source is local - 
		if name==None:
			self.name="DataCube"
		else:
			self.name=name
		self.logger=logging.getLogger(self.name)
		coloredlogs.install(level="DEBUG",logger=self.logger,fmt=SOMA_CONSOLE_FORMAT,level_styles=SOMA_LEVEL_STYLES,field_styles=SOMA_FIELD_STYLES)
		self.logger.info("Hi there....let me just find my bearings ")
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
				self.logger.error("If source is local, a path must be provided")
				return None
			self.initlocal(localpath)
		#If source is remote
		if src=='remote':
			if remotesheetkey==None and remotesheetname==None:
				self.logger.error("If source is remote, a sheet name or sheet key must be provided")
				return None
			if databender == None:
				self.logger.error("If source is remote, a bender is needed")
				return None
			self.initremote(remotesheetname,remotesheetkey,databender)
			
	def show_profile(self):
		self.logger.info("\n"+get_color_json(self.jsonprofile))
	
	def save_profile(self):
		if "cubepath" in self.jsonprofile.keys():
			self.jsonfile=os.path.join(self.cubepath,"cube.json")
			self.set_property("jsonfile",self.jsonfile)
		else:
			self.logger.error("No local path specified")
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
			self.logger.error("If source is local, a path must be provided")
			return None
		self.cubepath=localpath
		self.set_property('cubepath',self.cubepath)
		self.cubedeffilepath=os.path.join(self.cubepath,"cubedef.csv")	
		self.set_property('cubedeffilepath',self.cubedeffilepath)
		self.cubedictsfilepath=os.path.join(self.cubepath,"cubedicts.json")
		self.set_property('cubedictsfilepath',self.cubedictsfilepath)
		if self.src=="local":
			self.logger.info("Initing local")
			if not os.path.exists(self.cubepath):
				self.logger.info("Making directory",self.cubepath)
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
				self.logger.info("Please enter a cube definition in the file " + os.path.join(self.cubepath,"cubedef.csv"))
		self.local=True	
		self.set_property("local",self.local)
		
	def initremote(self,remotesheetname=None,remotesheetkey=None,databender=None):
		self.cubesheetname=remotesheetname
		self.cubesheetkey=remotesheetkey
		if self.cubesheetkey==None and self.cubesheetname==None:
			self.logger.error("If source is remote, a sheet name or sheet key must be provided")
			self.remote=False
			return None
		if databender == None:
			self.logger.error("If source is remote, a bender is needed")
			self.remote=False
			return None	
		
		cubesheetdict={}
		cubesheetdict['id']=self.cubesheetkey
		cubesheetdict['name']=self.cubesheetname
		cubesheetdict=databender.lookup_ssheet(cubesheetdict)
		self.logger.info("Looked up sheetdict",cubesheetdict)
		if cubesheetdict['id']!=None and cubesheetdict['name']==None:
			self.logger.error("Specified id doesnt exist and no name specified")
			self.remote=False
			return None
		if cubesheetdict['id']==None and cubesheetdict['name'] !=None:
			self.logger.info("Creating sheet...")
			databender.gc.create(title=cubesheetdict['name'])
		self.cubesheet=databender.get_ssheet(name=cubesheetdict['name'])
		self.cubesheetname=self.cubesheet.title
		self.cubesheetkey=self.cubesheet.id

		self.set_property("cubesheetname",self.cubesheetname)
		self.set_property("cubesheetkey",self.cubesheetkey)
		if self.src=="remote":
			self.logger.info("Initing remote")
			if 'cubedef' in get_worksheet_names(self.cubesheet):
				self.cubedef=self.cubesheet.worksheet_by_title("cubedef").get_as_df()
				self.cubedefdict=get_as_dict(self.cubedef)
			else:
				self.logger.warning("Could not get cubedef....trying to create")
				try:
					self.cubesheet.add_worksheet(title="cubedef")
					self.cubedef=pandas.DataFrame(columns=['key','value'])
					keys=pandas.Series(['index','cubename','dictionary_prefix','datasheet_prefix','columns'])
					self.cubedef.key=keys
					self.cubesheet.worksheet_by_title("cubedef").set_dataframe(self.cubedef,(1,))
					self.logger.info("Please enter a cube definition in the worksheet cubedef at https://docs.google.com/spreadsheets/d"+self.cubesheet.id)
				except Exception as e:
					self.logger.error("Could not create worksheet because", str(e))
					
			
		self.remote=True
		self.set_property("remote",self.remote)
		
		return None
	def initmemory (self):
		self.logger.info("Initing memory")
		self.build_cube()
		if self.check_cube_data()==True:
			self.load_cube_data()
		self.load_cube_dicts()
		self.load_cube_calcsheets()
		
	def build_cube(self):
		if self.get_property(self.src)==False:
			self.logger.error("Cannot build cube, specified source is not connected, init local or remote successfully first")
			return None
		self.cubename=self.cubedefdict['cubename']
		self.set_property("cubename",self.cubename)
		self.save_profile()
		self.logger.info("Prefixes-")
		for key,value in self.cubedefdict.iteritems():
			if "_prefix" in key:
				self.logger.info(key+" "+value)
				self.set_property(key,value)
		self.logger.info("Index-")
		self.set_property("index",self.cubedefdict['index'])
		indexrange=string_to_range(self.cubedefdict['index'])
		self.logger.info(str(indexrange))
		
		self.logger.info("Columns-")
		columnrange=self.cubedefdict['columns'].split(",")
		self.logger.info(str(columnrange))
		self.cubedatadf=pandas.DataFrame(columns=columnrange,index=indexrange)
		
	def check_cube_data(self):
		checked=True
		for i in self.cubedatadf.index:
			for col in self.cubedatadf.columns:
				datasheetname=self.get_property("datasheet_prefix")+"_"+str(i)+"_"+col
				if self.src=="local":
					datafilename=datasheetname+".csv"
					if os.path.exists(os.path.join(self.get_property("cubepath"),datafilename)):
						self.logger.info(os.path.join(self.get_property("cubepath"),datafilename) + " exists...checked!")
					else:
						self.logger.error(os.path.join(self.get_property("cubepath"),datafilename) + " does not exists...:(!")
						checked=False
				if self.src=="remote":
					if datasheetname in get_worksheet_names(self.cubesheet):
						self.logger.info(datasheetname + " exists...checked!")
					else:
						self.logger.error(datasheetname + " does not exists...:(!")
						checked=False
		return checked
	def load_cube_data(self):
		for i in self.cubedatadf.index:
			for col in self.cubedatadf.columns:
				self.logger.info("Loading "+str(i)+" "+str(col))
				datasheetname=self.get_property("datasheet_prefix")+"_"+str(i)+"_"+col
				if self.src=="local":
					datafilename=datasheetname+".csv"
					if os.path.exists(os.path.join(self.get_property("cubepath"),datafilename)):
						self.cubedatadf[col][i]=pandas.read_csv(os.path.join(self.get_property("cubepath"),datafilename))
				if self.src=="remote":
					if datasheetname in get_worksheet_names(self.cubesheet):
						self.cubedatadf[col][i]=self.cubesheet.worksheet_by_title(datasheetname).get_as_df()
	def load_cube_calcsheets(self):
		calcsheets=[]
		if self.src=="local":
			self.logger.info("Loading calculated sheets from local..")
			for fn in os.listdir(self.cubepath):
				ws=fn.replace(".csv","")
				if ws.split("_")[0]==self.cubename:
					self.logger.info("Found calculated sheet " + ws)
					calcsheets.append(ws)
			for sheet in calcsheets:
				self.logger.info("Reading "+ os.path.join(self.cubepath,sheet+".csv"))
				self.cubecalcsheets[sheet]=pandas.read_csv(os.path.join(self.cubepath,sheet+".csv"))
		if self.src=="remote":
			self.logger.info("Loading calculated sheets from remote...")
			for ws in get_worksheet_names(self.cubesheet):
				if ws.split("_")[0]==self.cubename:
					self.logger.info("Found calculated sheet " + ws)
					calcsheets.append(ws)
			for sheet in calcsheets:
				self.logger.info("Fetching "+sheet)
				self.cubecalcsheets[sheet]=self.cubesheet.worksheet_by_title(sheet).get_as_df()
	def load_cube_dicts(self):
		if self.src=="local":
			self.logger.info("Loading cube dicts from local file "+self.cubedictsfilepath)
			if os.path.exists(self.cubedictsfilepath):
				with open(self.cubedictsfilepath,"r") as cubedictsjson:
					self.cubedicts=json.loads(cubedictsjson.read())
			else:
				self.cubedicts={}
		if self.src=="remote":
			self.logger.info("Loading cube dicts from remote source ")
			self.cubedicts={}
			dictsheets=[]
			for ws in get_worksheet_names(self.cubesheet):
				if ws.split("_")[0]==self.get_property("dictionary_prefix"):
					self.logger.info("Found dictionary " +ws)
					dictsheets.append(ws)
			for ws in dictsheets:
				self.logger.info("Fetching " + ws)
				self.cubedicts[ws]=get_as_dict(self.cubesheet.worksheet_by_title(ws).get_as_df())
		
		
	def save_local(self):
		self.logger.info("Saving local")
		self.logger.info("Saving cube definition")
		self.cubedef.to_csv(self.cubedeffilepath,index=False,encoding="utf8")
		self.logger.info("Saving cube dictionaries")
		with open(self.cubedictsfilepath,"w") as cubedictsjson:
			cubedictsjson.write(json.dumps(self.cubedicts))
		self.logger.info("Saving cube data")
		for i in self.cubedatadf.index:
			for col in self.cubedatadf.columns:
				self.logger.info("Writing file "+ os.path.join(self.cubepath,self.get_property("datasheet_prefix")+"_"+str(i)+"_"+col+".csv"))
				self.cubedatadf[col][i].to_csv(os.path.join(self.cubepath,self.get_property("datasheet_prefix")+"_"+str(i)+"_"+col+".csv"),index=False,encoding="utf8")
		self.logger.info("Saving cube calculated sheets")
		for key in self.cubecalcsheets.keys():
			self.logger.info("Writing file "+ os.path.join(self.cubepath,key+".csv"))
			self.cubecalcsheets[key].to_csv(os.path.join(self.cubepath,key+".csv"),index=False,encoding="utf8")
			
		self.save_profile()
		
	def save_remote(self):
		self.logger.info("Saving remote")
		self.logger.info("Saving cube definition")
		if 'cubedef' not in get_worksheet_names(self.cubesheet):
			self.cubesheet.add_worksheet(title="cubedef")
		self.cubesheet.worksheet_by_title("cubedef").set_dataframe(self.cubedef,(1,1))
		self.logger.info("Saving cube dictionaries")
		for dictionary in self.cubedicts.keys():
			if dictionary not in get_worksheet_names(self.cubesheet):
				self.cubesheet.add_worksheet(title=dictionary)
			dictdf=get_as_df(self.cubedicts[dictionary])
			self.cubesheet.worksheet_by_title(dictionary).set_dataframe(dictdf,(1,1))
		self.logger.info("Saving cube data")
		for i in self.cubedatadf.index:
			for col in self.cubedatadf.columns:
				self.logger.info("Uploading "+ self.get_property("datasheet_prefix")+"_"+str(i)+"_"+col)
				self.cubesheet.worksheet_by_title(self.get_property("datasheet_prefix")+"_"+str(i)+"_"+col).set_dataframe(self.cubedatadf[col][i],(1,1))
		self.logger.info("Saving cube calculated sheets")
		for calcsheet in self.cubecalcsheets.keys():
			if calcsheet not in get_worksheet_names(self.cubesheet):
				self.cubesheet.add_worksheet(title=calcsheet)
			self.cubesheet.worksheet_by_title(calcsheet).set_dataframe(self.cubecalcsheets[calcsheet],(1,1))
		

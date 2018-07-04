import ConfigParser
import os,sys
#sys.path.append("/opt/xetrapal")
#import xetrapal
# from libsoma import *
import pygsheets
from bs4 import BeautifulSoup
#from xetrapal.Xetrapal import Xetrapal

     
        
def get_gc(confile):
    config=ConfigParser.ConfigParser()
    config.read(confile)
    try:
        outhstore = config.get("Google","outhstore")
        outhfile = config.get("Google","outhfile")

    except:
        print("Not the right conf file try again")
        
    try:
        
        gc=pygsheets.authorize(outh_file=outhfile,outh_nonlocal=True,outh_creds_store=outhstore)
        return gc   
    except:
        print("Not able to authorize")
        return None

        
        
        
        
        
        
        
        
        #super(DataBender,self).__init__(*args, **kwargs)
		#self.logger.info("Looks like I'm a databender")
		 #self.gdrive_login()
          
         #self.get_googledriver()   
          
         #self.datacubes=[]
		
		
def lookup_ssheet(gc,sheetdict):
    
    

    #logger.info("Looking up sheetdict")
    for ssheet in gc.list_ssheets():
        
           if sheetdict['id']==ssheet['id']:
				#logger.info("Found by ID")
		return ssheet
    if sheetdict['name']==ssheet['name']:
				#self.logger.info("Found by name")
		return ssheet
			
		return sheetdict
	
def get_ssheet(key=None,name=None):
	if key==None and name==None:
		return None
	if key!=None:
		return get_ssheet_by_key(key)
	if name!=None:
		return get_ssheet_by_name(name)
	
def create_new_ssheet(gc,title,folderid=None):
	for ssheet in gc.list_ssheets():
		if ssheet['name']==title:
			print "Sheet exists...try a different name"
			return None
		gc.create(title,parent_id=folderid)
		for ssheet in gc.list_ssheets():
			if ssheet['name']==title:
				print "Sheet %s created" %title
				return gc.open_by_key(ssheet['id'])
def get_ssheet_by_key(gc,key):
		try:
			#self.logger.info("Trying to fetch heet " + key )
			return gc.open_by_key(key)
		except:
			return None
def get_sheet_last_row(ssheet,sheetname):
	sheet=ssheet.worksheet_by_title(sheetname)
	rownum=2
	rowval=sheet.get_row(rownum)
	if rowval==['']:
		return None
	else:
		while rowval != ['']:
			rownum+=1
			rowval=sheet.get_row(rownum)
			return sheet.get_row(rownum-1)

	
def get_ssheet_by_name(gc,title):
	for ssheet in gc.list_ssheets():
		if ssheet['name']==title:
			#	self.logger.info("Sheet " + title  + " exists...fetching")
			return gc.open_by_key(ssheet['id'])
		#self.logger.error("Sheet does not exist...is your name correct")
		return None


		
#	def get_json_feed(self,feedurl):
#		response=urllib2.urlopen(feedurl)
#		data=json.load(response)
#		return data
	
	#def goto_sheet_by_key(self,sheetkey):
	#	self.goto_url("https://docs.google.com/spreadsheets/d/"+sheetkey)
	
	#def goto_sheet_tab(self,sheetname):
	#	for sheettab in self.driver.find_elements_by_class_name("docs-sheet-tab-name"):
	#		print sheettab.get_property("innerHTML")
	
#if sheettab.get_property("innerHTML")==sheetname:
#				sheettab.click()
	
	
	#def build_cube(self,sheetname=None,key=None):
	#	if name==None and key==None:
	#		self.logger.error("No remote identifier specified,local copy only")
	#		return None
	#	if name != None:
	#		self.logger.info("Trying to build cube from "+name)
	#		cubesheet=self.get_ssheet_by_name(name)
			
	#		cubesheet=self.get_ssheet_by_key(key)
	#	return cubesheet
		

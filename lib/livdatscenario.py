import os,sys

sys.path.append("/opt/livingdata/lib")

from livdatbutler import *
from libsoma import *
import pygsheets
from bs4 import BeautifulSoup

def get_color_json(dictionary):
	formatted_json=get_formatted_json(dictionary)
	colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.TerminalFormatter())
	return colorful_json

def get_formatted_json(dictionary):
	formatted_json=json.dumps(dictionary,sort_keys=True, indent=4)
	return formatted_json

class ScenarioGenerator(Butler):
	def __init__(self,configfile):
		config=ConfigParser.ConfigParser()
		config.read(configfile)
		self.outhstore = config.get("Google","outhstore")
		self.outhfile = config.get("Google","outhfile")
		self.scenariobookkey=config.get("Scenario","bookkey")
		self.name=config.get("Scenario","name")	
		self.config=config
		print "Read config for " + self.name
		self.gc=pygsheets.authorize(outh_file=self.outhfile,outh_nonlocal=True,outh_creds_store=self.outhstore)
		self.scenariobook=self.gc.open_by_key(self.scenariobookkey)
		self.scenariodef=self.scenariobook.worksheet_by_title("Scenario").get_as_df()
		
	def get_sheet_last_row(sheetname):
	sheet=self.scenariobook.worksheet_by_title(sheetname)
	rownum=2
	rowval=sheet.get_row(rownum)
	if rowval==['']:
		return None
	else:
		while rowval != ['']:
			rownum+=1
			rowval=sheet.get_row(rownum)
		return sheet.get_row(rownum-1)

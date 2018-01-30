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

class ScenarioGenerator(DataButler):
	def __init__(self,*args, **kwargs):
		super(ScenarioGenerator,self).__init__(*args, **kwargs)
		self.scenariobookkey=self.config.get("Scenario","bookkey")
		try:
			print "Trying to get scenario book..."
			self.scenariobook=self.gc.open_by_key(self.scenariobookkey)
			self.scenariodef=self.scenariobook.worksheet_by_title("Scenario").get_as_df()
		except:
			print "Failed to open scenario book by key " + self.scenariobookkey
		self.name=self.config.get("Scenario","name")	
	
	def blank_scenario(self):
		scenario={}
		for row in sc.scenariodef.itertuples():
		if row.Type=="read":
			print "Reading cell " + str(row.Cell) + " from RunSheet for field " + row.Name
			scenario[row.Name]=sc.scenariobook.worksheet_by_title("RunSheet").cell(str(row.Cell)).value
		if row.Type=="variable":
			print row.Name + " is a variable to be put in " + row.Cell
			scenario[row.Name]=None
		if row.Type=="result":
			print row.Name + " is a result to be put in " + row.Cell
			scenario[row.Name]=None
		return None

import os,sys,pandas
class DataStream(object):
	def __init__(self,path,columnnames):
		self.columnnames=columnnames
		self.fulldf=pandas.DataFrame(columns=self.columnnames)
		self.latestdf=pandas.DataFrame(columns=self.columnnames)
		if not os.path.exists(path):
			os.mkdir(path)
		self.path=path	
		self.latestjsonpath=os.path.join(self.path,"latest.json")
		self.fulljson=os.path.join(self.path,"full.json")


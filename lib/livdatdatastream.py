import os,sys,pandas,json
class DataStream(object):
	def __init__(self,path,columnnames=[],latestcount=100):
		self.path=path
		self.columnnames=columnnames
		if not os.path.exists(self.path):
			os.mkdir(self.path)
		self.latestjsonpath=os.path.join(self.path,"latest.json")
		self.fulljsonpath=os.path.join(self.path,"full.json")
		
		if not os.path.exists(self.fulljsonpath):
				
			self.fulldf=pandas.DataFrame(columns=self.columnnames)
			self.latestdf=pandas.DataFrame(columns=self.columnnames)
		else:		
			self.fulldf=pandas.read_json(self.fulljsonpath,orient="index").drop_duplicates().sort_values(by="created_at")
			self.latestdf=self.fulldf[-1*latestcount]
		self.columnnames=list(self.fulldf.columns)
		
		with open(self.fulljsonpath,"w") as f:
			f.write(json.dumps(self.fulldf.to_json(orient="index")))
		with open(self.latestjsonpath,"w") as f:
			f.write(json.dumps(self.latestdf.to_json(orient="index")))
	
				
	def save_stream(self):
		with open(self.fulljsonpath,"w") as f:
			f.write(json.dumps(self.fulldf.to_json(orient="index")))
		with open(self.latestjsonpath,"w") as f:
			f.write(json.dumps(self.latestdf.to_json(orient="index")))
		
	def append_data(self,newdatadf):
		self.fulldf=self.fulldf.append(newdatadf).drop_duplicates().sort_values(by="created_at")
		self.latestdf=self.fulldf[-1*latestcount]
		
	

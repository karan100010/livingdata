import os,sys,pandas,json
class DataStream(object):
	def __init__(self,path,columnnames=["created_at"],latestcount=50):
		self.path=path
		self.columnnames=columnnames
		self.latestcount=latestcount
		if not os.path.exists(self.path):
			os.mkdir(self.path)
		self.latestjsonpath=os.path.join(self.path,"latest.json")
		self.fulljsonpath=os.path.join(self.path,"full.json")
		self.fulldf=pandas.DataFrame(columns=self.columnnames)
		self.latestdf=pandas.DataFrame(columns=self.columnnames)
		
		if os.path.exists(self.fulljsonpath):
			try:
				self.fulldf=pandas.read_json(self.fulljsonpath,orient="index").drop_duplicates().sort_values(by="created_at")
				self.latestdf=self.fulldf[-1*self.latestcount:]
			except ValueError as exception:
				if "need more than 0 values to unpack" in exception:
					print "No entries in datastream yet"
			
		self.columnnames=list(self.fulldf.columns)
		
		with open(self.fulljsonpath,"w") as f:
			try:
				f.write(self.fulldf.to_json(orient="index"))
				f.write("\n")
			except Exception as exception:
				print exception
		with open(self.latestjsonpath,"w") as f:
			try:
				self.latestdf=self.fulldf[-1*self.latestcount:]
				f.write(self.latestdf.to_json(orient="index"))
				f.write("\n")
			except Exception as exception:
				print exception
				
	def save_stream(self):
		print "Saving stream at " + self.path
		with open(self.fulljsonpath,"w") as f:
			#print self.fulldf
			f.write(self.fulldf.to_json(orient="index"))
			f.write("\n")
		with open(self.latestjsonpath,"w") as f:
			#print self.latestdf
			f.write(self.latestdf.to_json(orient="index"))
			f.write("\n")
	
	def append_data(self,newdatadf):
		self.fulldf=self.fulldf.append(newdatadf).sort_values(by="created_at").drop_duplicates('created_at').reset_index(drop=True).sort_index()
		self.latestdf=self.fulldf[-1*self.latestcount:]
		
	

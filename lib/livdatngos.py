import os,sys
sys.path.append("../lib")
from livdatcsvlib import *


class NGOList(CSVFile):
	def addSectorCount(self,colname,namecol):
		outfile=NGOList()
		outfile.colnames=self.colnames
		outfile.colnames.append("SectorCount")
		counter=len(self.matrix)
		for row in self.matrix:
			#sys.stdout.write("\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b"+str(counter)+"|"+str(len(self.matrix)))
			#counter-=1
			dictionary=row
			#print row
			if row[colname]!=None and row[namecol]!=None:
				dictionary['SectorCount']=str(len(row[colname].split(",")))
				outfile.matrix.append(dictionary)
		return outfile
	def addSectorScoreCol(self,namecol,colname,scorecolname,sectorscorefile):
		secfile=NGOList()
		secfile.importfile(sectorscorefile)
		secdict={}
		for row in secfile.matrix:
			secdict[row['Sector Name']]=row[scorecolname]
		print secdict
		outfile=NGOList()
		outfile.colnames=self.colnames
		if scorecolname not in self.colnames:
			outfile.colnames.append(scorecolname)
		counter=len(self.matrix)
		for row in self.matrix:
			#sys.stdout.write("\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b"+str(counter)+"|"+str(len(self.matrix)))
			#counter-=1
			dictionary=row
			#print row
			if row[colname]!=None and row[namecol]!=None:
				score=0	
				rowsectors=row[colname].strip().split(",")
				rowsectorsstripped=[]
				for item in rowsectors:
					item=item.lstrip(" ").rstrip(" ")
					if item!="":
						rowsectorsstripped.append(item)
				#print rowsectorsstripped
				if rowsectorsstripped==[]:
					continue
				for sector in rowsectorsstripped:
					if sector not in secdict.keys():
						print "Warning! unrecognized sector...update sector file? check data? - Sector name ",sector
						score+=0
					else:
						score+=int(secdict[sector])
				
				dictionary[scorecolname]=str(score)
				outfile.matrix.append(dictionary)
		return outfile
	def filterbysector(self,sectorstring,sectorcol):
		subsetfile=NGOList()
		subsetfile.colnames=self.colnames
		if 'Percentage Match' not in self.colnames:
			subsetfile.colnames.append("Percentage Match")
		if "|" in sectorstring:
			operation=" or "
			seclist=sectorstring.strip('|').split(",")
		if "+" in sectorstring:
			operation=" and "
			seclist=sectorstring.strip('+').split(",")
		if "#" in sectorstring:
			operation=" only "
			seclist=sectorstring.strip("#").split(",")
		filtersectorset=set(seclist)
		for row in self.matrix:
				rowadd=row
				rowsectors=row[sectorcol].strip().split(",")
				rowsectorsstripped=[]
				for item in rowsectors:
					item=item.lstrip(" ").rstrip(" ")
					if item!="":
						rowsectorsstripped.append(item)
				#print rowsectorsstripped
				if rowsectorsstripped==[]:
					continue
				rowsectorset=set(rowsectorsstripped)
				filterflag=0
				matchcount=0
				if operation==" or " and len(filtersectorset&rowsectorset)>0:
					filterflag=1
					matchcount=len(filtersectorset&rowsectorset)
				if operation==" and " and len(filtersectorset&rowsectorset)==len(filtersectorset):
					filterflag=1
					matchcount=len(filtersectorset&rowsectorset)
				if operation==" only " and filtersectorset==rowsectorset:
					filterflag=1
					matchcount=len(filtersectorset&rowsectorset)
				rowcount=len(rowsectorset)
				percentmatch=matchcount*100/rowcount
				rowadd['Percentage Match']=str(percentmatch)
				if filterflag==1:
					subsetfile.matrix.append(rowadd)
		return subsetfile
	def getsectorlist(self,colname):
		sectorset=set([])
		for row in self.matrix:
				rowsectors=row[colname].strip().split(",")
				rowsectorsstripped=[]
				for item in rowsectors:
					item=item.lstrip(" ").rstrip(" ")
					if item!="":
						rowsectorsstripped.append(item)
				#print rowsectorsstripped
				if rowsectorsstripped==[]:
					continue
				rowsectorset=set(rowsectorsstripped)
				sectorset=sectorset|rowsectorset
		return list(sectorset)
	

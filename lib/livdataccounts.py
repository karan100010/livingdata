import os,sys
sys.path.append("../lib")
from livdatcsvlib import *

TALLYCOLNAMES=["DATE","BY","TO","AMOUNT","NARRATION","VOUCHERTYPE","VOUCHERNUM","PERSON","RECEIPT","PAYMENT"]
ONLINEVOUCHERCOLNAMES=["PERSON","DATE","VN","VENDOR","CAT","NARRAT","AMT","SRC","VOUCHERREF"]


	
def getheadsfromfile(headfile):
	f=open(headfile,"r")
	headlist=[]
	for line in f.readlines():
		headlist.append(line.strip("\n").lstrip(" ").rstrip(" "))
	return headlist
def getcategories(headfile):
	f=open(headfile,"r")
	headlist=[]
	for line in f.readlines():
		headlist.append(line.strip("\n"))
	return headlist

class AccountsExcel(ExcelFile):
	def __init__(self):
		self.filename=""
		self.worksheetnames=[]
		self.worksheets=[]
		self.headsheet="heads"
		self.categorysheet="categories"	
	def setcategorysheet(self,sheetname):
		self.categorysheet=sheetname
	def setheadsheet(self,sheetname):
		self.headsheet=sheetname	
	def getheadsfromsheet(self,sheetname="",headcol="HEAD"):
		if sheetname=="":
			if self.headsheet=="":
				print "No head sheet name defined!"
				return
			else:
				sheetname=self.headsheet
		heads=[]
		for sheet in self.worksheets:
			if sheet.filename.split(".")[0]==sheetname:
				for row in sheet.matrix:
					heads.append(row[headcol])
		return heads
	def getcategoriesfromsheet(self,sheetname="",catcol='CATEGORY'):
		if sheetname=="":
			if self.categorysheet=="":
				print "No category sheet name defined!"
				return
			else:
				sheetname=self.categorysheet
		categories=[]
		for sheet in self.worksheets:
			if sheet.filename.split(".")[0]==sheetname:
				for row in sheet.matrix:
					categories.append(row[catcol])
		return categories

class TransactionList(CSVFile):
	def SetCategoryFromField(self,fieldname,searchkey,catval,categoryfield=u"CATEGORY",filterstring="matchstringsany"):
		if categoryfield not in self.colnames:
			self.colnames.append(categoryfield)
			self.padrows()
			self.prunerows()
		idlist=self.filterids(searchkey,filterstring,fieldname)
		colnames=[categoryfield]
		values=[catval]
		self.updaterows(idlist,colnames,values)
		
	def SetHeadFromField(self,categories,fieldname,searchkey,headval,headfield=u"HEAD",filterstring="matchstringsany",categoryfield=u"CATEGORY"):			
		if headfield not in self.colnames:
			self.colnames.append(headfield)	
			self.padrows()
			self.prunerows()
		catidlist=self.filterids(",".join(categories),filterstring,categoryfield)
		headidlist=self.filterids(searchkey,filterstring,fieldname,idlist=catidlist)
		colnames=[headfield]
		values=[headval]
		self.updaterows(headidlist,colnames,values)
	def alterDateFormat(self,datefields,fmtcur,fmtfinal):
		for row in self.matrix:
			for field in datefields:
				row[field]=unicode(datetime.datetime.strptime(row[field],fmtcur).strftime(fmtfinal))
	
class BankStatement(TransactionList):
	def SetAmountTransType(self,withdrawalfield,depositfield):
		self.colnames+=[u"Amount",u"TransType"]
		for row in self.matrix:
			if row[withdrawalfield].lstrip(" ").rstrip(" ")!="":
				row[u'TransType']=u'Withdrawal'
				row[u'Amount']=str(float(row[withdrawalfield].lstrip(" ").rstrip(" ")))
			if row[depositfield].lstrip(" ").rstrip(" ")!="":
				row[u'TransType']=u'Deposit'
				row[u'Amount']=str(float(row[depositfield].lstrip(" ").rstrip(" ")))
				
		
		                
class VoucherList(TransactionList):
	def GenerateVoucherListFromPath(self,path,formatfile):
		filelist=os.popen("ls %s/*.PDF" %path).read().strip().lstrip("\/").split("\n")
		f=open(formatfile,"rb")
		keys=f.read().strip("\n").split("-")
		retfile=VoucherList()
		retfile.colnames=keys
		#print keys
		badfiles=[]
		for item in filelist:
			vals=item.strip(".PDF").lstrip("/").split("-")
			#print vals
			dictionary={}
			if len(vals)!=len(keys):
				badfiles.append(item)
				continue
			for i in range(0,len(keys)):
				dictionary[keys[i]]=vals[i]
			retfile.matrix.append(dictionary)
		print "Bad Filenames:\n",badfiles
		return retfile
	def CreateVoucherRefCol(self,fieldnames):
		newfile=VoucherList()
		newfile.colnames=self.colnames
		newfile.colnames.append("VOUCHERREF")
		for row in self.matrix:
			dictionary=row
			voucherref=""
			for item in fieldnames:
				voucherref=voucherref+dictionary[item]+"-"
			voucherref=voucherref.strip("-")
			dictionary["VOUCHERREF"]=voucherref
			newfile.matrix.append(dictionary)
		return newfile	
	def AddDateColumnFromField(self,fieldname):
		newfile=VoucherList()
		newfile.colnames=self.colnames
		newfile.colnames.append("SETDATE")
		for row in self.matrix:
			dictionary=row
			date=dictionary[fieldname]
			year=date[:4]
			month=date[4:][:2]
			day=date[6:][:2]
			print date,year,month,day
			dictionary["SETDATE"]=year+"-"+month+"-"+day
			newfile.matrix.append(dictionary)
		return newfile
	def GetBadVoucherFilenamesFromFolder(self,folder,filenameformat):
		f=open(filenameformat,"rb")
		fnfstring=f.read().strip("\n")
		print "Filename Format: ",fnfstring
		fnfnumtokens=len(fnfstring.split("-"))
		filelist=os.popen("ls %s" %folder).read().strip().split("\n")
		badlist=[]
		for filename in filelist:
			filenamenumtokens=len(filename.strip(".PDF").split("-"))
			#print filename,filenamenumtokens,fnfnumtokens
			if filenamenumtokens!=fnfnumtokens:
				badlist.append(filename)
		return badlist
	def GetVoucherListFromFolder(self,folder,filenameformat):
		badfiles=self.GetBadVoucherFilenamesFromFolder(folder,filenameformat)
		if len(badfiles)!=0:
			print "Please correct the following filenames first:",badfiles
			return
		filelist=os.popen("ls %s" %folder).read().strip().split("\n")
		retfile=VoucherList()
		f=open(filenameformat,"rb")
		fnfstring=f.read().strip("\n")
		print "Filename Format: ",fnfstring
		fnftokens=fnfstring.split("-")
		for filename in filelist:
			dictionary={}
			filenametokens=filename.strip(".PDF").split("-")
			#print filename,filenamenumtokens,fnfnumtokens
			for i in range(0,len(filenametokens)):
				dictionary[fnftokens[i]]=filenametokens[i]
				dictionary["VOUCHERREF"]=filenametokens[0]+"-"+filenametokens[1]+"-"+filenametokens[2]+"-"+filenametokens[3]
			retfile.matrix.append(dictionary)
		retfile.colnames=fnftokens
		retfile.colnames.append("VOUCHERREF")
		return retfile

class TallyVoucherList(TransactionList):
	def SetAmountTransType(self,withdrawalfield,depositfield):
		self.colnames+=[u"Amount",u"TransType"]
		for row in self.matrix:
			if row[withdrawalfield].lstrip(" ").rstrip(" ")!="":
				row[u'TransType']=u'Withdrawal'
				row[u'Amount']=str(float(row[withdrawalfield].lstrip(" ").rstrip(" ")))
			if row[depositfield].lstrip(" ").rstrip(" ")!="":
				row[u'TransType']=u'Deposit'
				row[u'Amount']=str(float(row[depositfield].lstrip(" ").rstrip(" ")))
	def SetNarration(self,particularsfield="Particulars"):
		rowindex=0
		for row in self.matrix:
			if row[particularsfield]=="Dr" or row[particularsfield]=="Cr":
				row[particularsfield]=self.matrix[rowindex+1][particularsfield]
				self.matrix.remove(self.matrix[rowindex+1])
			rowindex+=1
	
					
	def ImportOnlineVoucherList(self,voucherlist):
		v=VoucherList()
		v.importfile(voucherlist)
		t=TallyVoucherList()
		t.colnames=TALLYCOLNAMES
		if v.colnames!=ONLINEVOUCHERCOLNAMES:
			print "Mismatch!!! This is not an online voucherlist since it doesnt have the columns", ONLINEVOUCHERCOLNAMES
			print "Online Voucher Lists should have the following colnames", ONLINEVOUCHERCOLNAMES
			return
		for row in v.matrix:
			dictionary={}
			dictionary["DATE"]=row["DATE"]
			dictionary["AMOUNT"]=row["AMT"]
			dictionary["NARRATION"]=row["NARRAT"]
			dictionary["VOUCHERNUM"]=row["VOUCHERREF"]
			dictionary["PERSON"]=row["PERSON"]
			t.matrix.append(dictionary)
		return t
	
					

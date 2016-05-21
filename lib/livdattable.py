import sys,os,csv,json, codecs, cStringIO, datetime
import xlrd,copy, xlsxwriter  

class Table:
    def __init__(self):
        self.matrix=[]
        self.filename=""
        self.colnames=[]
        self.idfield=""
        self.filename=""
    def importfile(self,csvfilename):
        dictlist=[]
        f=open(csvfilename,"rb")
        reader=csv.UnicodeReader(f,delimiter=",",quotechar='"')
        for row in reader:
            dictlist.append(row)
        self.filename=csvfilename
        self.colnames=reader.fieldnames
        self.matrix=dictlist
        self.idfield=self.colnames[0]
        self.filename=csvfilename
        return self
    def exportfile(self,csvfilename=None):
        if self.colnames==[]:
            return None
        else:
            fieldnames=self.colnames
            f2=open(csvfilename,"wb")
            writer=csv.UnicodeWriter(f2,delimiter=",",quotechar='"',fieldnames=fieldnames)
            writer.writerow(dict((fn,fn) for fn in fieldnames))
            for row in self.matrix:
                writer.writerow(row)
    def exportcols(self,excolnames):
        finalcsv=Table()
        finalcsv.colnames=excolnames
        for row in self.matrix:
            dictionary={}
            for k,v in row.iteritems():
                if k in finalcsv.colnames:
                    dictionary[k]=v
            finalcsv.matrix.append(dictionary)
        return finalcsv
    def removeblankrows(self):
		finalcsv=Table()
		finalcsv.colnames=self.colnames
		for row in self.matrix:
			valueset=[]
			for k,v in row.iteritems():
				try:
					valueset.append(v.encode("utf-8").lstrip().rstrip())
				except:
					print v
					break
			if set(valueset)!=(''):
				dictionary={}
				for colname in self.colnames:
					dictionary[colname]=row[colname]
				finalcsv.matrix.append(dictionary)
		return finalcsv
    def deduplicaterows(self):
        finalcsv=Table()
        finalcsv.colnames=self.colnames
        tempmatrix=[]
        for item in set([tuple(row.items()) for row in self.matrix]):
            dictin={}
            for pair in item:
                dictin[pair[0]]=pair[1]
            tempmatrix.append(dictin)
        finalcsv.matrix=tempmatrix
        return finalcsv

    def filldefaults(self,fieldname,value):
        finalcsv=Table()
        finalcsv.colnames=self.colnames
        for row in self.matrix:
            dictionary=row
            dictionary[fieldname]=value
            finalcsv.matrix.append(dictionary)
        return finalcsv    
    def mergefields(self,fields,delimiter='|',include_fieldnames=False, nfieldname=""):
        finalcsv=Table()
        finalcsv.colnames=self.colnames
        newfieldname=""
        print finalcsv.colnames
        for fieldname in fields:
            finalcsv.colnames.remove(fieldname)
            newfieldname=newfieldname+fieldname+delimiter
        newfieldname=newfieldname.strip(delimiter)
        finalcsv.colnames.append(newfieldname)
        for row in self.matrix:
            dictionary=row
            dictionary[newfieldname]=""
            for fieldname in fields:
                if include_fieldnames==False:
                    dictionary[newfieldname]=dictionary[newfieldname]+dictionary[fieldname]+delimiter
                else:
                    dictionary[newfieldname]=dictionary[newfieldname]+fieldname+":"+dictionary[fieldname]+delimiter
                dictionary.pop(fieldname,None)
            dictionary[newfieldname]=dictionary[newfieldname].strip(delimiter)
            finalcsv.matrix.append(dictionary)
        return finalcsv
    def __init__(self):
        self.matrix=[]
        self.filename=""
        self.colnames=[]
        self.idfield=""
    def importfile(self,csvfilename):
        dictlist=[]
        f=open(csvfilename,"rb")
        reader=csv.DictReader(f,delimiter=",",quotechar='"')
        for row in reader:
            dictlist.append(row)
        self.filename=csvfilename
        self.colnames=reader.fieldnames
        self.matrix=dictlist
        self.idfield=self.colnames[0]
        return self
    def exportfile(self,csvfilename=None):
        if self.colnames==[]:
            return None
        else:
            fieldnames=self.colnames
            f2=open(csvfilename,"wb")
            writer=csv.DictWriter(f2,delimiter=",",quotechar='"',fieldnames=fieldnames)
            writer.writerow(dict((fn,fn) for fn in fieldnames))
            for row in self.matrix:
                writer.writerow(row)
    def exportcols(self,excolnames):
        newfile=Table()
        newfile.colnames=excolnames
        for row in self.matrix:
            dictionary={}
            for k,v in row.iteritems():
                if k in newfile.colnames:
                    dictionary[k]=v
            newfile.matrix.append(dictionary)
        return newfile
    def printcols(self,colnames):
		for row in self.matrix:
			printrow=""
			for col in colnames:
				printrow=printrow+row[col]+","
			


def get_unique_vals_for_col(csv,colname):
  uniquevals=[]
  for row in csv.matrix:
    if row[colname] not in uniquevals:
      uniquevals.append(row[colname])
  return uniquevals

def importExcelFile(pathtofile):
	Tables=[]
	workbook=xlrd.open_workbook(pathtofile,encoding_override='utf-8')
	worksheets=workbook.sheet_names()
	for sheet in worksheets:
		currsheet=workbook.sheet_by_name(sheet)
		c=Table()
		c.filename=sheet+".CSV"
		for i in range(0,currsheet.ncols):
			c.colnames.append(currsheet.cell_value(0,i))
		for j in range(1,currsheet.nrows):
			dictionary={}
			for i in range(0,currsheet.ncols):
				if currsheet.cell_type(j,i)==xlrd.XL_CELL_DATE:
					date = datetime.datetime(1899, 12, 30)
					get_ = datetime.timedelta(int(currsheet.cell_value(j,i)))
					get_col2 = str(date + get_)[:10]
					d = datetime.datetime.strptime(get_col2, '%Y-%m-%d')
					get_col = d.strftime('%d-%b-%Y')
					dictionary[currsheet.cell_value(0,i)]=unicode(get_col)
				else:
					dictionary[currsheet.cell_value(0,i)]=unicode(currsheet.cell_value(j,i))
			c.matrix.append(dictionary)
		Tables.append(c)
	return Tables
	
def exportExcelFile(CSVFiles,pathtofile):
	wb=xlsxwriter.Workbook(pathtofile)
	for csv in CSVFiles:
		ws=wb.add_worksheet(csv.filename.split(".")[0])
		rownum=0
		colnum=0
		for colname in csv.colnames:
			ws.write(0,colnum,colname)
			colnum+=1
		for row in csv.matrix:
			rownum+=1
			colnum=0
			for colname in csv.colnames:
				ws.write(rownum,colnum,row[colname])
				colnum+=1
	wb.close()

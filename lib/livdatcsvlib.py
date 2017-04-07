import sys,os,csv,json, codecs, cStringIO, datetime
import xlrd,copy,xlsxwriter

def packkeyvalues(keys,values):
	dictionary=dict()
	if len(keys)!=len(values):
		print "Not enough keys or values!"
		return dictionary
	i=0
	for i in range(0,len(keys)):
		dictionary[keys[i]]=values[i]
		i+=1
	return dictionary


class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")

class UnicodeReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)
        self.fieldnames=self.reader.next()
    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]

    def __iter__(self):
        return self

class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        #print row
        self.writer.writerow([s for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

def genmergekeydict_interactive(left,right):
  newmergekey={}
  for attributes1 in left:
    print '\nPlease select corresponding Attribute Number for <' + attributes1 + '> from:'
    for index, attributes2 in enumerate(right):
      print index, attributes2
    choice = raw_input('Enter Your Choice, write None if nothing matches:')
    while(1):
      if choice.lower() == 'none':
        newname = raw_input('Enter New Name for ' + attributes1 + '(default '+attributes1+'): ')
        if newname=="":
          newname=attributes1
        newmergekey[attributes1]=newname
        break
      else:
        try:
          val = int(choice)
          if (val in range(len(right))):
            newname = raw_input('Enter New Name for ' + attributes1 + '(default '+right[val]+'): ')
            if newname=="":
              newname=right[val]
            newmergekey[attributes1]=newname
            right.remove(right[val])
            break
        except ValueError:
          choice = raw_input('Wrong Choice, Please Enter Your Again: ')
  return newmergekey
  
def union_caaaavs(csv1,csv2,unionfield1,unionfield2,colnames1,colnames2):
  finalcsv=CSVFile()
  csv1formerge=csv1.exportcols(colnames1)
  csv2formerge=csv2.exportcols(colnames2)
  print csv2formerge.colnames
  finalcsv.colnames=csv1formerge.colnames+csv2formerge.colnames
  for row in csv1formerge.matrix:
    dictionary=row
    for key in colnames2:
      dictionary[key]=""
    for lookuprow in csv2formerge.matrix:
      if row[unionfield1]==lookuprow[unionfield2]:
        for key in colnames1:
          dictionary[key]=row[key]
        for key in colnames2:
          dictionary[key]=lookuprow[key]
        print dictionary
    finalcsv.matrix.append(dictionary)
  return finalcsv
    
def get_unique_vals_for_col(csv,colname):
  uniquevals=[]
  for row in csv.matrix:
    if row[colname] not in uniquevals:
      uniquevals.append(row[colname])
  return uniquevals

def matchmatrices(matrix1,matrix2,mat1name="mat1",mat2name="mat2"):
	matchlist=[]
	if set(matrix1[0].keys())!=set(matrix2[0].keys()):
		print "Fieldnames dont match"
		return idlist
	else:
		for row1 in matrix1:
			for row2 in matrix2:
				#print "Checking", row1, row2
				match=False
				keys=row1.keys()[:]
				keys.remove('LD_ROWID')
				#print "Comparing keys",keys
				for key in keys:
					if row1[key]==row2[key]:
						match=True
						#print "Match made",key,row1[key],row2[key]
					else:
						match=False
						#print "Match broken"
						break
				if match==True:
					dictionary={}
					dictionary[mat1name]=row1['LD_ROWID']
					dictionary[mat2name]=row2['LD_ROWID']
					matchlist.append(dictionary)
	return matchlist

class ExcelFile:
	def __init__(self):
		self.filename=""
		self.worksheetnames=[]
		self.worksheets=[]
		self.workbook=None
	
		
		
	def importascsv(self,pathtofile):
		self.filename=os.path.split(pathtofile)[1]
		workbook=xlrd.open_workbook(pathtofile,encoding_override='utf-8')
		self.worksheetnames=workbook.sheet_names()
		for sheet in self.worksheetnames:
			currsheet=workbook.sheet_by_name(sheet)
			c=CSVFile()
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
				dictionary[u'LD_ROWID']=str(j)
				c.matrix.append(dictionary)
			self.worksheets.append(c)
			
	def exportfile(self,pathtofile):
		wb=xlsxwriter.Workbook(pathtofile)
		i=0
		for csv in self.worksheets:
			csv.filename=self.worksheetnames[i]
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
			i+=1
		wb.close()
	def getSheet(self,sheetname):
		if sheetname not in self.worksheetnames:
			return []
		else:
			for sheet in self.worksheets:
				if sheetname==sheet.filename.split(".")[0]:
					return sheet
	def addSheet(self,sheet):
		self.worksheetname.append(sheet.filename.split(".")[0])
		
class CSVFile:
	def __init__(self,csvfile=None):
		if csvfile == None:
			self.matrix=[]
			self.filename=""
			self.colnames=["LD_ROWID"]
			self.idfield=""
		else:
			#print csvfile.filename
			self.filename=csvfile.filename
			self.matrix=copy.deepcopy(csvfile.matrix)
			self.colnames=copy.deepcopy(csvfile.colnames)
			self.idfield=csvfile.idfield		
	def importfile(self,csvfilename):
		dictlist=[]
		f=open(csvfilename,"rb")
		reader=UnicodeReader(f,delimiter=",",quotechar='"')
		colnames=reader.fieldnames
		rowid=0
		for row in reader:
			if row!=colnames and len(row)!=0:
				dictionary={}
				rowid+=1
				dictionary[u'LD_ROWID']=str(rowid)
				vals=row
				i=0
				if len(vals)!=len(colnames):
					print "Warning! Colnames and Vals dont match"
				for colname in colnames:	
					dictionary[colname]=vals[i]
					i+=1
				dictlist.append(dictionary)
		self.filename=os.path.split(csvfilename)[1]
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
			writer=UnicodeWriter(f2,delimiter=",",quotechar='"')
			writer.writerow(dict((fn,fn) for fn in fieldnames))
			for row in self.matrix:
				writer.writerow(row.values())
	def exportcols(self,excolnames):
		finalcsv=CSVFile()
		finalcsv.colnames=excolnames
		for row in self.matrix:
			dictionary={}
			for k,v in row.iteritems():
				if k in finalcsv.colnames:
					dictionary[k]=v
			finalcsv.matrix.append(dictionary)
		return finalcsv
	def deduplicaterows(self):
		finalcsv=CSVFile()
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
		finalcsv=CSVFile()
		finalcsv.colnames=self.colnames
		for row in self.matrix:
			dictionary=row
			dictionary[fieldname]=value
			finalcsv.matrix.append(dictionary)
		return finalcsv    
	def mergefields(self,fields,delimiter='|',include_fieldnames=False, nfieldname=""):
		finalcsv=CSVFile()
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
	def getallids(self):
		idlist=[]
		for row in self.matrix:
			idlist.append(row['LD_ROWID'])
		return idlist
	def filterids(self,filterstring,filtertype,col,case=False,delim=' ',idlist=[]):
		if idlist==[]:
			idlist=self.getallids()
		finalidlist=[]
		filterstring=filterstring.encode("utf-8")
		if case==False:
			filterstring=filterstring.upper()
		rows=self.getmatrix(idlist,self.colnames)
		for row in rows:
			filterflag=False
			checkstring=row[col]
			if case==False:
				checkstring=checkstring.upper()
			checkwords=set(checkstring.split(delim))
			filterstrings=filterstring.split(',')
			words=[]
			for string in filterstrings:
				words=words+string.split(delim)
			filterwords=set(words)
			if filtertype=="matchstringsany":
				for string in filterstrings:
					if string in checkstring:
						filterflag=True
					
			if filtertype=="matchstringsall":
				for string in filterstrings:
					if string in checkstring:
						filterflag=True
					else:
						filterflag=False
					
			if filtertype=="exact":
				for string in filterstrings:
					if string == checkstring:
						filterflag=True
			if filtertype=="matchwordsany":
				if len(filterwords&checkwords)>0:
					filterflag=True
		
			if filtertype=="matchwordsall":
				if filterwords&checkwords==filterwords:
					filterflag=True
			
			if filterflag==True:
					finalidlist.append(row[u'LD_ROWID'])
		return list(set(finalidlist))
	def printrows(self,idlist):
		for row in self.matrix:
			if row[u'LD_ROWID'] in idlist:
				print row
	def getmatrix(self,idlist,colnames):
		matrix=[]
		for row in self.matrix:
			dictionary={}
			for col in colnames:
				dictionary[col]=row[col]
			if row[u'LD_ROWID'] in idlist:
				matrix.append(dictionary)
		return matrix
	def padrows(self,padval="None"):
		for row in self.matrix:
			if len(row.keys())<len(self.colnames):
					colstoadd=list(set(self.colnames)-set(row.keys()))
					for col in colstoadd:
						row[col]=padval
	def prunerows(self):
		for row in self.matrix:
			if len(row.keys())>len(self.colnames):
					colstoprune=list(set(row.keys())-set(self.colnames))
					for col in colstoadd:
						row.pop(col)
	def updaterows(self,idlist,colnames,values):
		dictionary=packkeyvalues(colnames,values)
		if dictionary=={} or len(set(colnames)&set(self.colnames))<len(set(colnames)):
			print "Error"
			return
		for row in self.matrix:
			if row[u'LD_ROWID'] in idlist:
				for col in dictionary.keys():
					row[col]=dictionary[col]
		return
	
				

class CSVJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if not isinstance(obj, CSVFile):
            return super(MyEncoder, self).default(obj)
        return obj.__dict__

class CSVFileMerger:
    def __init__(self,csvl,csvr):
        self.mergedfile=CSVFile()
        self.mergekey=CSVFile()
        self.left=csvl
        self.right=csvr
        self.mergekey.colnames=["LEFT","RIGHT","MERGED"]
        self.rightwidth=len(csvr.colnames)
        self.rightlen=len(csvr.matrix)
        self.leftwidth=len(csvl.colnames)
        self.leftlen=len(csvl.matrix)
        self.mergedlen=0
        self.mergedwidth=0
        self.totallen=self.leftlen+self.rightlen
    def getinitialmergerkey(self):
        loopindex=max(self.leftwidth,self.rightwidth)
        for i in range(0,loopindex):
            dictionary={}
            try:
                leftval=self.left.colnames[i]
            except:
                leftval=""
            dictionary['LEFT']=leftval
            try:
                rightval=self.right.colnames[i]
            except:
                rightval=""
            dictionary['RIGHT']=rightval
            dictionary['MERGED']=""
            self.mergekey.matrix.append(dictionary)
        return self.mergekey
    def generatemergekey_interactive(self):
        newmergekey=CSVFile()
        newmergekey.colnames=["LEFT","RIGHT","MERGED"]
        headers_file1=self.left.colnames
        headers_file2=self.right.colnames
        for attributes1 in headers_file1:
            print '\nPlease select corresponding Attribute Number for <' + attributes1 + '> from:'
            for index, attributes2 in enumerate(headers_file2):
                print index, attributes2
            choice = raw_input('Enter Your Choice, write None if nothing matches:')
            dictionary={}
            dictionary["LEFT"]=attributes1
            while(1):
                if choice.lower() == 'none':
                    #matched_headers_file2.append('None')
                    dictionary["RIGHT"]=""
                    header_name = raw_input('Enter New Name for ' + attributes1 + ': ')
                    dictionary["MERGED"]=header_name
                    break
                else:
                    try:
                        val = int(choice)
                        if (int(choice) in range(len(headers_file2))):
                            dictionary["RIGHT"]=headers_file2[int(choice)]
                            header_name = raw_input('Enter New Name for ' + attributes1 + ' & ' + headers_file2[int(choice)] + ': ')
                            dictionary["MERGED"]=header_name
                            headers_file2.remove(headers_file2[int(choice)])
                            break
                    except ValueError:
                        choice = raw_input('Wrong Choice, Please Enter Your Again: ')
            newmergekey.matrix.append(dictionary)
            #print newmergekey.matrix
        for attributes2 in headers_file2:
            dictionary={}
            dictionary["LEFT"]=""
            dictionary["RIGHT"]=attributes2
            header_name = raw_input('Enter New Name for ' + attributes2 + ': ')
            dictionary["MERGED"]=header_name
            newmergekey.matrix.append(dictionary)
        return newmergekey
    def setfinalmergekey(self,csvfilename):
        self.mergekey.importfile(csvfilename)
    def mergefiles(self):
        mergedcols=[]
        for row in self.mergekey.matrix:
            mergedcols.append(row['MERGED'])
        self.mergedfile.colnames=mergedcols
        for leftrow in self.left.matrix:
            mergedict={}
            for col in self.mergedfile.colnames:
                for keyrow in self.mergekey.matrix:
                    if keyrow['MERGED']==col:
                        leftcol=keyrow['LEFT']
                        try:
                            mergedict[col]=leftrow[leftcol]
                        except:
                            mergedict[col]=""
            #print mergedict
            self.mergedfile.matrix.append(mergedict)
        #print self.mergedfile.matrix
        for rightrow in self.right.matrix:
            mergedict={}
            for col in self.mergedfile.colnames:
                for keyrow in self.mergekey.matrix:
                    if keyrow['MERGED']==col:
                        rightcol=keyrow['RIGHT']
                        try:
                            mergedict[col]=rightrow[rightcol]
                        except:
                            mergedict[col]=""
            self.mergedfile.matrix.append(mergedict)
        self.mergedlen=len(self.mergedfile.matrix)
        self.mergedwidth=len(self.mergedfile.colnames)

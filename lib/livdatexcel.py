import pandas
def importExcelFileAsDFList(pathtofile):
	dflist={}
	e=pandas.ExcelFile(pathtofile)
	for sheet in e.sheet_names:
		ws=e.parse(sheet)
		dflist[sheet]=ws
	return dflist

def createMergerSheet(dflist,pathtofile,mergersheetname):
	writer = pandas.ExcelWriter(pathtofile, engine="xlsxwriter")
	columnlengthlist=[]
	for sheet,matrix in dflist.iteritems():
		matrix.to_excel(writer,sheet,index=False)
		columnlengthlist.append(len(matrix))
	mergersheet=writer.book.add_worksheet(mergersheetname)
	rownum=0
	colnum=0
	mergersheet.write(rownum,colnum,"MergedSheet<CHANGE THIS CELL TO NEW SHEETNAME>")
	print columnlengthlist, max(columnlengthlist)
	for sheet,matrix in dflist.iteritems():
		colnum+=1
		mergersheet.write(rownum,colnum,sheet)
		mergersheet.write(rownum+1,colnum,matrix.columns.values[0])
		#print type(matrix.columns.values)
		mergersheet.data_validation(1,colnum,max(columnlengthlist),colnum, {'validate': 'list',
                                  'source': list(matrix.columns.values)})
	
		#mergersheet.data_validation(1,colnum,len(matrix.columns.values),colnum, {'validate': 'list',
                                  'source': list(matrix.columns.values)})
		#print rownum,colnum,sheet
	writer.save()
	
def exportDFListAsExcelFile(dflist,pathtofile):
	writer = pandas.ExcelWriter(pathtofile,engine="xlsxwriter")
	for sheet,matrix in dflist.iteritems():
		matrix.to_excel(writer,sheet,index=False)
	writer.save()

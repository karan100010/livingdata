import pandas

def getColRenameDict(mergersheet,sheet):
	colrenamedict={}
	originalcolnames=mergersheet[sheet].fillna("NA")
	newcolnames=mergersheet[mergersheet.columns[0]]
	for i in range(0,len(originalcolnames)):
		colrenamedict[originalcolnames[i]]=newcolnames[i]
	
	#	if originalcolnames[i]!="NA":
	#		colrenamedict[originalcolnames[i]]=newcolnames[i]
	return colrenamedict
def createMergedDFList(dflist,mergersheetname):
	altereddfs={}
	for sheet,matrix in dflist.iteritems():
		if sheet == mergersheetname:
			altereddfs[sheet]=matrix
			mergersheet=matrix
		else:
			df=matrix
			print df.columns
			columnrenamedict=getColRenameDict(mergersheet,sheet)
			print columnrenamedict
			altereddf=df.rename(columns=columnrenamedict)
			for key,value in columnrenamedict.iteritems():
				if key =="NA":
					altereddf[value]=0
			print df,altereddf
			altereddfs[sheet]=altereddf
	finalsheet=[]
	for sheet,matrix in altereddfs.iteritems():
		if sheet!=mergersheetname:
			finalsheet.append(matrix.fillna(0))
	finalsheetm=pandas.concat(finalsheet)
	finalsheetname=mergersheet.columns.values[0]
	altereddfs[finalsheetname]=finalsheetm
	return altereddfs

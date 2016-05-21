import sys
sys.path.append("../lib")
from livdatops import *
from livdatexcel import *

if __name__=="__main__":
	if ".xlsx" in sys.argv[1]:
		try:
			inputdata=importExcelFileAsDFList(sys.argv[1])
		except:
			print "Import Failed...is %s a .xlsx file in the path you said it would be?" %sys.argv[1]
			exit
	if len(sys.argv)<3:
		filename2=sys.argv[1].strip(".xlsx")+"-Merged.xlsx"
	else:
		filename2=sys.argv[2]
	mergedlist=createMergedDFList(inputdata,"Merger")
	print mergedlist.keys()
	exportDFListAsExcelFile(mergedlist,filename2)
	print "File created at %s" %filename2

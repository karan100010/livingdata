import sys,os,json
import csv
sys.path.append("../lib")
from livdatcsvlib import *
from livdatmaplib import *
if __name__=="__main__":
	csv=CSVFile()
	csv.importfile("/media/sf_CSV/WAW-MappingSheetSarEPul-Nov12.csv")
	csv1=add_loc_lat_long(csv,"Province")
	print csv1.colnames,len(csv1.colnames)
	sampleushahidi=CSVFile().importfile("/media/sf_CSV/sampleushahidi.csv")
	print sampleushahidi.colnames,len(sampleushahidi.colnames)
	csvmergefields1=csv1.mergefields(['Province', 'Referred By', 'Status'],delimiter=" ",include_fieldnames=True)
	print csvmergefields1.colnames,len(csvmergefields1.colnames)
	csvmergefields=csvmergefields1.mergefields(['S.No', 'Reg No',],delimiter=" ",include_fieldnames=True)
	print csvmergefields.colnames,len(csvmergefields.colnames)
	merger=CSVFileMerger(sampleushahidi,csvmergefields)
	#newmergekey=merger.generatemergekey_interactive()
	#merger.mergekey=newmergekey
	#merger.mergekey.exportfile("/media/sf_CSV/ushaidimergekey.csv")
	#newmergekey=CSVFile()
	#newmergekey.importfile("/media/sf_CSV/ushaidimergekey.csv")
	merger.setfinalmergekey("/media/sf_CSV/ushaidimergekey.csv")
	merger.mergefiles()
	finalcsv2=merger.mergedfile
	
	finalcsv3=finalcsv2.filldefaults("VERIFIED","YES")
	finalcsv4=finalcsv3.filldefaults("APPROVED","YES")
	finalcsv5=finalcsv4.filldefaults(" #","")
	for row in finalcsv5.matrix:
		print row
	finalcsv5.exportfile("/media/sf_CSV/WAW-MappingSheetSarEPul-Nov12-USHAHIDI.csv")
	
	#csv3=merger.getinitialmergerkey()
	#csv3.exportfile("/media/sf_CSV/sampleWAWUshahidiMergerKey.csv")
	
	#csv2=geocode_field_from_CSV(csv,"Province")
	#csv2.exportfile("/media/sf_CSV/locationop.csv")
	

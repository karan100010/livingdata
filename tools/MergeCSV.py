#Piyush's tool
import sys,os
sys.path.append("../lib")
from livdatcsvlib import *

file1 = sys.argv[1]
file2 = sys.argv[2]
file3 = sys.argv[3]

try:
    reader_file1 = CSVFile()
    reader_file1.importfile(file1)
    headers_file1 = reader_file1.colnames
    no_of_attributes_file1 = len(reader_file1.colnames)

    reader_file2 = CSVFile()
    reader_file2.importfile(file2)
    headers_file2 = reader_file2.colnames
    no_of_attributes_file2 = len(reader_file2.colnames)


    print '\nHeaders for First file are: ' + str(headers_file1)
    print '\nHeaders for Second file are: ' + str(headers_file2)


    if (no_of_attributes_file1>no_of_attributes_file2):
        merger=CSVFileMerger(reader_file1,reader_file2)
    else:
        merger=CSVFileMerger(reader_file2,reader_file1)
    newmergekey=merger.generatemergekey_interactive()
    newmergekey.exportfile("./tempmergekey")
    print "\n The new headers are mapped as follows:\n"
    os.system("cat ./tempmergekey")
    merger.mergekey=newmergekey
    merger.mergefiles()
    merger.mergedfile.exportfile(file3)

finally:
    print "Done"

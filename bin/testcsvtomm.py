import sys,os,json
import csv
sys.path.append("../lib")
from livdatfreemind import *

if __name__ == "__main__":
    csv_to_mm_file(sys.argv[1])


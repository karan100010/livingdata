#!/usr/bin/python
import os,sys, pandas, matplotlib
sys.path.append("/opt/livingdata/lib")
from livdatbender import *
from livdatcube import *
from sklearn.feature_extraction.text import CountVectorizer

def wordcounter():
	word_vectorizer = CountVectorizer(ngram_range=(1,3), analyzer='word')
	for year in d.cubedatadf.index:
		sparse_matrix = word_vectorizer.fit_transform(d.cubedatadf.yeardata[year].Customer)
		frequencies=sum(sparse_matrix).toarray()[0] 
		freqdf=pandas.DataFrame(frequencies, index=word_vectorizer.get_feature_names(), columns=[year]).sort_values(by=year)
		print freqdf

jughead=DataBender(sys.argv[1],headless=True,launchbrowser=False)

d=DataCube(src="remote",remotesheetname="ICANN's Cheeseburger Analysis",databender=jughead)

d.build_cube()
d.check_cube_data()
d.load_cube_data()
d.load_cube_calcsheets()
d.load_cube_dicts()

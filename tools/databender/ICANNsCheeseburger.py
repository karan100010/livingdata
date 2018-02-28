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


print "The datacube is stored in a variable named d and the bender is called jughead"	


jughead=DataBender(sys.argv[1],headless=True,launchbrowser=False)


d=DataCube(name=sys.argv[2],src="remote",remotesheetname=sys.argv[2],databender=jughead)

d.initmemory()



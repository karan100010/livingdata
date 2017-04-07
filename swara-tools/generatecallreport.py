import sys
sys.path.append("../lib")
from livdatswaralib import *
import datetime
if __name__=="__main__":
  d=Database("/etc/swara.conf")
  f=open("lastrunreports","rb")
  t=f.read().strip()
  print t
  f.close()
  #t=sys.argv[1]
  lastcheckedtime=datetime.datetime.strptime(t,"%Y-%m-%d %H:%M:%S")
  p=datetime.datetime.now()
  searchtime=p.strftime("%Y-%m-%d %H:%M:%S")
  filesuffix=p.strftime("%Y-%m-%d-%H-%M-%S")
  #print p
  reportspath="/home/arjun/SwaraReports/"
  df1=d.executeQueryAsPandas("SELECT * from callLog where timeOfCall > '%s'" %lastcheckedtime)
  print df1.to_csv(reportspath+"CallReport"+filesuffix,index_label="PandaID")
  df2=d.executeQueryAsPandas("SELECT * from lb_postings where posted > '%s'" %lastcheckedtime)
  print df2.to_csv(reportspath+"PostReport"+filesuffix,index_label="PandaID")
  
  f=open("lastrunreports","w")
  f.write(searchtime)
  f.close()
  

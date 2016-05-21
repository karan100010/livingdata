import sys
sys.path.append("../lib")
from livdatops import *
from livdatexcel import *

if __name__=="__main__":
  d=Database("/etc/swara.conf")
  df=d.executeQueryAsPandas("SELECT * from callLog")
  #a=df[df['user']=='8989161864']
  #print df.to_csv("/home/mojoarjun/test.csv",index_label="ID")
  #print len(df)

import sys
sys.path.append("../lib")
sys.path.append("/home/arjun/opt/mojomail/mojomail/")
from livdatswaralib import *
from mojomail import *
import datetime
if __name__=="__main__":
  # Get a database connection 
  d=Database("/etc/swara.conf")
  
  # Find out when we last ran the reports 
  f=open("lastrunreports","rb")
  t=f.read().strip()
  f.close()
 
  # Formatting and housekeeping
  lastcheckedtime=datetime.datetime.strptime(t,"%Y-%m-%d %H:%M:%S")
  p=datetime.datetime.now()
  searchtime=p.strftime("%Y-%m-%d %H:%M:%S")
  filesuffix=p.strftime("%Y%m%d-%H%M%S")
  reportspath="/home/arjun/SwaraReports/"
  
  # Get the calls
  df1=d.executeQueryAsPandas("SELECT * from callLog where timeOfCall > '%s'" %lastcheckedtime)
  numcalls=len(df1)
  filename1=reportspath+"CallReport-"+lastcheckedtime.strftime("%Y%m%d-%H%M%S")+"-to-"+filesuffix+".csv"
  df1.to_csv(filename1,index_label="PandaID")
  
  # Get the posts
  df2=d.executeQueryAsPandas("SELECT * from lb_postings where posted > '%s'" %lastcheckedtime)
  numposts=len(df2)
  filename2=reportspath+"PostReport-"+lastcheckedtime.strftime("%Y%m%d-%H%M%S")+"-to-"+filesuffix+".csv"
  df2.to_csv(filename2,index_label="PandaID")
  
  # Update the last run time
  f=open("lastrunreports","w")
  f.write(searchtime)
  f.close()
  
  # Open mailbox, open compose message
  m=MojoMailer("/home/arjun/SwaraMain.conf")
  mmsg=MojoMessage("/home/arjun/mm-SwaraReport.conf")
  
  subdict=mmsg.getsubdict()
  bodydict=mmsg.getbodydict()
  
  subdict['$IDENTIFIER']="MOJOMAIL"
  subdict['$TIMESTAMP']=searchtime
  
  bodydict['$RECIPIENT,']="Dataman"
  bodydict['$TIMESTAMP']=searchtime
  bodydict['$SERVERSIG']=m.serversig
  
  subdict['$TYPE']="SWARACALLREPORT"
  subdict['$META']=str(numcalls)
  subdict['$PAYLOAD']=filename1
  bodydict['$CONTENT']="Here is the call report between " + t + " and " + searchtime + "\n" + "Calls in this period: " + str(numcalls)
  cr=mmsg.composemessage("swaranetworkdata@gmail.com",subdict,bodydict,filename1)
  
  
  subdict['$TYPE']="SWARAPOSTREPORT"
  subdict['$META']=str(numposts)
  subdict['$PAYLOAD']=filename2
  bodydict['$CONTENT']="Here is the post report between " + t + " and " + searchtime + "\n" + "Posts in this period: " + str(numposts)
  pr=mmsg.composemessage("swaranetworkdata@gmail.com",subdict,bodydict,filename2)
 
  m.sendmsg(cr)
  m.sendmsg(pr)
  

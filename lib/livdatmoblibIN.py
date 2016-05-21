import os,sys
sys.path.append("../lib")
from livdatcsvlib import *


class MobileNumberList(CSVFile):


    def getcircleforseries(self,series):
        circlerow=""
        try:
          circlerow=os.popen("cat /home/mojoarjun/mscodes.csv | grep %s" %series).read().strip()
        except:
          print "Exception"
        if circlerow!="":
            circle=circlerow.split(",")[2]
        else :
            circle="Unknown Circle"
        if circle!="":
            return circle
        else:
            return "Unknown Circle"

    def add_circle(self,fieldname):
        finalcsv=CSVFile()
        finalcsv.colnames=self.colnames
        finalcsv.colnames=finalcsv.colnames+["TELECOM CIRCLE"]
        counter=len(self.matrix)
        for row in self.matrix:
            sys.stdout.write("\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b"+str(counter)+"|"+str(len(self.matrix)))
            counter-=1
            dictionary=row
            #print str(row[fieldname])[:5]
            try:
                series=str(row[fieldname])[:5]
            except:
                series="00000"
            #print series
            circle=self.getcircleforseries(series)
            dictionary['TELECOM CIRCLE']=circle
            finalcsv.matrix.append(dictionary)
                
        return finalcsv
                    

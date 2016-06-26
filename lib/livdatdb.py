'''
LIVINGDATA - COLLABORATIVE DYNAMIC DATASETS (C) 2016 ARJUN VENKATRAMAN

THIS PROGRAM IS FREE SOFTWARE: YOU CAN REDISTRIBUTE IT AND/OR MODIFY IT UNDER THE 
TERMS OF THE GNU GENERAL PUBLIC LICENSE AS PUBLISHED BY THE FREE SOFTWARE FOUNDATION, 
EITHER VERSION 3 OF THE LICENSE, OR (AT YOUR OPTION) ANY LATER VERSION.

THIS PROGRAM IS DISTRIBUTED IN THE HOPE THAT IT WILL BE USEFUL, BUT WITHOUT ANY 
WARRANTY; WITHOUT EVEN THE IMPLIED WARRANTY OF MERCHANTABILITY OR FITNESS FOR A 
PARTICULAR PURPOSE. SEE THE GNU GENERAL PUBLIC LICENSE FOR MORE DETAILS.

YOU SHOULD HAVE RECEIVED A COPY OF THE GNU GENERAL PUBLIC LICENSE ALONG WITH THIS PROGRAM. 
IF NOT, SEE HTTP://WWW.GNU.ORG/LICENSES/.

'''
#DB Functions

#import * safe
import MySQLdb
import refrom livdattable import *
import ConfigParser



class Database:
	def __init__(self,configfile):
		config=ConfigParser.ConfigParser()
		config.read(configfile)
		DB_USER = config.get("Database","username")
		DB_PASSWD = config.get("Database","password")
		DB_HOST = config.get("Database","host")
		DB_PORT = int(config.get("Database","port"))
		DB_NAME = config.get("Database","dbname")	
		self.db = MySQLdb.connect(port=DB_PORT,host=DB_HOST,user=DB_USER,passwd=DB_PASSWD)
		self.c = self.db.cursor()
		self.c.execute('USE '+DB_NAME+';')
	def getQueryAsTable(self, query):
		self.c.execute(query)
		output = self.c.fetchall()
		return output

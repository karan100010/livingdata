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

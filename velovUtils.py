import urllib
import json
from pprint import pprint
import psycopg2
import threading
import time

def fullfill(url, station, conn):
	
	# Load data from Web url
	page = urllib.urlopen(url)

	# Read data
	datajson = page.read()
	datajson = json.loads(datajson)

	# Recover station name from station integer
	name = toValidTableName(datajson['values'][station]['name'].encode('latin-1'))

	# Recover value et prepare sql insert
	availbike = datajson['values'][station]['available_bikes']
	lastupdate = datajson['values'][station]['last_update']
	
	try:
		sqlInsert = "INSERT INTO "+ name +" (available_bikes, last_update ) VALUES ( " + availbike + ", '" +  lastupdate + "')"

		# execute sql insert
		# conn = psycopg2.connect(database = "velov", user = "postgres", password = "", host = "localhost" ,port = "5432")
		cur = conn.cursor()
		cur.execute(sqlInsert)
		conn.commit()
		# conn.close()
	except:
		print name
		pass

def CreateTableFromStationLabel(url, station, conn):
	# Load data from Web url
	page = urllib.urlopen(url)

	# Read data
	datajson = page.read()
	datajson = json.loads(datajson)
	
	# Recover station name from station integer
	name = toValidTableName(datajson['values'][station]['name'].encode('latin-1'))

	try:
		# create table
		sqlCreate = "CREATE TABLE " + name + " (available_bikes INTEGER, last_update TIMESTAMP)" 
		# conn =psycopg2.connect(database = "velov", user = "postgres", password = "", host = "localhost" ,port = "5432")
		cur = conn.cursor()
		cur.execute(sqlCreate)
		conn.commit()
		# conn.close()
	except:
		pass

	return name

def toValidTableName(name):
	name = name.replace("/", "")
	name = name.replace(" ", "")
	name = name.replace("&", "")
	name = name.replace("'", "")
	name = name.replace("-", "")

	name = name.decode('latin-1')
	return  name

def ScrapDataJsonEveryNSeconds(url):
	while True:
		conn = psycopg2.connect(database = "velov", user = "postgres", password = "", host = "localhost" ,port = "5432")
		try:
			FillOnlyOneTable(url, conn)
		except: 
		 	print "Connexion lost"
		 	pass
		conn.close()
		print 'One more!'
		time.sleep(10)

def createAllTable(url):	
	page = urllib.urlopen(url)
	# Read data
	datajson = page.read()
	datajson = json.loads(datajson)
	l=len(datajson['values'])
	for station in range(0,l):
		CreateTableFromStationLabel(url, station)
		name = datajson['values'][station]['name']

def fullfillAllTable(url, conn):	
	page = urllib.urlopen(url)
	# Read data
	datajson = page.read()
	datajson = json.loads(datajson)
	l=len(datajson['values'])
	for station in range(0,15):
		fullfill(url, station, conn)
		name = datajson['values'][station]['name']

def FillOnlyOneTable(url, conn):
	# page = urllib.urlopen(url)
	# # Read data
	# datajson = page.read()
	# datajson = json.loads(datajson)
	a = open('Test.json', 'r') 
	datajson = a.read()
	datajson = json.loads(datajson)	
	
	sqlInsert = "INSERT INTO velovData (station_name, available_bikes, last_update) values ( "
	
	stationCount=len(datajson['values'])
	for station in range(0, stationCount):		
		# Recover value et prepare sql insert
		availbike = datajson['values'][station]['available_bikes']
		lastupdate = datajson['values'][station]['last_update']
		name = toValidTableName(datajson['values'][station]['name'].encode('latin-1'))
		sqlInsert = sqlInsert + str(station) + ", " + availbike + ", '" + lastupdate + "'), ("
	sqlInsert = sqlInsert[0:-3]
	
	cur = conn.cursor()
	cur.execute(sqlInsert)
	conn.commit()
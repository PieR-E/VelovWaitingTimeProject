# coding: utf8 
import urllib
import json
from pprint import pprint
import psycopg2
import threading
import time

def toValidTableName(name):
	name = name.replace(u"/", "")
	name = name.replace(u" ", "")
	name = name.replace(u"&", "")
	name = name.replace(u"'", "")
	name = name.replace(u"-", "")
	name = name.replace(u"é", "")
	name = name.replace(u"è", "")
	return  name

def ScrapDataJsonEveryNSeconds(url, N):
	while True:
		conn = psycopg2.connect(database = "velov", user = "postgres", password = "", host = "localhost" ,port = "5432")
		FillOnlyOneTable(url, conn)
		conn.close()
		time.sleep(N)

def FillOnlyOneTable(url, conn):
	attempt = 10
	while attempt>0:
		try:
			# # Load local json for test if there is no internet
			# a = open('Test.json', 'r') 
			# datajson = a.read()
			# datajson = json.loads(datajson)	
			page = urllib.urlopen(url)
			# Read data
			datajson = page.read()
			datajson = json.loads(datajson)
			break
		except:
			attempt = attempt-1
	if attempt > 0:

		# Load local json for test if there is no internet
		# a = open('Test.json', 'r') 
		# datajson = a.read()
		# datajson = json.loads(datajson)	
		
		sqlInsert = "INSERT INTO velovData (station_name, available_bikes, last_update, last_update_fme, status, bike_stands, available_bike_stands, availabilitycode) values ( "
		
		stationCount=len(datajson['values'])
		for station in range(0, stationCount):		
			# Recover value et prepare sql insert
			availbike = datajson['values'][station]['available_bikes']
			lastupdate = datajson['values'][station]['last_update']
			lastupdatefme = datajson['values'][station]['last_update_fme']
			status = datajson['values'][station]['status']
			bikestands = datajson['values'][station]['bike_stands']
			availbikestands = datajson['values'][station]['available_bike_stands']
			availabilitycode = datajson['values'][station]['availabilitycode']


			name = toValidTableName(datajson['values'][station][u'name'])
			

			sqlInsert = sqlInsert + str(station) + ", " + availbike + ", '" + lastupdate + "', '" + lastupdatefme + "', '" + status + "', " + bikestands + ", " + availbikestands + ", " + availabilitycode + "), ("
		sqlInsert = sqlInsert[0:-3]
		
		cur = conn.cursor()
		cur.execute(sqlInsert)
		conn.commit()
	else:
		print "Impossible to establish connexion"

def createStationLabelsCorrespondance(url, conn):
	# # Load local json for test if there is no internet
	# a = open('Test.json', 'r') 
	# datajson = a.read()
	# datajson = json.loads(datajson)	
	page = urllib.urlopen(url)
	# Read data
	datajson = page.read()
	datajson = json.loads(datajson)
	stationCount=len(datajson['values'])
	for station in range(0, stationCount):
		lat = datajson['values'][station]['lat']
		lng = datajson['values'][station]['lng']
		number = datajson['values'][station]['number']
		sqlInsert = 'insert into stationLabel (station_name, name, number, lat, lng) values (' + str(station) + ", '" + toValidTableName(datajson['values'][station][u'name']) + "', " + number + ", " + lat + ", " + lng + ")"
		cur = conn.cursor()
		cur.execute(sqlInsert)
		conn.commit()

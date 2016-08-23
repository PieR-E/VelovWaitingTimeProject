# coding: utf8 
import urllib
import json
from pprint import pprint
import psycopg2
import threading
import time
import velovUtils
import numpy as np
import scipy.stats as sc
import matplotlib.pyplot as plt
import pandas as pd
import sys
from datetime import timedelta

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

def rawdata2useful(station, hour):
    # Create sql statement for retrieve data from database
    conn = psycopg2.connect(database = "velov", user = "postgres", password = "", host = "localhost" ,port = "5432")
    sqlSelect = "select distinct last_update, available_bike_stands  from velovdatatemp where station_name =" + str(station) +" and extract(HOUR FROM last_update_fme) =" + str(hour) + " order by last_update"

	# Retrieve all data for station at given hour into a pandas.dataFrame style variable data
    cur = conn.cursor()
    cur.execute(sqlSelect)
    data = cur.fetchall()
    dataAsDF = pd.DataFrame(data)

    labels = ['last_update', 'avale_bike_stands']
    for columns_label in range(0, len(labels)):
         dataAsDF = dataAsDF.rename(columns = {columns_label : labels[columns_label]})

	# We must now handle all data for identify automatic update all 10 minuts. 
	# Algorithm which is applying : If t2 = t1 + 10 minuts then this update do not correspond to a real velov station change but to an automatic update. Therefore it's do not interest us.
    tmp = list( dataAsDF.last_update[i+1] - dataAsDF.last_update[i] for i in range(0,len(dataAsDF)-1))
    TenMinuts = timedelta(minutes = 10)

	# First add to dataAsDF column for duration between two update
    duration = [timedelta(seconds = 0)]+ tmp
    duration = list(duration[i].total_seconds() for i in range(0,len(duration)))
    dataAsDF = pd.concat([dataAsDF, pd.DataFrame(duration)], axis=1)

	# Then create list isValidUpdate which specify if update is valid
    isValidUpdate = [False] +list( (tmp[i] < TenMinuts)  for i in range(0, len(tmp)))

	# Then create list correctDuration which contain the duration of waiting time during two "Real" update.
    correctDuration = [duration[i] for i in range(0, (len(isValidUpdate)))]
    for Ocursor in range(0, len(isValidUpdate)-1):
        if isValidUpdate[Ocursor] == False and duration[Ocursor] > 0 and duration[Ocursor] < 650: # Ignore if last update is False and if duration lower than 650 ( in case of non continous data there will be ignored)
            correctDuration[Ocursor+1] = duration[Ocursor+1] + correctDuration[Ocursor]

    # Create list countMinuts which count minuts of waiting time
    countMinuts = list(int(correctDuration[i]/60) for i in range(0, len(correctDuration)))

    # Create final data frame with all new variable.
    dataFinal = list( data[i] + (isValidUpdate[i],) + (duration[i],) + (correctDuration[i],) + (countMinuts[i],) for i in range(0,len(isValidUpdate)))
    dataFinal= pd.DataFrame(dataFinal)
    labels = ['last_update', 'available_bike_stands', 'isvalidupdate', 'duration', 'correctedDuration', 'countMinuts']
    for Ocolumns in range(0, len(labels)):
        dataFinal = dataFinal.rename(columns = {Ocolumns : labels[Ocolumns]})

    # Then raw data are esay to handle with dataFinal data frame.
    useful = dataFinal.loc[dataFinal['available_bike_stands'] == 0] # Only time with no available bike stands
    useful = useful.loc[useful['isvalidupdate'] == True] # only valid update
    useful = useful.loc[useful['correctedDuration'] > 30] # Only duration upper than 30 sec. Some patern are recurent and might correspond to the claim : when we take a bike we often are with somebody else. Therefore  waiting time which are lower than 30 seconds are unavailable

    return useful	
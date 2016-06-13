# coding: utf8 
from __future__ import division
import urllib
import json
from pprint import pprint
import psycopg2
import threading
import velovUtils
import time
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys
from datetime import timedelta

print sys.version
conn = psycopg2.connect(database = "velov", user = "postgres", password = "", host = "localhost" ,port = "5432")
url = 'https://download.data.grandlyon.com/ws/rdata/jcd_jcdecaux.jcdvelov/all.json'
# velovUtils.createStationLabelsCorrespondance(url, conn)
sqlSelect = "select distinct last_update, available_bike_stands from velovdatatemp where last_update> '01/05/2016' and station_name = 11 order by last_update"
# sqlSelect = "select distinct last_update, available_bike_stands  from velovdata where station_name = 111 and  ( extract(HOUR FROM last_update_fme) = 19 or extract(HOUR FROM last_update_fme) = 20 or extract(HOUR FROM last_update_fme) = 21 ) order by last_update"
sqlSelectName = "select column_name from information_schema.columns where table_name = 'velovdata'"
# sqlSelect = "select * from velovdata where station_name = 11 and  ( extract(HOUR FROM last_update_fme) = 20 or extract(HOUR FROM last_update_fme) = 21 ) and (last_update_fme > '2016-05-08')"
cur = conn.cursor()
cur.execute(sqlSelect)
data = cur.fetchall()
#
#tmp = list( data[i][0] for i in range(0,len(data)-1))
#tmp2 = list( data[i][0] for i in range(1,len(data)))
#isUpdated = list(tmp[i] != tmp2[i] for i in range(0, len(tmp)))
#isUpdated = isUpdated+[False]
#

#cur.execute(sqlSelectName)
#labels = cur.fetchall()
dataAsDF = pd.DataFrame(data)

labels = ['last_update', 'avale_bike_stands']
for columns_label in range(0, len(labels)):
    dataAsDF = dataAsDF.rename(columns = {columns_label : labels[columns_label]})

# We must handle all data for identify automatic update all 10 minuts. 
# Algorithm which is applying : If t2 = t1 + 10 minuts +/- e then this update do not correspond to a real velov change but to an automatic update 
# e represent error because the automatic update are not exactly all ten minuts. e = 30 seconds
tmp = list( dataAsDF.last_update[i+1] - dataAsDF.last_update[i] for i in range(0,len(dataAsDF)-1))
TenMinuts = timedelta(minutes = 10)
e = timedelta(seconds = 30)

# First add column for duration betweento update
duration = [timedelta(seconds = 0)]+ tmp
duration = list(duration[i].total_seconds() for i in range(0,len(duration)))
dataAsDF = pd.concat([dataAsDF, pd.DataFrame(duration)], axis=1)

#labels = ['last_update', 'available_bike_stands', 'duration']
#for columns_label in range(0, len(labels)):
#    dataAsDF = dataAsDF.rename(columns = {columns_label : labels[columns_label]})

# Then specify if update is valid
isValidUpdate = [False] +list( (tmp[i] < TenMinuts)  for i in range(0, len(tmp)))

correctDuration = duration
for Ocursor in range(0, len(isValidUpdate)-1):
    if isValidUpdate[Ocursor] == False and duration[Ocursor] > 0 and duration[Ocursor] < 650:
        correctDuration[Ocursor+1] = duration[Ocursor+1] + duration[Ocursor]

dataFinal = list( data[i] + (isValidUpdate[i],) + (duration[i],) + (correctDuration[i],) for i in range(0,len(isValidUpdate)))

dataFinal= pd.DataFrame(dataFinal)
labels = ['last_update', 'available_bike_stands', 'isvalidupdate', 'duration', 'correctedDuration']
for Ocolumns in range(0, len(labels)):
    dataFinal = dataFinal.rename(columns = {Ocolumns : labels[Ocolumns]})


test = dataFinal.loc[dataFinal['available_bike_stands'] == 0]
test = test.loc[test['isvalidupdate'] == True]
plt.hist(list(test.duration), 200)
plt.show()
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
import scipy.stats as sc
import matplotlib.pyplot as plt
import pandas as pd
import sys
from datetime import timedelta
from operator import itemgetter

station = 11

# Create sql statement for retrieve data from database
conn = psycopg2.connect(database = "velov", user = "postgres", password = "", host = "localhost" ,port = "5432")
sqlSelect = "select lat, lng from stationlabel where station_name =" + str(station)

	# Retrieve all data for station at given hour into a pandas.dataFrame style variable data#
cur = conn.cursor()
cur.execute(sqlSelect)
data = cur.fetchall()
lat = data[0][0] # retrieve latitude
lng = data[0][1] # retrieve longitude


sqlSelect = "select station_name, lat, lng from stationlabel where station_name <>" + str(station)
cur = conn.cursor()
cur.execute(sqlSelect)
data = cur.fetchall()
dataAsDF = pd.DataFrame(data)
labels = ['station_name', 'lat', 'lng']
for columns_label in range(0, len(labels)):
    dataAsDF = dataAsDF.rename(columns = {columns_label : labels[columns_label]})

latdiff = np.abs(dataAsDF.lat - lat)
lngdiff = np.abs(dataAsDF.lng - lng)

toSort = list((data[i][0],) + (np.sqrt(latdiff[i]*latdiff[i] + lngdiff[i]*lngdiff[i]),) for i in range(0, len(latdiff)))
toSort = sorted(toSort, key = itemgetter(1))

# Retrieve nearest station_name identifier
nearest_station = list(toSort[i][0] for i in range(0,len(toSort)))

for N in range(0,5):
    sqlSelect = "select name from stationlabel where station_name =" + str(nearest_station[N])
    cur = conn.cursor()
    cur.execute(sqlSelect)
    station = cur.fetchall()
    print station
    
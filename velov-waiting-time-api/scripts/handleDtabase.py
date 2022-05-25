import psycopg2
import urllib
import json
import populateStations
import pandas as pd
from datetime import timedelta
import datetime
import seaborn as sns
from scipy.stats import exponweib

url = 'https://download.data.grandlyon.com/ws/rdata/jcd_jcdecaux.jcdvelov/all.json'

conn = psycopg2.connect(database = "velov", 
                        user = "dev", 
                        password = "velov", 
                        host = "localhost" ,
                        port = "5432")

sqlDropStationsHours = "DROP TABLE stations_hours"
sqlCreateStationsHours = "CREATE TABLE stations_hours (station_id integer, hour integer, exponentiation numeric, shape numeric, loc numeric, scale numeric, PRIMARY KEY(station_id, hour))"
sqlDropStations = "DROP TABLE stations"
sqlCreateStations = "CREATE TABLE stations (station_id integer PRIMARY KEY, name character varying(50), number integer, lat integer, lng integer, bike_stands integer, address character varying(50), code_insee integer, commune character varying(20))"
sqlDropStationsData = "DROP TABLE stations_data"
sqlCreateStationsData = "CREATE TABLE stations_data ( station_id integer, available_bikes integer, last_update timestamp without time zone, last_update_fme timestamp without time zone, status character varying(20), available_bike_stands integer, availabilitycode integer )"

cur = conn.cursor()
cur.execute(sqlDropStations)
cur.execute(sqlDropStationsData)
cur.execute(sqlDropStationsHours)
cur.execute(sqlCreateStationsHours)
cur.execute(sqlCreateStationsData)
cur.execute(sqlCreateStations)
conn.commit()

# Populate stations
populateStations.createStationLabelsCorrespondance(url, conn)

print('all good')
# coding: utf8 
import random
import psycopg2
import urllib
import urllib.request
import json

conn = psycopg2.connect(database = "velov",
                        user = "dev",
                        password = "velov",
                        host = "localhost",
                        port = "5432")

url = 'https://download.data.grandlyon.com/ws/rdata/jcd_jcdecaux.jcdvelov/all.json'

def getWeibullParam(station_id, hour):
  # Fake for now
  exponentiation = random.uniform(0, 1)
  shape = random.uniform(0, 1)
  loc = random.uniform(0, 1)
  scale = random.uniform(0, 1)
  return exponentiation, shape, loc, scale

def createStationHours(url, conn):
    page = urllib.request.urlopen(url)
    datajson = page.read()
    datajson = json.loads(datajson)
    stationCount = len(datajson['values'])
    for station in range(0, stationCount):
      for hour in range(0, 23):
        station_id = datajson['values'][station]['number']

        exponentiation, shape, loc, scale = getWeibullParam(station_id, hour)

        sqlInsert = 'insert into stations_hours (station_id, hour, exponentiation, shape, loc, scale) values (' + str(
            station_id) + ", " + str(hour) + ", " + str(exponentiation) + ", "+ str(shape) + ", " + str(loc) + ", " + str(scale) + ")"

        cur = conn.cursor()
        cur.execute(sqlInsert)
        conn.commit()

sqlDropStationsHours = "DROP TABLE stations_hours"
sqlCreateStationsHours = "CREATE TABLE stations_hours (station_id integer, hour integer, exponentiation numeric, shape numeric, loc numeric, scale numeric, PRIMARY KEY(station_id, hour))"
cur = conn.cursor()
cur.execute(sqlDropStationsHours)
cur.execute(sqlCreateStationsHours)
conn.commit()

createStationHours(url, conn)

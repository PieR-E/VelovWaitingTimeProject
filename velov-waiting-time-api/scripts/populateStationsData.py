# coding: utf8 
import urllib
import urllib.request
import json
from pprint import pprint
import psycopg2
import threading
import time

conn = psycopg2.connect(database = "velov",
                        user = "dev",
                        password = "velov",
                        host = "localhost",
                        port = "5432")

url = 'https://download.data.grandlyon.com/ws/rdata/jcd_jcdecaux.jcdvelov/all.json'

def toValidTableName(name):
    name = name.replace(u"/", "")
    name = name.replace(u"&", "")
    name = name.replace(u"'", "")
    name = name.replace(u"-", "")
    name = name.replace(u"é", "e")
    name = name.replace(u"è", "e")
    name = name.replace(u"'", "")
    return name

def ScrapDataJsonEveryNSeconds(url, N):
    while True:
        conn = psycopg2.connect(database="velov",
                                user="dev",
                                password="velov",
                                host="localhost",
                                port="5432")
        FillOnlyOneTable(url, conn)
        conn.close()
        time.sleep(N)

def FillOnlyOneTable(url, conn):
    attempt = 10
    while attempt > 0:
        try:
            page = urllib.request.urlopen(url)
            # Read data
            datajson = page.read()
            datajson = json.loads(datajson)
            break
        except Exception as e:
            print(e)
            attempt = attempt - 1
    if attempt > 0:

        sqlInsert = "INSERT INTO stations_data (station_id, available_bikes, last_update, last_update_fme, status, available_bike_stands, availabilitycode) values ( "

        stationCount = len(datajson['values'])

        # fileJson = open("data.json", "w")
        # json.dump(datajson, fileJson)
        # fileJson.close()

        for station in range(0, stationCount):
            # Recover value et prepare sql insert
            availbike = str(datajson['values'][station]['available_bikes'])

            lastupdate = datajson['values'][station]['last_update']
            lastupdatefme = datajson['values'][station]['last_update_fme']
            status = datajson['values'][station]['status']
            availbikestands = str(datajson['values'][station]['available_bike_stands'])
            availabilitycode = str(datajson['values'][station]['availabilitycode'])
            station_id = datajson['values'][station]['number']

            # if station_id == 10059:
            #     print(datajson['values'][station]['number'])
            #     print(availbike)
            #     print(datajson['values'][station]['available_bikes'])

            sqlInsert = sqlInsert + str(
                station_id) + ", " + availbike + ", '" + lastupdate + "', '" + lastupdatefme + "', '" + status + "', " + availbikestands + ", " + availabilitycode + "), ("

        sqlInsert = sqlInsert[0:-3]

        cur = conn.cursor()
        cur.execute(sqlInsert)
        conn.commit()
    else:
        print("Impossible to establish connexion")

sqlDropStationsData = "DROP TABLE stations_data"
sqlCreateStationsData = "CREATE TABLE stations_data ( station_id integer, available_bikes integer, last_update timestamp without time zone, last_update_fme timestamp without time zone, status character varying(20), available_bike_stands integer, availabilitycode integer )"
cur = conn.cursor()
cur.execute(sqlDropStationsData)
cur.execute(sqlCreateStationsData)
conn.commit()

ScrapDataJsonEveryNSeconds(url, 15)

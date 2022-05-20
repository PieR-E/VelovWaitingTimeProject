# coding: utf8 
from pprint import pprint
import psycopg2
import urllib
import urllib.request
import time
import json

conn = psycopg2.connect(database = "velov",
                        user = "dev",
                        password = "velov",
                        host = "localhost",
                        port = "5432")

url = 'https://download.data.grandlyon.com/ws/rdata/jcd_jcdecaux.jcdvelov/all.json'

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
        for station in range(0, stationCount):
            # Recover value et prepare sql insert
            availbike = str(datajson['values'][station]['available_bikes'])
            lastupdate = datajson['values'][station]['last_update']
            lastupdatefme = datajson['values'][station]['last_update_fme']
            status = datajson['values'][station]['status']
            availbikestands = str(datajson['values'][station]['available_bike_stands'])
            availabilitycode = str(datajson['values'][station]['availabilitycode'])

            sqlInsert = sqlInsert + str(
                station) + ", " + availbike + ", '" + lastupdate + "', '" + lastupdatefme + "', '" + status + "', " + availbikestands + ", " + availabilitycode + "), ("

        sqlInsert = sqlInsert[0:-3]

        cur = conn.cursor()
        cur.execute(sqlInsert)
        conn.commit()
    else:
        print("Impossible to establish connexion")

ScrapDataJsonEveryNSeconds(url, 15)

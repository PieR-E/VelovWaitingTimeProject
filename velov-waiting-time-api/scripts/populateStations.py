# coding: utf8 
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

def toValidTableName(name):
    name = name.replace(u"/", "")
    name = name.replace(u"&", "")
    name = name.replace(u"'", "")
    name = name.replace(u"-", "")
    name = name.replace(u"é", "e")
    name = name.replace(u"è", "e")
    name = name.replace(u"'", "")
    return name

def createStationLabelsCorrespondance(url, conn):
    page = urllib.request.urlopen(url)
    datajson = page.read()
    datajson = json.loads(datajson)
    stationCount = len(datajson['values'])
    for station in range(0, stationCount):
        address = str(datajson['values'][station]['address'])
        code_insee = str(datajson['values'][station]['code_insee'])
        commune = str(datajson['values'][station]['commune'])
        bikestands = str(datajson['values'][station]['bike_stands'])
        lat = datajson['values'][station]['lat']
        lng = datajson['values'][station]['lng']
        number = datajson['values'][station]['number']
        name = datajson['values'][station][u'name']

        if name is not None:
            name = toValidTableName(name)
        else:
            name = ''

        if address is not None:
            address = toValidTableName(address)
        else: 
            address = ''

        if commune is not None:
            commune = toValidTableName(commune)
        else: 
            commune = ''

        if code_insee == 'None':
            code_insee = 0
        
        sqlInsert = 'insert into stations (station_id, name, number, lat, lng, bike_stands, address, code_insee, commune) values (' + str(
            number) + ", '" + f'{name}' + "', " + str(number) + ", " + lat + ", " + lng + ", " + str(bikestands) + ", '" + f'{address}' + "', " + str(code_insee) + ", '" + f'{commune}' + "')"

        cur = conn.cursor()
        cur.execute(sqlInsert)
        conn.commit()

sqlDropStations = "DROP TABLE stations"
sqlCreateStations = "CREATE TABLE stations (station_id integer PRIMARY KEY, name character varying(50), number integer, lat numeric, lng numeric, bike_stands integer, address character varying(50), code_insee integer, commune character varying(20))"
cur = conn.cursor()
cur.execute(sqlDropStations)
cur.execute(sqlCreateStations)
conn.commit()

createStationLabelsCorrespondance(url, conn)

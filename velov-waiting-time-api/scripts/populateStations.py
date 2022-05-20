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
    name = name.replace(u" ", "")
    name = name.replace(u"&", "")
    name = name.replace(u"'", "")
    name = name.replace(u"-", "")
    name = name.replace(u"é", "")
    name = name.replace(u"è", "")
    name = name.replace(u"'", "")
    return name

def createStationLabelsCorrespondance(url, conn):
    print('hello')
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
            station) + ", '" + toValidTableName(name) + "', " + str(number) + ", " + str(lat) + ", " + str(lng) + ", " + str(bikestands) + ", '" + toValidTableName(address) + "', " + str(code_insee) + ", '" + toValidTableName(commune) + "')"

        cur = conn.cursor()
        cur.execute(sqlInsert)
        conn.commit()

createStationLabelsCorrespondance(url, conn)

# coding: utf8 
import urllib
import json
from pprint import pprint
import psycopg2
import threading
import velovUtils
import time


conn = psycopg2.connect(database = "velov", user = "postgres", password = "", host = "localhost" ,port = "5432")
url = 'https://download.data.grandlyon.com/ws/rdata/jcd_jcdecaux.jcdvelov/all.json'
# velovUtils.createStationLabelsCorrespondance(url, conn)
velovUtils.ScrapDataJsonEveryNSeconds(url, 5)

# page = urllib.urlopen(url)

# 	# Read data
# datajson = page.read()
# datajson = json.loads(datajson)
# print len(datajson['values'])


# station = 1
# # velovUtils.CreateTableFromStationLabel(url, station)
# velovUtils.fullfill(url, station)



# # Lire url puis recup chaine JSON
# page = urllib.urlopen('https://download.data.grandlyon.com/ws/rdata/jcd_jcdecaux.jcdvelov/all.json')
# test = page.read()
# test = json.loads(test)

# # print "Pour la station", test['values'][110]['name'], "il y a ", test[u'values'][110]['available_bikes'], "veloV diponible."



# List all the station

# name = test['values'][0]['name'].encode('latin-1')
# name = name.replace("/", "")
# name = name.replace(" ", "")
# name = name.decode('latin-1')
# print name


# sqlCreate = "CREATE TABLE  test ( Id INTEGER,  " + test['fields'][14] + " INTEGER )" 
# conn =psycopg2.connect(database = "velov", user = "postgres", password = "", host = "localhost" ,port = "5432")
# cur = conn.cursor()
# cur.execute(sqlCreate)
# conn.commit()
# conn.close()

# sql = "select * from test"
# conn =psycopg2.connect(database = "velov", user = "postgres", password = "", host = "localhost" ,port = "5432")
# cur = conn.cursor()
# cur.execute(sql)
# res = cur.fetchall()

# print len(res)

# conn.commit()
# conn.close()



# # len(test['values'])
# for VeloVstation in range(1,2):
# 	sqlInsert = 'INSERT INTO VELOV ('

# 	for VeloVstationAttribute in range(0,len(test['fields'])):
# 		sqlInsert = sqlInsert + test['fields'][VeloVstationAttribute] + ', '
# 	sqlInsert = sqlInsert[0:-2] + ') VALUES ('
	
# 	for VeloVstationAttribute in range(0,len(test['fields'])):
# 			test['values'][VeloVstation][test['fields'][VeloVstationAttribute]] = test['values'][VeloVstation][test['fields'][VeloVstationAttribute]].replace(" ", "")
# 			print type(test['values'][VeloVstation][test['fields'][VeloVstationAttribute]])
# 			sqlInsert = sqlInsert + test['values'][VeloVstation][test['fields'][VeloVstationAttribute]] + ', '
		
# 	sqlInsert = sqlInsert[0:-2] + ')'
# 	sqlInsert = sqlInsert.encode('latin-1')

# 	print(sqlInsert)
# 	f = open('Test.txt', 'w')
# 	f.write(sqlInsert)


# 	cur = conn.cursor()
# 	cur.execute(sqlInsert)
# 	conn.commit()
# 	conn.close();


# with open('Test.json', 'w') as f:
# 	json.dump(test, f, indent=1)

# Creation table

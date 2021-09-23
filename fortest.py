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


print sys.version
conn = psycopg2.connect(database = "velov", user = "postgres", password = "", host = "localhost" ,port = "5432")
url = 'https://download.data.grandlyon.com/ws/rdata/jcd_jcdecaux.jcdvelov/all.json'
# velovUtils.createStationLabelsCorrespondance(url, conn)

sqlSelect = "select distinct last_update, available_bike_stands  from velovdatatemp where station_name = 11 and extract(HOUR FROM last_update_fme) = 20 order by last_update"
# sqlSelect = "select distinct last_update, available_bike_stands from velovdatatemp where station_name = 11 order by last_update"

sqlSelectName = "select column_name from information_schema.columns where table_name = 'velovdata'"
# sqlSelect = "select * from velovdata where station_name = 11 and  ( extract(HOUR FROM last_update_fme) = 20 or extract(HOUR FROM last_update_fme) = 21 ) and (last_update_fme > '2016-05-08')"
cur = conn.cursor()
cur.execute(sqlSelect)
data = cur.fetchall()

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

# First add column for duration between two update
duration = [timedelta(seconds = 0)]+ tmp
duration = list(duration[i].total_seconds() for i in range(0,len(duration)))
dataAsDF = pd.concat([dataAsDF, pd.DataFrame(duration)], axis=1)

#labels = ['last_update', 'available_bike_stands', 'duration']
#for columns_label in range(0, len(labels)):
#    dataAsDF = dataAsDF.rename(columns = {columns_label : labels[columns_label]})

# Then specify if update is valid
isValidUpdate = [False] +list( (tmp[i] < TenMinuts)  for i in range(0, len(tmp)))

correctDuration = [duration[i] for i in range(0, (len(isValidUpdate)))]
for Ocursor in range(0, len(isValidUpdate)-1):
    if isValidUpdate[Ocursor] == False and duration[Ocursor] > 0 and duration[Ocursor] < 650:
        correctDuration[Ocursor+1] = duration[Ocursor+1] + correctDuration[Ocursor]

# Create list which count minuts
countMinuts = list(int(correctDuration[i]/60) for i in range(0, len(correctDuration)))

dataFinal = list( data[i] + (isValidUpdate[i],) + (duration[i],) + (correctDuration[i],) + (countMinuts[i],) for i in range(0,len(isValidUpdate)))

dataFinal= pd.DataFrame(dataFinal)
labels = ['last_update', 'available_bike_stands', 'isvalidupdate', 'duration', 'correctedDuration', 'countMinuts']
for Ocolumns in range(0, len(labels)):
    dataFinal = dataFinal.rename(columns = {Ocolumns : labels[Ocolumns]})



## Test 0 : do some plot
test = dataFinal.loc[dataFinal['available_bike_stands'] == 0]
test = test.loc[test['isvalidupdate'] == True]

# Some patern are recurent and might correspond to the claim : when we take a bike we often go with somebody else
# Therefore  waiting time which are lower than 10 seconds are unavailable
test = test.loc[test['correctedDuration'] > 10]


# test = test.loc[test['correctedDuration'] < 200]

# plt.hist(list(test.correctedDuration), 100)


longestTime= test.loc[test['correctedDuration'] > 300]

## Test 1 : consider X like the number of minuts it's necessaryt to wait forand test if it's follow poisson law



isPoisson = dataFinal.loc[dataFinal['available_bike_stands'] == 0]
isPoisson = isPoisson.loc[isPoisson['isvalidupdate'] == True]
isPoisson = isPoisson.loc[isPoisson['correctedDuration'] > 30]
# isPoisson = isPoisson.loc[isPoisson['correctedDuration'] < 2000]

# plt.hist(list(isPoisson.correctedDuration), 100)
# plt.show()


poissontheo = np.random.poisson(5, len(isPoisson.countMinuts))
# plt.hist(list(poissontheo), 100)
#plt.show()

exptheo = np.random.exponential((np.mean(isPoisson.correctedDuration)), len(isPoisson.countMinuts))
# plt.hist(list(exptheo), 100)
#plt.show()

dd = isPoisson.correctedDuration
expTest = sc.kstest(dd.tolist(), 'expon', (np.mean(isPoisson.correctedDuration),))
# print(expTest)

weiTest = sc.kstest(dd.tolist(), 'dweibull', (np.mean(isPoisson.correctedDuration),))
# print(weiTest)

from scipy.stats import exponweib
weibulltheo = exponweib.rvs(85, 0.3, size=len(isPoisson.countMinuts))
#plt.hist(list(weibulltheo), 100)

weibulltheo = exponweib.rvs(1, 0.5, loc=0, scale=1, size=len(isPoisson.countMinuts))
estim = exponweib.fit(dd.tolist())
expweibulltest = sc.ks_2samp(dd.tolist(), exponweib.rvs(estim[0], estim[1], loc=estim[2], scale=estim[3], size=len(isPoisson.countMinuts)))
print(expweibulltest)

p = sc.probplot(dd, dist = sc.exponweib, sparams =(estim[0], estim[1], estim[2], estim[3]), fit = True, plot=plt)
plt.show()



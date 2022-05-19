# coding: utf8 
import urllib
import json
from pprint import pprint
import psycopg2
import threading
import velovUtils
import time

conn = psycopg2.connect(database = "velov",
                        user = "dev",
                        password = "velov",
                        host = "localhost",
                        port = "5432")

url = 'https://download.data.grandlyon.com/ws/rdata/jcd_jcdecaux.jcdvelov/all.json'

velovUtils.ScrapDataJsonEveryNSeconds(url, 5)

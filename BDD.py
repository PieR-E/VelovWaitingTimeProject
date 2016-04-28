import psycopg2

conn =psycopg2.connect(database = "velov", user = "postgres", password = "", host = "localhost" ,port = "5432")
# sql_table = "CREATE TABLE VELOV (" \
#             "number INTEGER NOT NULL," \
#             "name VARCHAR(36) NOT NULL," \
#             "address VARCHAR(65) NOT NULL," \
#             "address2 VARCHAR(48)," \
#             "commune VARCHAR(16) NOT NULL," \
#             "nmarrond INTEGER," \
#             "bonus VARCHAR(3) NOT NULL," \
#             "pole VARCHAR(61) NOT NULL," \
#             "lat DECIMAL(18) NOT NULL," \
#             "lng DECIMAL(18) NOT NULL," \
#             "bike_stands INTEGER NOT NULL," \
#             "status VARCHAR(6) NOT NULL," \
#             "available_bike_stands INTEGER NOT NULL," \
#             "available_bikes INTEGER NOT NULL," \
#             "availabilitycode INTEGER NOT NULL," \
#             "availability VARCHAR(6) NOT NULL," \
#             "banking VARCHAR(5) NOT NULL," \
#             "gid INTEGER NOT NULL," \
#             "last_update TIMESTAMP WITHOUT TIME ZONE NOT NULL," \
#             "last_update_fme TIMESTAMP WITHOUT TIME ZONE NOT NULL)"
sql = "select * from velov"
cur = conn.cursor()
res = cur.execute(sql)
print res
conn.commit()
conn.close();

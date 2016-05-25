drop table velovData;
create table velovData (station_name INTEGER, available_bikes INTEGER, last_update TIMESTAMP, last_update_fme TIMESTAMP, status varchar(20), lat float, lng float, bike_stands integer, available_bike_stands integer)
create table stationLabel (station_name INTEGER, name VARCHAR, number INTEGER, lat float, lng float)
/* sudo -i -u postgres psql */

CREATE DATABASE velovTest;
CREATE USER dev PASSWORD 'velov';
\c velov;

CREATE TABLE stations_data ( station_id integer, available_bikes integer, last_update timestamp without time zone, last_update_fme timestamp without time zone, status character varying(20), available_bike_stands integer, availabilitycode integer );

CREATE TABLE stations (station_id integer, name character varying(50), number integer, lat integer, lng integer, bike_stands integer, address character varying(50), code_insee integer, commune character varying(20), PRIMARY KEY (station_id) );

CREATE TABLE stations_hours (station_id integer, hour integer, exponentiation numeric, shape numeric, loc numeric, scale numeric, PRIMARY KEY (station_id, hour) );

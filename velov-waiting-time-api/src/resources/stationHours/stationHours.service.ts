import type {StationHour} from '~/types/stationHour'

const pgp = require('pg-promise')({});
const connectionString = `postgres://${process.env.DB_USERNAME}:${process.env.DB_PASSWORD}@${process.env.DB_HOST}:${process.env.DB_PORT}/${process.env.DB_DATABASE}`;
const db = pgp(connectionString);

export class StationHoursService {
    TABLE_NAME = 'station_hours';

    stationHours: StationHour[] = [
        {station_id: 0, hour: 1},
        {station_id: 0, hour: 2},
        {station_id: 1, hour: 2},
        {station_id: 2, hour: 1},
    ]

    async findAll(): Promise<StationHour[]> {
        return db.any(`SELECT * FROM "${this.TABLE_NAME}"`)
    }

    async findHoursByStationId(id: number): Promise<StationHour[]> {
        return db.many(`SELECT * FROM "${this.TABLE_NAME}" WHERE station_id = ${id}`)
    }

    async findOne(id: number, hour: number): Promise<StationHour | undefined> {
        return db.one(`SELECT * FROM "${this.TABLE_NAME}" WHERE station_id = ${id} AND hour = ${hour}`)
    }
}

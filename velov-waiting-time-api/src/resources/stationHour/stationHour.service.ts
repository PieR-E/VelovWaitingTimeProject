import type {StationHour} from '~/types/stationHour'

const pgp = require('pg-promise')({});
const connectionString = `postgres://${process.env.DB_USERNAME}:${process.env.DB_PASSWORD}@${process.env.DB_HOST}:${process.env.DB_PORT}/${process.env.DB_DATABASE}`;
console.log(connectionString);
const db = pgp(connectionString);
const tableName = 'stationDataByHour';

export class StationHourService {
    stationHours: StationHour[] = [
        {id: 0, hour: 1, stationName: 'test'},
        {id: 0, hour: 2, stationName: 'test'},
        {id: 1, hour: 2, stationName: 'test 2'},
        {id: 2, hour: 1, stationName: 'test 3'},
    ]

    async findAll(): Promise<StationHour[]> {
        return db.any(`SELECT * FROM "${tableName}"`)
    }

    async findStationAll(id: number): Promise<StationHour[]> {
        return db.many(`SELECT * FROM "${tableName}" WHERE id = ${id}`)
    }

    async findOne(id: number, hour: number): Promise<StationHour | undefined> {
        return db.one(`SELECT * FROM "${tableName}" WHERE id = ${id} AND hour = ${hour}`)
    }
}

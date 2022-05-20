import {db_connection} from '~/resources/database';
import type {StationsHour} from '~/types/stationsHour'

export class StationsHoursService {
    TABLE_NAME = 'stations_hours';

    async findAll(): Promise<StationsHour[]> {
        return db_connection.any(`SELECT * FROM "${this.TABLE_NAME}"`)
    }

    async findHoursByStationId(id: number): Promise<StationsHour[]> {
        return db_connection.many(`SELECT * FROM "${this.TABLE_NAME}" WHERE station_id = ${id}`)
    }

    async findOne(id: number, hour: number): Promise<StationsHour | undefined> {
        return db_connection.one(`SELECT * FROM "${this.TABLE_NAME}" WHERE station_id = ${id} AND hour = ${hour}`)
    }
}

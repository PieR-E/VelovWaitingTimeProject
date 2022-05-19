import type {Station} from '~/types/station';

const pgp = require('pg-promise')({});
const connectionString = `postgres://${process.env.DB_USERNAME}:${process.env.DB_PASSWORD}@${process.env.DB_HOST}:${process.env.DB_PORT}/${process.env.DB_DATABASE}`;
const db = pgp(connectionString);

export class StationsService {
    TABLE_NAME = 'stations';

    stations: Station[] = [
        {station_id: 0, station_name: 'test 1'},
        {station_id: 1, station_name: 'test 2'},
        {station_id: 2, station_name: 'test 3'},
        {station_id: 3, station_name: 'test 4'},
    ]

    async findAll(): Promise<Station[]> {
        return db.any(`SELECT * FROM "${this.TABLE_NAME}"`)
    }

    async findOne(id: number): Promise<Station[]> {
        return db.many(`SELECT * FROM "${this.TABLE_NAME}" WHERE station_id = ${id}`)
    }
}

import {db_connection} from '~/resources/database';
import type {Station} from '~/types/station';

export class StationsService {
    TABLE_NAME = 'stations';

    async findAll(): Promise<Station[]> {
        return db_connection.any(`SELECT * FROM "${this.TABLE_NAME}"`)
    }

    async findOne(id: number): Promise<Station[]> {
        return db_connection.many(`SELECT * FROM "${this.TABLE_NAME}" WHERE station_id = ${id}`)
    }
}

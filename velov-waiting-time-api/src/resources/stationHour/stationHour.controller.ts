import {Router} from 'express'
import {StationHourService} from '~/resources/stationHour/stationHour.service'
import {BadRequestException, NotFoundException} from '~/utils/exceptions'

const StationHourController = Router()
const service = new StationHourService()

/* Find All */
StationHourController.get('/', async (req, res, next) => {
    try {
        return res
            .status(200)
            .json(await service.findAll())
    } catch (error) {
        next(error);
    }
})

/* Find Station All Hours */
StationHourController.get('/:id', async (req, res, next) => {
    try {
        const id = Number(req.params.id)

        if (!Number.isInteger(id)) {
            return Promise.reject(new BadRequestException('Invalid ID'));
        }

        const station = await service.findStationAll(id)
        if (!station) {
            return Promise.reject(new NotFoundException('Station not found'));
        }

        return res
            .status(200)
            .json(station)
    } catch (error) {
        next(error);
    }
})

/* Find One Station-Hour */
StationHourController.get('/:id/:hour', async (req, res, next) => {
    try {
        const id = Number(req.params.id);
        const hour = Number(req.params.hour);

        if (!Number.isInteger(id)) {
            return Promise.reject(new BadRequestException('Invalid ID'));
        }
        if (!Number.isInteger(hour)) {
            return Promise.reject(new BadRequestException('Invalid Hour'));
        }

        const stationHour = await service.findOne(id, hour)
        if (!stationHour) {
            return Promise.reject(new NotFoundException('Station-Hour not found'));
        }

        return res
            .status(200)
            .json(stationHour)
    } catch (error) {
        next(error);
    }
})

export {StationHourController}

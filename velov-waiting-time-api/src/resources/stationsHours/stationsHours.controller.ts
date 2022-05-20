import {Router} from 'express'
import {StationsHoursService} from '~/resources/stationsHours/stationsHours.service'
import {BadRequestException, NotFoundException} from '~/utils/exceptions'

const StationsHoursController = Router()
const service = new StationsHoursService()

/* Find All */
StationsHoursController.get('/', async (req, res, next) => {
    try {
        return res
            .status(200)
            .json(await service.findAll())
    } catch (error) {
        next(error);
    }
})

/* Find Hours By Station */
StationsHoursController.get('/:id', async (req, res, next) => {
    try {
        const id = Number(req.params.id)

        if (!Number.isInteger(id)) {
            return Promise.reject(new BadRequestException('Invalid ID'));
        }

        const station = await service.findHoursByStationId(id)
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
StationsHoursController.get('/:id/:hour', async (req, res, next) => {
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

export {StationsHoursController}

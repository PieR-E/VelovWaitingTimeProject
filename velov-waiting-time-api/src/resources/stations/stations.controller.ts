import {Router} from 'express'
import {BadRequestException, NotFoundException} from '~/utils/exceptions'
import {StationsService} from '~/resources/stations/stations.service';

const StationsController = Router()
const service = new StationsService()

/* Find All */
StationsController.get('/', async (req, res, next) => {
    try {
        return res
            .status(200)
            .json(await service.findAll())
    } catch (error) {
        next(error);
    }
})

/* Find One Station */
StationsController.get('/:id', async (req, res, next) => {
    try {
        const id = Number(req.params.id)

        if (!Number.isInteger(id)) {
            return Promise.reject(new BadRequestException('Invalid ID'));
        }

        const station = await service.findOne(id)
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

export {StationsController}

import 'dotenv/config';
import express from 'express'
import cors from 'cors'
import {ExceptionsHandler} from '~/middlewares/exceptions.handler';
import {UnknownRoutesHandler} from '~/middlewares/unknownRoutes.handler'
import {StationsController} from '~/resources/stations/stations.controller';
import {StationHoursController} from '~/resources/stationHours/stationHours.controller';

require('dotenv').config();

const app = express()
app.use(cors())

app.use('/stations', StationsController)
app.use('/station-hours', StationHoursController)

app.all('*', UnknownRoutesHandler)
app.use(ExceptionsHandler)
app.listen(process.env.PORT, () => console.log(`[server]: Server is running at http://localhost:${process.env.PORT}`))

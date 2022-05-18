import 'dotenv/config';
import express from 'express'
import cors from 'cors'
import {StationHourController} from '~/resources/stationHour/stationHour.controller';
import {ExceptionsHandler} from '~/middlewares/exceptions.handler';
import {UnknownRoutesHandler} from '~/middlewares/unknownRoutes.handler'

require('dotenv').config();

const app = express()
app.use(cors())

app.use('/station-hour', StationHourController)

app.all('*', UnknownRoutesHandler)
app.use(ExceptionsHandler)
app.listen(process.env.PORT, () => console.log(`[server]: Server is running at http://localhost:${process.env.PORT}`))

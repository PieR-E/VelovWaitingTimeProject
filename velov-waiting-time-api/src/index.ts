import 'dotenv-flow/config';
import express from 'express'
import cors from 'cors'
import {ExceptionsHandler} from '~/middlewares/exceptions.handler';
import {UnknownRoutesHandler} from '~/middlewares/unknownRoutes.handler'
import {StationsController} from '~/resources/stations/stations.controller';
import {StationsHoursController} from '~/resources/stationsHours/stationsHours.controller';

require('dotenv-flow').config(
    {
        purge_dotenv: true,
        silent: true
    }
);

const app = express()
app.use(cors())

app.use('/stations', StationsController)
app.use('/stations-hours', StationsHoursController)

app.all('*', UnknownRoutesHandler)
app.use(ExceptionsHandler)
app.listen(process.env.PORT, () => console.log(`[server]: Server is running at http://localhost:${process.env.PORT}`))

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

const homePage = '<div style="margin: auto">' +
    '<h1 style="text-align: center">Velov Waiting Time API</h1>' +
    '<ul><b>Controllers</b>' +
    '<li><a href="/stations">stations</a></li>' +
    '<li><a href="/stations-hours">stations-hours</a></li>' +
    '</ul></div>'
app.get('/', (req, res) => {
    return res.send(homePage);
})

app.use('/stations', StationsController)
app.use('/stations-hours', StationsHoursController)

app.all('*', UnknownRoutesHandler)
app.use(ExceptionsHandler)
app.listen(process.env.PORT, () => console.log(`[server]: Server is running at http://localhost:${process.env.PORT}`))

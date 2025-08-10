import { Router } from 'express';
import { PrayerTimesController } from '../controllers/prayerTimesController';

const router = Router();
const prayerTimesController = new PrayerTimesController();

export function setPrayerTimesRoutes(app) {
    router.get('/prayer-times', prayerTimesController.getPrayerTimes.bind(prayerTimesController));
    router.post('/prayer-times', prayerTimesController.addPrayerTime.bind(prayerTimesController));
    
    app.use('/api', router);
}
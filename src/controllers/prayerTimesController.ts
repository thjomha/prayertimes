class PrayerTimesController {
    constructor(private prayerTimeModel: any) {}

    async getPrayerTimes(req: any, res: any) {
        try {
            const prayerTimes = await this.prayerTimeModel.getAllPrayerTimes();
            res.status(200).json(prayerTimes);
        } catch (error) {
            res.status(500).json({ message: 'Error retrieving prayer times' });
        }
    }

    async addPrayerTime(req: any, res: any) {
        const newPrayerTime = req.body;
        try {
            await this.prayerTimeModel.insertPrayerTime(newPrayerTime);
            res.status(201).json({ message: 'Prayer time added successfully' });
        } catch (error) {
            res.status(500).json({ message: 'Error adding prayer time' });
        }
    }
}

export default PrayerTimesController;
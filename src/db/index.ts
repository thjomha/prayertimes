import { Pool } from 'pg';
import { PrayerTime } from '../models/prayerTime';

const pool = new Pool({
    user: 'your_username',
    host: 'localhost',
    database: 'prayer_times',
    password: 'your_password',
    port: 5432,
});

export const getAllPrayerTimes = async (): Promise<PrayerTime[]> => {
    const result = await pool.query('SELECT * FROM prayer_times');
    return result.rows;
};

export const insertPrayerTime = async (prayerTime: PrayerTime): Promise<void> => {
    const { date, fajr, dhuhr, asr, maghrib, isha } = prayerTime;
    await pool.query(
        'INSERT INTO prayer_times (date, fajr, dhuhr, asr, maghrib, isha) VALUES ($1, $2, $3, $4, $5, $6)',
        [date, fajr, dhuhr, asr, maghrib, isha]
    );
};
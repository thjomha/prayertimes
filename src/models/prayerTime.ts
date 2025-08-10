export class PrayerTime {
    id: number;
    date: string;
    fajr: string;
    dhuhr: string;
    asr: string;
    maghrib: string;
    isha: string;

    constructor(id: number, date: string, fajr: string, dhuhr: string, asr: string, maghrib: string, isha: string) {
        this.id = id;
        this.date = date;
        this.fajr = fajr;
        this.dhuhr = dhuhr;
        this.asr = asr;
        this.maghrib = maghrib;
        this.isha = isha;
    }
}
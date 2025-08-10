from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///prayertimes.db'
db = SQLAlchemy(app)

class PrayerTime(db.Model):
    date = db.Column(db.Date, primary_key=True)  # Use db.Date instead of db.String
    fajr = db.Column(db.String)
    sunrise = db.Column(db.String)
    dhuhr = db.Column(db.String)
    asr = db.Column(db.String)
    maghrib = db.Column(db.String)
    isha = db.Column(db.String)

# Create tables before running the app
with app.app_context():
    db.create_all()

@app.route('/prayertimes', methods=['POST'])
def add_prayer_time():
    data = request.json
    # Convert date string to date object
    try:
        data['date'] = datetime.strptime(data['date'], "%Y%m%d").date()
    except Exception:
        return jsonify({'error': 'Date must be in yyyymmdd format.'}), 400
    pt = PrayerTime(**data)
    db.session.add(pt)
    db.session.commit()
    return jsonify({'message': 'Prayer time added'}), 201

@app.route('/prayertimes/<date>', methods=['GET'])
def get_prayer_time_by_date(date):
    try:
        parsed_date = datetime.strptime(date, "%Y%m%d").date()
        print("Querying for date:", parsed_date)
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use yyyymmdd.'}), 400

    pt = PrayerTime.query.filter_by(date=parsed_date).first()
    if not pt:
        return jsonify({'error': 'No data for this date.'}), 404

    return jsonify({
        'date': pt.date.strftime("%Y%m%d"),
        'fajr': pt.fajr,
        'sunrise': pt.sunrise,
        'dhuhr': pt.dhuhr,
        'asr': pt.asr,
        'maghrib': pt.maghrib,
        'isha': pt.isha
    })

@app.route('/prayertimes/range', methods=['GET'])
def get_prayer_times_range():
    start = request.args.get('start')
    end = request.args.get('end')
    if not start or not end:
        return jsonify({'error': 'Please provide start and end dates in yyyymmdd format.'}), 400

    try:
        start_date = datetime.strptime(start, "%Y%m%d").date()
        end_date = datetime.strptime(end, "%Y%m%d").date()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use yyyymmdd.'}), 400

    times = PrayerTime.query.filter(PrayerTime.date >= start_date, PrayerTime.date <= end_date).all()
    return jsonify([{
        'date': t.date.strftime("%Y%m%d"),
        'fajr': t.fajr,
        'sunrise': t.sunrise,
        'dhuhr': t.dhuhr,
        'asr': t.asr,
        'maghrib': t.maghrib,
        'isha': t.isha
    } for t in times])

if __name__ == '__main__':
    app.run(debug=True)
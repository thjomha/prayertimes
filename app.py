import os
from flask import send_from_directory, abort
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

class AthanFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String, nullable=True)

# Create tables before running the app
with app.app_context():
    db.create_all()

ATHAN_FOLDER = os.path.join(os.path.dirname(__file__), 'athans')

@app.route('/athan/<int:athan_id>', methods=['GET'])
def serve_athan_by_id(athan_id):
    athan = AthanFile.query.get(athan_id)
    if not athan:
        abort(404)
    return send_from_directory(ATHAN_FOLDER, athan.filename, as_attachment=True)

@app.route('/<date>', methods=['GET'])
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

@app.route('/range', methods=['GET'])
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

@app.route('/')
def landing():
    return """
    <html>
    <head><title>Prayer Times API for Edmonton, Alberta</title></head>
    <body>
        <h1>Prayer Times API</h1>
        <h2>Quick Guide</h2>
        <ul>
            <li><b>GET /&lt;yyyymmdd&gt;</b> — Get prayer times for a specific date<br>
                Example: <code>/api/20250809</code>
            </li>
            <li><b>GET /range?start=yyyymmdd&end=yyyymmdd</b> — Get prayer times for a date range<br>
                Example: <code>/api/range?start=20250801&end=20250809</code>
            </li>
        </ul>
        <p>All dates must be in <b>yyyymmdd</b> format.</p>
    </body>
    </html>
    """
@app.route('/athan', methods=['GET'])
def get_athan_files():
    files = AthanFile.query.all()
    return jsonify([
        {
            'id': f.id,
            'filename': f.filename,
            'description': f.description
        } for f in files
    ])
if __name__ == '__main__':
    app.run(debug=True)
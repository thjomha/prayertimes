# Prayer Times API

This project is a simple API that serves prayer times from a database. It is built using TypeScript and Express.

## Project Structure

```
prayer-times-api
├── src
│   ├── app.ts                     # Entry point of the application
│   ├── controllers                # Contains the controllers for handling requests
│   │   └── prayerTimesController.ts
│   ├── models                     # Contains the data models
│   │   └── prayerTime.ts
│   ├── routes                     # Contains the route definitions
│   │   └── prayerTimesRoutes.ts
│   └── db                        # Database connection and queries
│       └── index.ts
├── package.json                   # NPM package configuration
├── tsconfig.json                  # TypeScript configuration
└── README.md                      # Project documentation
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd prayer-times-api
   ```

2. Install the dependencies:
   ```
   npm install
   ```

3. Start the server:
   ```
   npm start
   ```

## API Endpoints

- `GET /api/prayer-times`: Retrieve all prayer times.
- `POST /api/prayer-times`: Add a new prayer time.

## Usage Examples

### Retrieve Prayer Times

```bash
curl -X GET http://localhost:3000/api/prayer-times
```

### Add Prayer Time

```bash
curl -X POST http://localhost:3000/api/prayer-times -H "Content-Type: application/json" -d '{"date": "2023-10-01", "fajr": "05:00", "dhuhr": "12:00", "asr": "15:30", "maghrib": "18:00", "isha": "19:30"}'
```

## License

This project is licensed under the MIT License.
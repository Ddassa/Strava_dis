# Trailmetrics

Trailmetrics is a small FastAPI application that integrates with Strava to compute metrics for new activities. It demonstrates OAuth authentication, webhook handling and metric computations.

## Setup

1. Copy `.env.example` to `.env` and fill in your Strava API credentials.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the development server:
   ```bash
   uvicorn app.main:app --reload --host localhost --port 8000
   ```
4. Test endpoints using curl or Postman.

## Tests

Run tests with:
```bash
pytest
```

# Quickstart: Web Support Form Channel

## Prerequisites
- Backend: `uv` installed.
- Frontend: `node` and `npm` installed.
- PostgreSQL running (refer to `.env`).

## 1. Backend Setup
```bash
cd backend
uv sync
uv run fastapi dev app/main.py
```
The backend should be available at `http://localhost:8000`.

## 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
The frontend should be available at `http://localhost:3000`.

## 3. Verification
1. Navigate to `http://localhost:3000`.
2. Fill out the support form with test data.
3. Click "Submit".
4. Verify success message and Ticket ID display.
5. Check backend logs for `POST /api/v1/webhooks/web-form 201`.
6. (Optional) Check database `ticket` and `message` tables for new records.

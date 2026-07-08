## Backend deployment (Render)

- **Root Directory**: `backend`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Required environment variables

- `DATABASE_URL` — Render PostgreSQL URL (Render panosundan alınır)
- `GEMINI_API_KEY` — Gemini API key
- `AI_PROVIDER` — `gemini` or `mock` (use `mock` on Render demo if quota is exhausted)
- `GEMINI_MODEL` — e.g. `gemini-2.0-flash`
- `SECRET_KEY` — JWT secret
- `ALGORITHM` — usually `HS256`
- `ACCESS_TOKEN_EXPIRE_MINUTES` — e.g. `60`
- `FRONTEND_URL` — e.g. `http://localhost:5173` or deployed frontend URL


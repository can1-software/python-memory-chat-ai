from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import FRONTEND_URL
from app.routers import auth, chats, debug

app = FastAPI(title="Memory Chat AI")


origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
if FRONTEND_URL:
    origins.append(FRONTEND_URL)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router)
app.include_router(chats.router)
app.include_router(debug.router)


@app.get("/")
def home():
    return {"message": "Memory Chat AI backend çalışıyor 🚀"}


@app.get("/health")
def health():
    return {"status": "ok"}

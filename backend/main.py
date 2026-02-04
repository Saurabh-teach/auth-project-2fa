from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine
from routers import auth

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Auth App with 2FA")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Keep prefix here — this adds /auth to all routes in auth router
app.include_router(auth.router, prefix="/auth")
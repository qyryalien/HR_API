from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routers import user, auth, position, candidate, schedule
from src.config import settings

app = FastAPI()

origins = [
    settings.CLIENT_ORIGIN,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, tags=['Auth'], prefix='/api/auth')
app.include_router(user.router, tags=['Users'], prefix='/api/users')
app.include_router(position.router, tags=['Positions'], prefix='/api/positions')
app.include_router(candidate.router, tags=['Candidates'], prefix='/api/candidate')
app.include_router(schedule.router, tags=['Schedules'], prefix='/api/schedule')

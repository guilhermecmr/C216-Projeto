from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.users import router as users_router
from app.routes.polls import router as polls_router
from app.routes.options import router as options_router
from app.routes.votes import router as votes_router
from app.routes.auth import router as auth_router

app = FastAPI(
    title="EnqueteHub",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(users_router)
app.include_router(polls_router)
app.include_router(options_router)
app.include_router(votes_router)
app.include_router(auth_router)
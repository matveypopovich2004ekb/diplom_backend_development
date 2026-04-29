from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.general_router import router as general_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(general_router)
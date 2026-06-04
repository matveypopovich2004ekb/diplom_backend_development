from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.general_router import router as general_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "https://diplom-frontend-one.vercel.app",],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(general_router)
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api import users, sync, report, cve
from app.database.init_db import init


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Initializing database...")
    await init()
    yield

app = FastAPI(title="Android Security Database API", lifespan=lifespan)

# Add origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
)

app.include_router(users.router)
app.include_router(sync.router)
app.include_router(report.router, prefix="/report")
app.include_router(cve.router, prefix="/api")

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
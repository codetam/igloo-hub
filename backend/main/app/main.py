from mangum import Mangum
from datetime import datetime
import os
import logging
from logging.config import dictConfig
from contextlib import asynccontextmanager

import yaml
from fastapi import FastAPI
from app.core.db import init_db, reset_db
from app.api.routes import games, players, stadiums

logging_config_path = os.getenv("LOGGING_CONFIG", "/logging/logging.yaml")
with open(logging_config_path, "r") as f:
    config = yaml.safe_load(f.read())
    dictConfig(config)

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield
    logging.info("FastAPI shutdown complete")

app = FastAPI(docs_url="/docs", openapi_url=f"/docs/openapi.json", lifespan=lifespan)
start_time = datetime.now()

app.include_router(games.router)
app.include_router(players.router)
app.include_router(stadiums.router)

@app.get("/health")
async def healthcheck():
    return {"status": "ok", "uptime_seconds": (datetime.now() - start_time).total_seconds()}

handler = Mangum(app)
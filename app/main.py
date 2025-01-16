from fastapi import FastAPI
from loguru import logger

from app import setup
from app.api.organization import org_router
from .config.consts import config


DEV = config["DEV"]

if DEV:
    app = FastAPI(docs_url="/api/swagger", redoc_url="/api/redoc")
else:
    app = FastAPI(docs_url=None, redoc_url=None)

app.include_router(org_router)

setup.init_logging(setup.log.LogSettings())
logger.info(f"App start!")

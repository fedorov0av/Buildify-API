from fastapi import FastAPI
from loguru import logger

from app import setup
from .config.consts import config

DEV = config["DEV"]

if DEV:
    app = FastAPI(docs_url="/api/swagger", redoc_url="/api/redoc")
else:
    app = FastAPI(docs_url=None, redoc_url=None)

setup.init_logging(setup.log.LogSettings())
logger.info(f"App start!")

from __future__ import annotations
from dotenv import dotenv_values

import zoneinfo
from pathlib import Path

config = dotenv_values(".env")
TIME_ZONE = zoneinfo.ZoneInfo("Europe/Moscow")
API_VERSION = 'v1'

BASE_DIR = Path(__file__).parent.parent.parent
LOG_DIR = BASE_DIR / "logs"

for DIR in [LOG_DIR, ]:
    DIR.mkdir(exist_ok=True)
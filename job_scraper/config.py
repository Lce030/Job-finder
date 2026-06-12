"""Loads configuration and credentials from environment variables."""

import os

from dotenv import load_dotenv

load_dotenv()

ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID", "")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY", "")


def adzuna_configured() -> bool:
    """Returns whether Adzuna credentials are available."""
    return bool(ADZUNA_APP_ID and ADZUNA_APP_KEY)

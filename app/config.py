from __future__ import annotations

import os


def database_url() -> str:
    # Example: sqlite:////data/app.db (docker compose)
    return os.getenv("DATABASE_URL", "sqlite:///./app.db")


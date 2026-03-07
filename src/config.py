import os
class Config:
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://postgres:kimdokja@localhost:5432/proyecto"
    )

    MAX_RETRIES = 3
    BASE_BACKOFF = 0.1
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    DEV_MODE = "true"  # os.getenv("DEV_MODE", "false").lower() == "true"
    DB_URI = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
    OUTPUT_DIR = "output"
    LOG_LEVEL = "INFO"
    ANALYZED_ARTICLES = set()  # Track analyzed articles in memory

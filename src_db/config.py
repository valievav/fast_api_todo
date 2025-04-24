from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    DATABASE_URL: str
    TEST_DATABASE_URL: str

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent / '.env',
        env_file_encoding='utf-8',
        extra="ignore",  # do not read extra attributes from env file
    )


import os
print("ENV FILE FOUND?", os.path.isfile(".env"))
print("DATABASE_URL", os.getenv("DATABASE_URL"))

Config = Settings()

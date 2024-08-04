from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn


class Settings(BaseSettings):
    db_url: PostgresDsn = MultiHostUrl("postgresql+asyncpg://user:pass@localhost/dbname")

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


config = Settings()

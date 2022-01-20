from pydantic import BaseSettings


class Settings(BaseSettings):
    IS_TESTING: bool = False
    DEBUG: bool = False

    DB_DSN: str = "sqlite+aiosqlite:///db"
    DB_DSN_SYNC: str = "sqlite:///db"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

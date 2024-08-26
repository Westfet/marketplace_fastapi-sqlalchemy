import datetime
from typing import Annotated
from pydantic_settings import BaseSettings
from sqlalchemy import text
from sqlalchemy.orm import mapped_column


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_NAME: str
    DB_PASS: str

    class Config:
        env_file = ".env"

    @property
    def DATABASE_URL_psycopg(self):
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()


# Константы полей
CREATED_AT = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
UPDATED_AT = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"),
                                                        onupdate=datetime.datetime.utcnow)]

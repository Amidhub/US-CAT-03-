from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    database_url: str = Field(alias="DATABASE_URL")
    secret_key: str = Field(alias="SECRET_KEY")
    service_key: str = Field(alias="SERVICE_KEY")
    debug: bool = Field(default=False, alias="DEBUG")

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
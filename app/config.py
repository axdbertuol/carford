from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_driver: str
    database_host: str
    database_port: int
    database_user: str
    database_password: str
    database_dbname: str
    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore", populate_by_name=True
    )

    def get_sql_alch_dbconnstr(self):
        return (
            f"{self.database_driver}://{self.database_user}:{self.database_password}@{self.database_host}"
            + f":{self.database_port}/{self.database_dbname}"
        )


@lru_cache
def get_settings():
    return Settings()


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SQLALCHEMY_DATABASE_URI = get_settings().get_sql_alch_dbconnstr()

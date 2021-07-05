from functools import lru_cache
from pydantic import BaseSettings, AnyUrl, validator
from typing import Optional, Dict, Any
import sqlalchemy


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    IMG_DIR: str

    DB_HOST: str
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    SQLALCHEMY_DATABASE_URI: Optional[AnyUrl] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return sqlalchemy.engine.url.URL(
            drivername="mysql",
            username=values.get("DB_USER"),
            password=values.get("DB_PASSWORD"),
            host=values.get("DB_HOST"),
            database=values.get("DB_NAME"),
            query={'charset': 'utf8'}
        ).__str__()


    class Config:
        env_file_encoding = 'utf-8'
        case_sensitive = True


def get_settings() -> Settings:
    return Settings()

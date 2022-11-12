from pathlib import Path
from typing import Optional

from pydantic import BaseSettings, Field

BASE_DIR = Path(__file__).parent
SQLITE_PATH = BASE_DIR / "sql_app.db"
SQLALCHEMY_DATABASE_URL = "sqlite:///" + SQLITE_PATH.__str__()


class _UvicornConfig(BaseSettings):
    host: str = Field('0.0.0.0')
    port: int = Field(8000)
    workers: Optional[int] = Field(4)

    class Config:
        env_file = BASE_DIR / '.env'
        env_prefix = 'APP_'


class PostgresConfig(BaseSettings):
    username: str = Field('postgres')
    host: str = Field('postgres')
    port: int = Field(5432)
    password: str = Field('postgres')

    class Config:
        env_file = BASE_DIR / '.env'
        env_prefix = 'POSTGRES_'

    @property
    def postgre_url(self):
        return f'postgresql+asyncpg://{self.username}:{self.password}@{self.host}:{self.port}'


postgres_url = PostgresConfig().postgre_url
uvicorn_config = _UvicornConfig().dict(exclude_none=True)

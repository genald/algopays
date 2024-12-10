from functools import lru_cache
from pydantic_settings import BaseSettings

class DatabaseConfig(BaseSettings):
    DB_CONNECTOR: str = "sqlite"
    DB_USERNAME : str = ""
    DB_PASSWORD : str = ""
    DB_NAME     : str = ""
    DB_HOST     : str = ""
    DB_PORT     : str = ""

    def __str__(self):
        password = self.DB_PASSWORD and f":{self.DB_PASSWORD}" or ""
        host     = self.DB_HOST and f"@{self.DB_HOST}" or ""
        port     = self.DB_PORT and f":{self.DB_PORT}" or ""
        return f"{self.DB_CONNECTOR}://{self.DB_USERNAME}{password}{host}{port}/{self.DB_NAME}"

db_config = lru_cache(lambda: DatabaseConfig())

engine_config = dict(
    pool_size     = 0,
    pool_timeout  = None,
    pool_pre_ping = True,
    connect_args  = {'connect_timeout': 36000}
)

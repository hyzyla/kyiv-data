from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    AUTH_TOKEN: str
    STORAGE_ENDPOINT: str
    STORAGE_ACCESS_KEY: str
    STORAGE_SECRET_KEY: str
    STORAGE_SECURE: bool
    CC_HOST: str = '1551-back.kyivcity.gov.ua'
    SENTRY_DSN: Optional[str] = None


settings = Settings()

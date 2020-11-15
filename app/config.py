from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    CC_HOST: str = '1551-back.kyivcity.gov.ua'
    SENTRY_DSN: Optional[str] = None


settings = Settings()

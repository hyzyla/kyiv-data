from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    CC_HOST: str = '1551-back.kyivcity.gov.ua'

    class Config:
        env_prefix = 'APP_'


settings = Settings()

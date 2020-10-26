from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    CONTACT_CENTER_HOST: str = '1551-back.kyivcity.gov.ua'
    CONTACT_CENTER_TICKETS_URL: str = f'https://{CONTACT_CENTER_HOST}/api/tickets/search'

    class Config:
        env_prefix = 'APP_'


settings = Settings()

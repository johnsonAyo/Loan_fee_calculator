from pydantic_settings import BaseSettings
from app.core.constants import (
    APP_NAME as DEFAULT_APP_NAME,
    DEBUG_DEFAULT,
    ENV_FILE_NAME,
)

class Settings(BaseSettings):
    APP_NAME: str = DEFAULT_APP_NAME
    DEBUG: bool = DEBUG_DEFAULT
    
    class Config:
        env_file = ENV_FILE_NAME

settings = Settings()

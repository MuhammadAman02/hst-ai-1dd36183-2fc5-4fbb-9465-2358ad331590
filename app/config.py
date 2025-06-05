from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    app_name: str = "NiceGUI Showcase"
    app_version: str = "1.0.0"
    debug: bool = False
    port: int = 8000
    host: str = "0.0.0.0"
    
    class Config:
        env_file = ".env"


settings = Settings()
# settings.py (exemplo)
import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

# Define a base directory as the directory where settings.py is located
base_dir = os.path.dirname(os.path.abspath(__file__))

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.path.join(base_dir, ".env"),
        env_file_encoding="utf-8"
    )
    OPENAI_API_KEY: str
    SERPER_API_KEY: str

@lru_cache(maxsize=1)
def get_config() -> Settings:
    return Settings()

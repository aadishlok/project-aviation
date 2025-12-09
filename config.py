from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_HOST: str
    APP_PORT: int
    AVIATION_DATA_API_URL: str
    AVAIATION_DATA_API_TOKEN: str
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
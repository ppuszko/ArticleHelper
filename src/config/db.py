from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_URL: str
    LOCAL_STORAGE_PATH: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    ) 

DBConfig = Settings() # type: ignore
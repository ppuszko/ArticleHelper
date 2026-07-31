from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    GOOGLE_API_KEY: str
    TEXT_PROC_MODEL: str
    IMG_PROC_MODEL: str
    RETRIES: int = 3

    model_config = SettingsConfigDict(
        extra="ignore",
        env_file=".env"
    ) 

AIConfig = Settings() # type: ignore
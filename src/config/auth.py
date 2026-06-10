from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    JWT_SECRET: str
    RESET_PASSWORD_TOKEN_SECRET: str
    VERIFICATION_TOKEN_SECRET: str 
    TOKEN_LIFETIME_SECONDS: int = 3600

    model_config = SettingsConfigDict(
        extra="ignore",
        env_file=".env"
    ) 

AuthConfig = Settings() # type: ignore
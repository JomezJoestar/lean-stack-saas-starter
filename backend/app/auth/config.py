from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # JWT Settings
    SECRET_KEY: str = "DEFAULT_INSECURE_SECRET_KEY"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Stripe Settings
    STRIPE_SECRET_KEY: str
    STRIPE_WEBHOOK_SECRET: str

    # Reads OS environment variables injected by Docker Compose,
    # with fallbacks to .env in either current directory or parent directory.
    model_config = SettingsConfigDict(
        env_file=(".env", "../.env"),
        env_file_encoding="utf-8",
        extra="ignore"  # Ignores extra environment variables from Docker
    )

# Instantiate the global settings object
auth_settings = Settings()
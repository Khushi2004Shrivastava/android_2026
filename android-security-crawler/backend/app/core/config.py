from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://nvd_user:nvd_password@localhost:5432/nvd_db"

    # Ollama Local Setup
    # Hardcoding these as defaults makes local setup "plug and play"
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "cogito-2.1:671b"

    # Modern Pydantic V2 way to handle config
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()

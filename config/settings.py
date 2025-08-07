"""
Configuration settings for TalentScout Hiring Assistant
"""
import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Application settings configuration"""

    # API Configuration
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")
    OPENROUTER_BASE_URL: str = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

    # Application Configuration
    APP_NAME: str = os.getenv("APP_NAME", "TalentScout Hiring Assistant")
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # Model Configuration
    DEFAULT_MODEL: str = "openai/gpt-4-turbo-preview"
    FALLBACK_MODEL: str = "openai/gpt-3.5-turbo"
    MAX_TOKENS: int = 1500
    TEMPERATURE: float = 0.7

    # Session Configuration
    SESSION_TIMEOUT: int = 3600  # 1 hour in seconds
    MAX_CONVERSATION_LENGTH: int = 50  # Maximum number of messages to keep

    # File Paths
    DATA_DIR: str = "data"
    CANDIDATES_FILE: str = os.path.join(DATA_DIR, "candidates.json")
    ASSETS_DIR: str = "assets"

    # Validation Settings
    MIN_NAME_LENGTH: int = 2
    MAX_NAME_LENGTH: int = 100
    MIN_EXPERIENCE_YEARS: int = 0
    MAX_EXPERIENCE_YEARS: int = 50

    @classmethod
    def validate_api_key(cls) -> bool:
        """Validate if API key is configured"""
        return bool(cls.OPENROUTER_API_KEY and cls.OPENROUTER_API_KEY != "your_openrouter_api_key_here")

settings = Settings()

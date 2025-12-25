import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables
    """
    # OpenAI Configuration
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")

    # Qdrant Configuration
    qdrant_url: str = os.getenv("QDRANT_URL", "")
    qdrant_api_key: str = os.getenv("QDRANT_API_KEY", "")

    # Application Configuration
    api_host: str = os.getenv("API_HOST", "localhost")
    api_port: int = int(os.getenv("API_PORT", "8000"))
    default_top_k: int = int(os.getenv("DEFAULT_TOP_K", "5"))
    similarity_threshold: float = float(os.getenv("SIMILARITY_THRESHOLD", "0.5"))

    # Validation
    def validate_config(self):
        """Validate that required configuration is present"""
        errors = []
        if not self.openai_api_key:
            errors.append("OPENAI_API_KEY is required")
        if not self.qdrant_url:
            errors.append("QDRANT_URL is required")
        if not self.qdrant_api_key:
            errors.append("QDRANT_API_KEY is required")

        if errors:
            raise ValueError(f"Missing required configuration: {'; '.join(errors)}")


# Global settings instance
settings = Settings()
settings.validate_config()
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    gemini_api_image_key: str
    file_limit_mb: int = 10
    total_files: int = 5
    bytes_to_mb: int = 1024 * 1024

    @property
    def max_file_size_bytes(self) -> int:
        return self.file_limit_mb * self.bytes_to_mb

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
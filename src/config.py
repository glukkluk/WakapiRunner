from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

SUPPORTED_EDITORS = ["Code", "Code - Insiders", "pycharm64"]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    editor: str = Field(default="Code")
    wakapi_config_path: str = Field(default="~/wakapi/config.yml")
    timeout: float = Field(default=0.5)

    @field_validator("editor")
    @classmethod
    def validate_editor(cls, v: str) -> str:
        if v not in SUPPORTED_EDITORS:
            raise ValueError(f"Editor must be one of: {SUPPORTED_EDITORS}")
        return v

    def get_wakapi_config_path(self) -> Path:
        return Path(self.wakapi_config_path).expanduser().resolve()


settings = Settings()
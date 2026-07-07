# Python libs
import tomllib
from pathlib import Path

# Pydantic
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


# Settings Class
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    # App
    app_mode: str = ""

    # Data from pyproject.toml
    project_name: str = ""
    project_version: str = ""
    project_description: str = ""
    project_authors: list[str] = Field(default_factory=list)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        pyproject = Path(__file__).resolve().parent / "pyproject.toml"

        if pyproject.exists():
            with pyproject.open("rb") as f:
                data = tomllib.load(f)

            metadata = data.get("tool", {}).get("openhubble", {})

            self.project_name = metadata.get("name", "")
            self.project_version = metadata.get("version", "")
            self.project_description = metadata.get("description", "")
            self.project_authors = metadata.get("authors", [])


# Run settings
settings = Settings()

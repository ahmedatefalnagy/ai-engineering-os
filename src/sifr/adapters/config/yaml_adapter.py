"""YAML Configuration Adapter using safe loading and validation."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field

from sifr.domain.models import ProjectConfig
from sifr.ports.contracts import ConfigPort


class ProjectConfigSchema(BaseModel):
    """Pydantic validation schema for project YAML files."""

    name: str = Field(min_length=1)
    version: str = Field(default="0.1.0")
    technology_profile: str = Field(default="generic")
    description: str = Field(default="")
    settings: dict[str, Any] = Field(default_factory=dict)


class YamlConfigAdapter(ConfigPort):
    """Adapter for reading and writing YAML configuration files safely."""

    def load_project_config(self, config_path: Path) -> ProjectConfig:
        if not config_path.is_file():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")

        with open(config_path, encoding="utf-8") as f:
            raw_data = yaml.safe_load(f)

        if not isinstance(raw_data, dict):
            raise ValueError(f"Invalid YAML structure in {config_path}: expected dictionary")

        validated = ProjectConfigSchema(**raw_data)
        return ProjectConfig(
            name=validated.name,
            version=validated.version,
            technology_profile=validated.technology_profile,
            description=validated.description,
            settings=validated.settings,
        )

    def save_project_config(self, config_path: Path, config: ProjectConfig) -> None:
        data = {
            "name": config.name,
            "version": config.version,
            "technology_profile": config.technology_profile,
            "description": config.description,
            "settings": config.settings,
        }
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(config_path, "w", encoding="utf-8") as f:
            yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True)

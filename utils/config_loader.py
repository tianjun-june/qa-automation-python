import logging
import os
from dotenv import load_dotenv
from pathlib import Path

import yaml
from pydantic import ValidationError
from utils.config_models import AppConfig

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = PROJECT_ROOT / "config"


def load_yaml(file_path: Path) -> dict:
    with open(file_path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file) or {}

def merge_config(base:dict, override:dict) -> dict:
    result = base.copy()

    for key, value in override.items():
        if (
            key in result
            and isinstance(result[key], dict)
            and isinstance(value, dict)
        ):
            result[key] = merge_config(result[key], value)
        else:
            result[key] = value

    return result

def load_config(environment: str) -> AppConfig:
    base_config = load_yaml(CONFIG_DIR / "base.yaml")

    environment_file = CONFIG_DIR / f"{environment}.yaml"

    if not environment_file.exists():
        raise FileNotFoundError(f"Configuration file {environment_file} not found")

    environment_config = load_yaml(environment_file)

    merged_config = merge_config(base_config, environment_config)

    username = os.getenv("TEST_USERNAME")
    password = os.getenv("TEST_PASSWORD")

    if not username or not password:
        raise RuntimeError(
            "TEST_USERNAME and TEST_PASSWORD variables are required."
        )

    merged_config["credentials"] = {
        "username": username,
        "password": password,
    }

    try:
        return AppConfig.model_validate(merged_config)

    except ValidationError as error:
        raise  ValueError(
            f"Invalid configuration for environment '{environment}':\n"
            f"{error}"
        ) from error

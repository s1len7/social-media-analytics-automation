import os
from pathlib import Path

import yaml

from social_media_analytics.constants import APP_NAME


def get_project_directory():
    current_path = Path(__file__).resolve()

    for parent in current_path.parents:
        if (parent / "pyproject.toml").exists():
            return parent

    return None


def get_app_directory():
    project_directory = get_project_directory()

    if project_directory:
        return project_directory / ".config" / APP_NAME

    if os.getenv("APPDATA"):
        return Path(os.getenv("APPDATA")) / APP_NAME

    return Path.home() / ".config" / APP_NAME


APP_DIRECTORY = get_app_directory()
ENV_PATH = APP_DIRECTORY / ".env"
CONFIG_PATH = APP_DIRECTORY / "config.yaml"


def get_template_config_path():
    return Path(__file__).parents[3] / "config" / "config_default.yaml"


def ensure_app_directory():
    APP_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )


def env_exists():
    return ENV_PATH.exists()


def config_exists():
    return CONFIG_PATH.exists()


def save_env(values):
    ensure_app_directory()

    content = []

    for key, value in values.items():
        content.append(
            f"{key}={value}",
        )

    ENV_PATH.write_text(
        "\n".join(content),
        encoding="utf-8",
    )


def load_env():
    if not ENV_PATH.exists():
        return {}

    result = {}

    for line in ENV_PATH.read_text(
        encoding="utf-8",
    ).splitlines():
        line = line.strip()

        if not line:
            continue

        if line.startswith("#"):
            continue

        if "=" not in line:
            continue

        key, value = line.split(
            "=",
            1,
        )

        result[key.strip()] = value.strip()

    return result


def save_config(config):
    ensure_app_directory()

    CONFIG_PATH.write_text(
        yaml.safe_dump(
            config,
            allow_unicode=True,
            sort_keys=False,
        ),
        encoding="utf-8",
    )


def load_config_file():
    if not CONFIG_PATH.exists():
        return {}

    return yaml.safe_load(
        CONFIG_PATH.read_text(
            encoding="utf-8",
        )
    )


def load_template_config():
    template_path = get_template_config_path()

    if not template_path.exists():
        raise FileNotFoundError(
            f"Config template not found: {template_path}",
        )

    return yaml.safe_load(
        template_path.read_text(
            encoding="utf-8",
        )
    )


def load_or_create_config():
    if config_exists():
        return load_config_file()

    return load_template_config()


def get_env_path():
    return ENV_PATH


def get_config_path():
    return CONFIG_PATH

import os
import re
from pathlib import Path

import yaml

from social_media_analytics.setup.config_io import get_config_path

ENV_PATTERN = re.compile(r"\$\{([^}]+)\}")


def replace_env_variables(value):
    if isinstance(value, dict):
        return {key: replace_env_variables(item) for key, item in value.items()}

    if isinstance(value, list):
        return [replace_env_variables(item) for item in value]

    if isinstance(value, str):
        matches = ENV_PATTERN.findall(value)

        for key in matches:
            env_value = os.getenv(
                key,
                "",
            )

            value = value.replace(
                f"${{{key}}}",
                env_value,
            )

    return value


def load_config():
    config_path = Path(get_config_path())

    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    config = yaml.safe_load(
        config_path.read_text(
            encoding="utf-8",
        )
    )

    return replace_env_variables(config)

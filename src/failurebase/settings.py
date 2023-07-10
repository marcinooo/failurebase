"""Settings module."""

import os
from pathlib import Path
from pydantic import BaseSettings


CONFIGURATION_FILE_VARIABLE = 'FAILUREBASE_CONFIGURATION'


def get_configuration_file_path():
    """Reads and validates path of configuration file assigned to env variable."""

    configuration = os.environ.get(f'{CONFIGURATION_FILE_VARIABLE}')

    if configuration is None:
        raise ConfigurationError(f'"{CONFIGURATION_FILE_VARIABLE}" system variable is not defined.')

    path = Path(configuration)

    if not path.exists():
        raise ConfigurationError(f'Configuration file does not exist ({CONFIGURATION_FILE_VARIABLE}={path}).')
    if not path.is_file():
        raise ConfigurationError(f'Path from "{CONFIGURATION_FILE_VARIABLE}" system variable does not indicate file.')

    return path


class ConfigurationError(Exception):
    """Throws when configuration file cannot be loaded."""


class Settings(BaseSettings):
    """Main app settings."""

    DATABASE_URI: str

    EVENTS_PER_PAGE: int
    TESTS_PER_PAGE: int

    class Config:
        env_file = get_configuration_file_path()
        env_file_encoding = 'utf-8'

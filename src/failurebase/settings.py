"""Settings module."""

import os
from pathlib import Path
from pydantic import BaseSettings, validator, root_validator


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

    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    CLIENT_FROM_APP: bool
    CORS_ALLOWED_ORIGINS: str | None
    DATABASE_URI: str
    EVENTS_PER_PAGE: int
    TESTS_PER_PAGE: int
    CLIENTS_PER_PAGE: int
    RESOURCES_DIR: Path = Path(__file__).parent / 'resources'
    LOGGING_CONFIGURATION_FILE: str | None = None

    class Config:
        env_file = get_configuration_file_path()
        env_file_encoding = 'utf-8'

    @validator('CORS_ALLOWED_ORIGINS')
    def cors_allowed_origins(cls, v: str | None) -> list:
        """Prepares list of allowed origins."""

        if v is not None:
            return [host.strip() for host in v.split(',')]
        return []

    @root_validator
    def logging_configuration_file(cls, values: dict) -> dict:
        """Builds path to logging configuration file."""

        logging_configuration_file = values.get('LOGGING_CONFIGURATION_FILE')

        if logging_configuration_file is not None:
            values['LOGGING_CONFIGURATION_FILE'] = Path(logging_configuration_file)
        values['LOGGING_CONFIGURATION_FILE'] = values.get('RESOURCES_DIR') / 'logging' / 'default.conf'
        return values

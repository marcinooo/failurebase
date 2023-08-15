"""CLI utils module."""

from enum import Enum


class ExitCode(Enum):
    """CLI exit codes."""

    SUCCESS: int = 0
    UNKNOWN_COMMAND_ERROR: int = 10
    CONFIGURATION_FILE_ERROR: int = 20
    DATABASE_CONNECTION_ERROR: int = 30
    API_KEY_ERROR: int = 40
    FILE_DOES_NOT_EXIST: int = 50
    COPY_FILE_ERROR: int = 60
    FRONTEND_DIRECTORY_ERROR: int = 70


class PARSER(Enum):
    """Parser types."""

    CONFIG_CREATE = 11
    FRONTEND_CREATE = 21
    API_KEY_CREATE = 31
    API_KEY_SHOW = 32
    API_KEY_DELETE = 33

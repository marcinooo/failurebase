"""Api Key commands module."""

import os
from pathlib import Path
from fastapi import status as fastapi_statuses
from sqlalchemy.exc import ArgumentError

from failurebase.cli.commands.base import Command
from failurebase.cli.utils import ExitCode


class CreateFailurebaseAppCommandMixin:
    """Extends base command class."""

    def __init__(self):

        self.app = None

    def load_environment_file(self, env_file: Path | str) -> ExitCode:
        """Loads environments fail. REQUIRED before app creation."""

        if isinstance(env_file, str):
            env_file = Path(env_file)

        if not Path(env_file).exists():
            self.log(f'Configuration file does not exist\n')
            return ExitCode.CONFIGURATION_FILE_ERROR

        self.log(f'Used configuration file: {env_file}\n')

        os.environ['FAILUREBASE_CONFIGURATION'] = str(env_file)

        return ExitCode.SUCCESS

    def create_app(self, env_file: Path | str) -> ExitCode:
        """Creates failurebase app."""

        status = self.load_environment_file(env_file)
        if status != ExitCode.SUCCESS:
            return status

        from failurebase.application import create_app

        try:
            self.app = create_app()
        except ArgumentError as error:
            self.log(f'Database connection error: {error}\n')
            return ExitCode.DATABASE_CONNECTION_ERROR

        return ExitCode.SUCCESS


class CreateApiKeyCommand(Command, CreateFailurebaseAppCommandMixin):
    """Manage creation of api key."""

    def execute(self, *args, **kwargs):
        """Performs main command action."""

        value: str = kwargs.get('value')
        env_file: Path | str = kwargs.get('env_file')

        status = self.create_app(env_file)
        if status != ExitCode.SUCCESS:
            return status

        api_key_service = self.app.container.services.api_key_service()
        secret_manager = self.app.container.managers.secret_manager()

        from failurebase.schemas.api_key import CreateApiKeySchema
        api_key_schema = CreateApiKeySchema(value=secret_manager.encrypt(value))

        api_key_service.create(api_key_schema)

        self.log(f'Api key created successfully\n')

        return status


class ShowApiKeyCommand(Command, CreateFailurebaseAppCommandMixin):
    """Manage presentation of existing api keys in database."""

    def execute(self, *args, **kwargs):
        """Performs main command action."""

        env_file: Path | str = kwargs.get('env_file')

        status = self.create_app(env_file)
        if status != ExitCode.SUCCESS:
            return status

        api_key_service = self.app.container.services.api_key_service()
        secret_manager = self.app.container.managers.secret_manager()

        api_keys = api_key_service.get_many()

        self.log(f'All API KEYs:\n')

        if api_keys.count == 0:
            self.log(f'There are no any API KEYs \n')

        for api_key in api_keys.items:
            self.log(f'- id: {api_key.id}\n  value: {secret_manager.decrypt(api_key.encrypted_value)}\n')

        return status


class DeleteApiKeyCommand(Command, CreateFailurebaseAppCommandMixin):
    """Manage deletion of api key."""

    def execute(self, *args, **kwargs):
        """Performs main command action."""

        api_key_id: int = kwargs.get('api_key_id')
        env_file: Path | str = kwargs.get('env_file')

        status = self.create_app(env_file)
        if status != ExitCode.SUCCESS:
            return status

        from failurebase.schemas.common import IdsSchema

        api_key_service = self.app.container.services.api_key_service()
        deletion_statuses = api_key_service.delete(IdsSchema(ids=[api_key_id]))

        if deletion_statuses.statuses[0].status == fastapi_statuses.HTTP_200_OK:
            self.log(f'API KEY witch ID equals {api_key_id} was deleted successfully.\n')
            return ExitCode.API_KEY_ERROR

        self.log(f'API KEY witch ID equals {api_key_id} does NOT exist.\n')
        return ExitCode.API_KEY_ERROR

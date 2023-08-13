import os

import pytest

from failurebase.cli.commands.api_key import CreateApiKeyCommand, ShowApiKeyCommand, DeleteApiKeyCommand
from failurebase.adapters.models import ApiKey


class TestApiKeyCommands:

    @pytest.mark.parametrize(
        'params,console_message', [
            ({'value': 'value', 'env_file': os.environ['FAILUREBASE_CONFIGURATION']}, 'created successfully'),
            ({'value': '1234', 'env_file': os.environ['FAILUREBASE_CONFIGURATION']}, 'created successfully'),
            ({'value': 's 1', 'env_file': os.environ['FAILUREBASE_CONFIGURATION']}, 'created successfully'),
        ]
    )
    def test_create_api_key_command(self, params, console_message, database_session, capsys):

        number_of_api_keys_before = len(database_session.query(ApiKey).all())

        command = CreateApiKeyCommand()
        command.execute(**params)

        captured = capsys.readouterr()

        assert console_message in captured.out

        number_of_api_keys_after = len(database_session.query(ApiKey).all())

        assert number_of_api_keys_after == number_of_api_keys_before + 1

    def test_show_api_key_command(self, database_session, capsys):

        command = ShowApiKeyCommand()
        command.execute(env_file=os.environ['FAILUREBASE_CONFIGURATION'])

        captured = capsys.readouterr()

        assert '- id: ' in captured.out
        assert '  value: ' in captured.out

    def test_delete_api_key_command(self, database_session, capsys):
        number_of_api_keys_before = len(database_session.query(ApiKey).all())

        command = DeleteApiKeyCommand()
        command.execute(api_key_id=1, env_file=os.environ['FAILUREBASE_CONFIGURATION'])

        captured = capsys.readouterr()

        print(captured)

        number_of_api_keys_after = len(database_session.query(ApiKey).all())

        assert number_of_api_keys_after == number_of_api_keys_before - 1


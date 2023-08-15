import os
import pytest

from failurebase.cli.commands.api_key import CreateApiKeyCommand, ShowApiKeyCommand, DeleteApiKeyCommand
from failurebase.cli.commands.configuration import CreateConfigurationFileCommand
from failurebase.cli.commands.frontend import CreateClientFrontendCommand
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

        assert 'deleted successfully' in captured.out

        number_of_api_keys_after = len(database_session.query(ApiKey).all())

        assert number_of_api_keys_after == number_of_api_keys_before - 1


class TestConfigurationCommands:

    def test_create_configuration_file_command(self, tmp_path, capsys):

        command = CreateConfigurationFileCommand()
        command.execute(dest=tmp_path)

        captured = capsys.readouterr()

        file = tmp_path / 'config' / '.env'

        assert file.exists()
        assert 'created successfully' in ''.join(captured.out)


class TestFrontendCommands:

    def test_create_frontend_files_command(self, tmp_path, capsys):

        api_url = 'https://your-domain.com'

        command = CreateClientFrontendCommand()
        command.execute(url=api_url, dest=tmp_path)

        captured = capsys.readouterr()

        file = tmp_path / 'frontend' / 'index.html'

        print(''.join(captured.out))

        assert file.exists()
        assert api_url in open(file, 'r').read()
        assert 'created successfully' in ''.join(captured.out)

"""Main CLI module."""

from argparse import Namespace

from failurebase.cli.utils import PARSER, ExitCode
from failurebase.cli.commands.api_key import CreateApiKeyCommand, ShowApiKeyCommand, DeleteApiKeyCommand
from failurebase.cli.commands.configuration import CreateConfigurationFileCommand
from failurebase.cli.commands.frontend import CreateClientFrontendCommand


class Cli:
    """Commands dispatcher."""

    COMMANDS = {
        PARSER.CONFIG_CREATE: CreateConfigurationFileCommand(),
        PARSER.FRONTEND_CREATE: CreateClientFrontendCommand(),
        PARSER.API_KEY_CREATE: CreateApiKeyCommand(),
        PARSER.API_KEY_SHOW: ShowApiKeyCommand(),
        PARSER.API_KEY_DELETE: DeleteApiKeyCommand()
    }

    def run(self, args: Namespace) -> ExitCode:
        """Executes command based on given namespace."""

        command = self.COMMANDS.get(args.parser_type)
        status = command.execute(**vars(args))

        return status.value

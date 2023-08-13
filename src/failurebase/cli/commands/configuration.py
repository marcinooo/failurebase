"""Configration commands module."""

from pathlib import Path
from jinja2 import Template
from cryptography.fernet import Fernet

from failurebase.cli.commands.base import Command
from failurebase.cli.utils import ExitCode


class CreateConfigurationFileCommand(Command):
    """Manage creation of configuration files."""

    def execute(self, *args, **kwargs):
        """Performs main command action."""

        secret_key: str | None = kwargs.get('secret_key', Fernet.generate_key())
        dest: Path | str = kwargs.get('dest', Path.cwd())

        if isinstance(dest, str):
            dest = Path(dest)

        if not dest.exists():
            self.log(f'No such file or directory "{dest}"\n\n')
            return ExitCode.CONFIGURATION_FILE_ERROR

        src = Path(__file__).parent / 'resources' / 'config' / '.env'
        dest_dir = dest / 'config'
        dest_file = dest / 'config' / '.env'

        dest_dir.mkdir(exist_ok=True)

        if dest_file.exists():
            self.log(f'File already exists: "{dest_file}"\nDelete or rename it first.\n\n')
            return ExitCode.CONFIGURATION_FILE_ERROR

        self.log(f'Config file will be created under "{dest_file}"\n')

        with open(src, 'r') as rfh, open(dest_file, 'w') as wfh:
            template = Template(rfh.read())
            config = template.render({'secret_key': secret_key})
            wfh.write(config)

        self.log(f'File was successfully created.\n\n')

        return ExitCode.SUCCESS

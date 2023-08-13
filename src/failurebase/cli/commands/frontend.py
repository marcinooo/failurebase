"""Frontend commands module."""

import shutil
from pathlib import Path
from jinja2 import Template

from failurebase.cli.commands.base import Command
from failurebase.cli.utils import ExitCode


class CreateClientFrontendCommand(Command):
    """Manage creation of frontends files."""

    def execute(self, *args, **kwargs):
        """Performs main command action."""

        api_url: str = kwargs.get('api_url')
        dest: Path | str = kwargs.get('dest', Path.cwd())

        if isinstance(dest, str):
            dest = Path(dest)

        src = Path(__file__).parent / 'resources' / 'frontend'

        dest = dest / 'frontend'

        if not dest.exists():
            self.log(f'No such file or directory "{dest}"\n\n')
            return ExitCode.FILE_DOES_NOT_EXIST

        self.log(f'Frontend files will be created in "{dest}"\n\n')

        try:
            shutil.copytree(src, dest)
        except FileExistsError as error:
            self.log(f'Files could not be copied.\nError: {error}\n')
            return ExitCode.COPY_FILE_ERROR

        self._fill_api_url(dest / 'index.html', api_url)
        self.log(f'Files was successfully created.\n')

        return ExitCode.SUCCESS

    @staticmethod
    def _fill_api_url(file_path: Path, value: str) -> None:
        """Render html file with given api URL."""

        with open(file_path, 'r+') as fh:

            template = Template(fh.read())
            html = template.render(api_url=value)

            fh.seek(0)
            fh.write(html)

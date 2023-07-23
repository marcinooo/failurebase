"""Utils module."""

import shutil
import sys
from pathlib import Path
from jinja2 import Template


def render_client(api_url: str, dest: Path | str = Path.cwd()) -> None:
    """Copies frontend files to indicated directory. Adds api URL to index.html."""

    if isinstance(dest, str):
        dest = Path(dest)

    src = Path(__file__).parent / 'resources'

    dest_resource = dest / 'frontend'

    _show(f'Coping frontend files to "{dest_resource}"\n\n')

    try:
        shutil.copytree(src, dest_resource)
    except FileExistsError as error:
        _show(f'Files could not be copied.\nError: {error}\n')
    else:
        _fill_api_url(dest_resource / 'index.html', api_url)
        _show(f'Files was successfully copied.\n')


def _fill_api_url(file_path: Path, value: str) -> None:
    """Render html file with given api URL."""

    with open(file_path, 'r+') as fh:

        template = Template(fh.read())
        html = template.render(api_url=value)

        fh.seek(0)

        fh.write(html)


def _show(text: str) -> None:
    """Shows message in console."""
    sys.stdout.write(text)

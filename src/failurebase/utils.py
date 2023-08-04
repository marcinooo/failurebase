"""Utils module."""

import os
import sys
import shutil
from pathlib import Path
from jinja2 import Template
from cryptography.fernet import Fernet


def create_api_key(value: str, env_file: Path | str) -> None:

    if not Path(env_file).exists():
        _show(f'Configuration file does not exist\n')
        return

    _show(f'Configuration file: {env_file}\n')

    os.environ['FAILUREBASE_CONFIGURATION'] = str(env_file)

    from failurebase.application import create_app
    from failurebase.schemas.api_key import CreateApiKeySchema
    from failurebase.settings import CONFIGURATION_FILE_VARIABLE

    failurebase_app = create_app()

    api_key_service = failurebase_app.container.services.api_key_service()
    secret_manager = failurebase_app.container.managers.secret_manager()

    api_key_schema = CreateApiKeySchema(value=secret_manager.encrypt(value))
    api_key_service.create(api_key_schema)

    _show(f'Api key created successfully\n')


def render_config(secret_key: str | None = None, dest: Path | str = Path.cwd()) -> None:

    if secret_key is None:
        secret_key = Fernet.generate_key()

    data = {
        'secret_key': secret_key.decode('utf-8')
    }

    if isinstance(dest, str):
        dest = Path(dest)

    if not dest.exists():
        _show(f'No such file or directory "{dest}"\n\n')
        return

    src = Path(__file__).parent / 'resources' / 'config' / '.env'
    dest_dir = dest / 'config'
    dest_file = dest / 'config' / '.env'

    dest_dir.mkdir(exist_ok=True)

    if dest_file.exists():
        _show(f'File already exists: "{dest_file}"\nDelete or rename it first.\n\n')
        return

    _show(f'Config file will be created under "{dest_file}"\n')

    with open(src, 'r') as rfh, open(dest_file, 'w') as wfh:
        template = Template(rfh.read())
        config = template.render(data)
        wfh.write(config)

    _show(f'File was successfully created.\n\n')


def render_client(api_url: str, dest: Path | str = Path.cwd()) -> None:
    """Copies frontend files to indicated directory. Adds api URL to index.html."""

    if isinstance(dest, str):
        dest = Path(dest)

    src = Path(__file__).parent / 'resources' / 'frontend'

    dest = dest / 'frontend'

    if not dest.exists():
        _show(f'No such file or directory "{dest}"\n\n')
        return

    _show(f'Frontend files will be created in "{dest}"\n\n')

    try:
        shutil.copytree(src, dest)
    except FileExistsError as error:
        _show(f'Files could not be copied.\nError: {error}\n')
    else:
        _fill_api_url(dest / 'index.html', api_url)
        _show(f'Files was successfully created.\n')


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

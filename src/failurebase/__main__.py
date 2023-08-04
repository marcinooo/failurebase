"""Makes package runnable as module."""

import sys
import argparse
from enum import Enum
from pathlib import Path

from .utils import render_client, create_api_key, render_config


class PARSER(Enum):
    CONFIG_CREATE = 11
    FRONTEND_CREATE = 21
    API_KEY_CREATE = 31
    API_KEY_SHOW = 32


def cli(args):
    """
    Perform given actions based on parsed arguments.

    :param args: namespace built from parsed attributes
    :type args: argparse.Namespace
    """
    if args.parser_type == PARSER.CONFIG_CREATE:
        render_config(args.secret_key, args.dest)
    elif args.parser_type == PARSER.FRONTEND_CREATE:
        render_client(args.url, args.dest)
    elif args.parser_type == PARSER.API_KEY_CREATE:
        create_api_key(args.value, args.env_file)
    elif args.parser_type == PARSER.API_KEY_SHOW:
        print('API_KEY_SHOW')


def main():

    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(help='select an instance to manage')
    subparsers.required = True

    # Config subparser
    config_parser = subparsers.add_parser('config')
    config_parser.set_defaults(parser_type='config')

    config_subparsers = config_parser.add_subparsers(help='select management command')
    config_subparsers.required = True

    config_create_parser = config_subparsers.add_parser('create')
    config_create_parser.set_defaults(parser_type=PARSER.CONFIG_CREATE)
    config_create_parser.add_argument('-s', '--secret-key', type=str, required=False, default=None,
                                      help='Secret key.')
    config_create_parser.add_argument('-d', '--dest', type=str, required=False, default=str(Path.cwd()),
                                      help='Path where to create config file.')

    # Frontend parser
    frontend_parser = subparsers.add_parser('frontend')
    frontend_parser.set_defaults(parser_type='frontend')

    frontend_subparsers = frontend_parser.add_subparsers(help='select management command')
    frontend_subparsers.required = True

    frontend_create_parser = frontend_subparsers.add_parser('create')
    frontend_create_parser.set_defaults(parser_type=PARSER.FRONTEND_CREATE)
    frontend_create_parser.add_argument('-u', '--url', type=str, required=True,
                                        help='server url in "<http or https>://<ip>:<port>" format')
    frontend_create_parser.add_argument('-d', '--dest', type=str, required=False, default=str(Path.cwd()),
                                        help='Path where to render frontend files.')

    # Api Key parser
    api_key_parser = subparsers.add_parser('api-key')
    api_key_parser.set_defaults(parser_type='api-key')

    api_key_subparsers = api_key_parser.add_subparsers(help='select management command')
    api_key_subparsers.required = True

    api_key_create_parser = api_key_subparsers.add_parser('create')
    api_key_create_parser.set_defaults(parser_type=PARSER.API_KEY_CREATE)
    api_key_create_parser.add_argument('-v', '--value', type=str, required=True,
                                       help='Value of API KEY. Failurebase will ask about it later.')
    api_key_create_parser.add_argument('-e', '--env-file', type=str, required=True,
                                       help='Path to configuration file which will be used by server.')

    api_key_show_parser = api_key_subparsers.add_parser('show')
    api_key_show_parser.set_defaults(parser_type=PARSER.API_KEY_SHOW)

    args = parser.parse_args()
    cli(args)

    return 0


if __name__ == "__main__":
    sys.exit(main())

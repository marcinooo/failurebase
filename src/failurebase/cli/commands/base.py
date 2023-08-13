"""Base commands module."""

import sys
from abc import ABCMeta, abstractmethod

from failurebase.cli.utils import ExitCode


class Command(metaclass=ABCMeta):
    """Base command interface."""

    @abstractmethod
    def execute(self, *args, **kwargs) -> ExitCode:
        """Executes current command"""

    @staticmethod
    def log(text: str) -> None:
        """Shows message in console."""

        sys.stdout.write(text)

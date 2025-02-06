# Copyright (c) 2024 - 2025 Noppanut Ploywong (@noppanut15) <noppanut.connect@gmail.com>
# Apache License 2.0 (see LICENSE file or http://www.apache.org/licenses/LICENSE-2.0)


"""A module for parsing a CSV file containing depth data.

This module contains the abstract base class `DiveLogCsvParser` 
for parsing a CSV file containing depth data.
"""

from abc import abstractmethod
from depthviz.parsers.generic.generic_divelog_parser import (
    DiveLogParser,
    DiveLogParserError,
)


class DiveLogCsvParserError(DiveLogParserError):
    """Base class for exceptions in this module."""


class DiveLogCsvInvalidHeaderError(DiveLogParserError):
    """Exception raised for missing target header errors."""


class DiveLogCsvParser(DiveLogParser):
    """A generic class to parse a CSV file containing depth data."""

    @abstractmethod
    def parse(self, file_path: str) -> None:
        """Parses a CSV file containing depth data.

        Args:
            file_path: The path to the CSV file to be parsed.
        """

    @abstractmethod
    def get_time_data(self) -> list[float]:
        """Returns the time data parsed from the CSV file.

        Returns:
            The time data parsed from the CSV file.
        """

    @abstractmethod
    def get_depth_data(self) -> list[float]:
        """Returns the depth data parsed from the CSV file.

        Returns:
            The depth data parsed from the CSV file.
        """

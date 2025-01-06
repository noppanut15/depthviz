"""
This module contains the DiveLogCsvParser base class 
which is used to parse a CSV file containing depth data.
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
    """
    A class to parse a CSV file containing depth data.
    """

    @abstractmethod
    def parse(self, file_path: str) -> None:
        """
        Parses a CSV file containing depth data.

        Parameters:
        file_path (str): The path to the CSV file to be parsed.
        """

    @abstractmethod
    def get_time_data(self) -> list[float]:
        """
        Returns the time data parsed from the CSV file.

        Returns:
        list[float]: The time data parsed from the CSV file.
        """

    @abstractmethod
    def get_depth_data(self) -> list[float]:
        """
        Returns the depth data parsed from the CSV file.

        Returns:
        list[float]: The depth data parsed from the CSV file.
        """

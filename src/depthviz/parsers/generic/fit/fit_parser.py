"""
This module contains the DiveLogFitParser base class 
which is used to parse a FIT file containing depth data.
"""

from abc import abstractmethod
from depthviz.parsers.generic.generic_divelog_parser import (
    DiveLogParser,
    DiveLogParserError,
)


class DiveLogFitParserError(DiveLogParserError):
    """Base class for exceptions in this module."""


class DiveLogFitInvalidFitFileError(DiveLogFitParserError):
    """Exception raised for errors related to invalid FIT files."""


class DiveLogFitInvalidFitFileTypeError(DiveLogFitParserError):
    """Exception raised for errors related to invalid FIT file types."""


class DiveLogFitDiveNotFoundError(DiveLogFitParserError):
    """Exception raised when a dive is not found in the FIT file."""


class DiveLogFitParser(DiveLogParser):
    """
    A class to parse a FIT file containing depth data.
    """

    @abstractmethod
    def parse(self, file_path: str) -> None:
        """
        Parses a FIT file containing depth data.

        Parameters:
        file_path (str): The path to the FIT file to be parsed.
        """

    @abstractmethod
    def get_time_data(self) -> list[float]:
        """
        Returns the time data parsed from the FIT file.

        Returns:
        list[float]: The time data parsed from the FIT file.
        """

    @abstractmethod
    def get_depth_data(self) -> list[float]:
        """
        Returns the depth data parsed from the FIT file.

        Returns:
        list[float]: The depth data parsed from the FIT file.
        """

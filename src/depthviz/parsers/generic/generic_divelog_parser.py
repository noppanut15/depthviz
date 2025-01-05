"""
This module contains the DiveLogParser base class 
which is used to parse a dive log file containing depth data.
"""

from abc import ABC, abstractmethod


class DiveLogParserError(Exception):
    """Base class for exceptions in this module."""


class DiveLogFileNotFoundError(DiveLogParserError):
    """Exception raised for file not found errors."""


class InvalidTimeValueError(DiveLogParserError):
    """Exception raised for invalid time value errors."""


class InvalidDepthValueError(DiveLogParserError):
    """Exception raised for invalid depth value errors."""


class EmptyFileError(DiveLogParserError):
    """Exception raised for empty file errors."""


class DiveLogParser(ABC):
    """
    A class to parse a dive log file containing depth data.
    """

    @abstractmethod
    def parse(self, file_path: str) -> None:
        """
        Parses a dive log file containing depth data.

        Parameters:
        file_path (str): The path to the dive log file to be parsed.
        """

    @abstractmethod
    def get_time_data(self) -> list[float]:
        """
        Returns the time data parsed from the dive log file.

        Returns:
        list[float]: The time data parsed from the dive log file.
        """

    @abstractmethod
    def get_depth_data(self) -> list[float]:
        """
        Returns the depth data parsed from the dive log file.

        Returns:
        list[float]: The depth data parsed from the dive log file.
        """

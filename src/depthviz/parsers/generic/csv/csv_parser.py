"""
This module contains the CsvParser base class 
which is used to parse a CSV file containing depth data.
"""

from abc import ABC, abstractmethod


class CsvParserError(Exception):
    """Base class for exceptions in this module."""


class CsvFileNotFoundError(CsvParserError):
    """Exception raised for file not found errors."""


class InvalidHeaderError(CsvParserError):
    """Exception raised for missing target header errors."""


class InvalidDepthValueError(CsvParserError):
    """Exception raised for invalid depth value errors."""


class EmptyFileError(CsvParserError):
    """Exception raised for empty file errors."""


class CsvParser(ABC):
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
    def get_depth_data(self) -> list[float]:
        """
        Returns the depth data parsed from the CSV file.

        Returns:
        list[float]: The depth data parsed from the CSV file.
        """

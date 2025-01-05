"""
This module contains the XmlParser base class 
which is used to parse a XML file containing depth data.
"""

from abc import abstractmethod
from depthviz.parsers.generic.generic_divelog_parser import (
    DiveLogParser,
    DiveLogParserError,
)


class DiveLogXmlParserError(DiveLogParserError):
    """Base class for exceptions in this module."""


class DiveLogXmlInvalidRootElementError(DiveLogXmlParserError):
    """Exception raised for an invalid root element in the XML file."""


class DiveLogXmlInvalidElementError(DiveLogXmlParserError):
    """Exception raised for an invalid element in the XML file."""


class DiveLogXmlFileContentUnreadableError(DiveLogXmlParserError):
    """Exception raised for unreadable XML file content."""


class DiveLogXmlParser(DiveLogParser):
    """
    A class to parse a XML file containing depth data.
    """

    @abstractmethod
    def parse(self, file_path: str) -> None:
        """
        Parses a XML file containing depth data.

        Parameters:
        file_path (str): The path to the XML file to be parsed.
        """

    @abstractmethod
    def get_time_data(self) -> list[float]:
        """
        Returns the time data parsed from the XML file.

        Returns:
        list[float]: The time data parsed from the XML file.
        """

    @abstractmethod
    def get_depth_data(self) -> list[float]:
        """
        Returns the depth data parsed from the XML file.

        Returns:
        list[float]: The depth data parsed from the XML file.
        """

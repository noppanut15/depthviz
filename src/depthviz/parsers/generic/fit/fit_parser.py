# Copyright (c) 2024 - 2025 Noppanut Ploywong (@noppanut15) <noppanut.connect@gmail.com>
# Apache License 2.0 (see LICENSE file or http://www.apache.org/licenses/LICENSE-2.0)


"""This module contains the abstract base class for FIT file parsers.

The FIT file format is a binary file format used by Garmin devices (and some other brands) 
to store activity data. This module provides an abstract base class for FIT file parsers 
that can be used to parse FIT files containing depth data.
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
    """A class to parse a FIT file containing depth data."""

    @abstractmethod
    def parse(self, file_path: str) -> None:
        """Parses a FIT file containing depth data.

        Args:
            file_path: The path to the FIT file to be parsed.
        """

    @abstractmethod
    def get_time_data(self) -> list[float]:
        """Returns the time data parsed from the FIT file.

        Returns:
            The time data parsed from the FIT file.
        """

    @abstractmethod
    def get_depth_data(self) -> list[float]:
        """Returns the depth data parsed from the FIT file.

        Returns:
            The depth data parsed from the FIT file.
        """

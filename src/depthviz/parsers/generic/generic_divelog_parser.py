"""This module contains the DiveLogParser abstract base class.

The DiveLogParser class is an abstract base class that defines the interface
for parsing a dive log file containing depth data. The class also provides
methods for ensuring that the depth data starts and ends at zero, and for
executing the depth mode operation on the depth and time data.

Constants:
    ASSUMED_DESCENT_RATE (float): The assumed descent rate in meters per second.
        The descent rate is used to calculate the duration of the descent phase
        when ensuring that the depth data starts at zero.
    ASSUMED_ASCENT_RATE (float): The assumed ascent rate in meters per second. 
        The ascent rate is used to calculate the duration of the ascent phase when 
        ensuring that the depth data ends at zero.
    ASCENT_CUTOFF_DEPTH (float): The ascent cutoff depth in meters. If the depth
        is less than this value, it is considered to be at the surface. This
        value is used to determine the end of the dive.
"""

from abc import ABC, abstractmethod

ASSUMED_DESCENT_RATE = 1  # meters per second
ASSUMED_ASCENT_RATE = 1  # meters per second
ASCENT_CUTOFF_DEPTH = 1  # meters


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
    """A class to parse a dive log file containing depth data."""

    def __init__(self, depth_mode: str) -> None:
        """Initializes the DiveLogParser object."""
        self.time_data: list[float] = []
        self.depth_data: list[float] = []
        self.depth_mode = depth_mode

    @abstractmethod
    def parse(self, file_path: str) -> None:
        """Parses a dive log file containing depth data.

        Args:
            file_path (str): The path to the dive log file to be parsed.
        """

    @abstractmethod
    def get_time_data(self) -> list[float]:
        """Returns the time data parsed from the dive log file.

        Returns:
            The time data parsed from the dive log file.
        """

    @abstractmethod
    def get_depth_data(self) -> list[float]:
        """Returns the depth data parsed from the dive log file.

        Returns:
            The depth data parsed from the dive log file.
        """

    def ensure_zero_depth_at_surface(self) -> None:
        """Ensures that the depth data starts and ends at zero.

        Note:
            This is a helper method which will be called by depth_mode_execute().
        """
        # Step 1: Ensure that the depth data STARTS at zero
        first_depth = self.depth_data[0]
        first_time = self.time_data[0]
        if first_depth > 0:
            self.depth_data.insert(0, 0)
            duration = (1 / ASSUMED_DESCENT_RATE) * first_depth
            self.time_data.insert(0, first_time - duration)

        # Step 2: Ensure that the depth data END at zero
        last_depth = self.depth_data[-1]
        last_time = self.time_data[-1]
        if last_depth > 0:
            # Clean up the depth data to remove any values close to zero
            # (between 0 and ASCENT_CUTOFF_DEPTH)
            for idx in range(len(self.depth_data) - 1, -1, -1):
                if self.depth_data[idx] < ASCENT_CUTOFF_DEPTH:
                    self.depth_data.pop(idx)
                    self.time_data.pop(idx)
                else:
                    break
            # Add a zero depth value at the end
            last_time = self.time_data[-1]
            last_depth = self.depth_data[-1]
            self.depth_data.append(0)
            duration = (1 / ASSUMED_ASCENT_RATE) * last_depth
            self.time_data.append(last_time + duration)

        # Step 3: Ensure the time data is positive (by starting at zero)
        self.time_data = [time - self.time_data[0] for time in self.time_data]

    def depth_mode_execute(self) -> None:
        """Executes the depth mode operation on the depth and time data.

        Mode of operation:
            `zero-based`: Ensures that the depth data starts and ends at zero.
            `raw`: No operation needed. (The starting and ending depth values are not modified.)

        Raises:
            DiveLogParserError: If the depth mode is invalid.
        """
        if self.depth_mode == "zero-based":
            self.ensure_zero_depth_at_surface()
        elif self.depth_mode == "raw":
            # No operation needed
            pass
        else:
            raise DiveLogParserError("Invalid depth mode")

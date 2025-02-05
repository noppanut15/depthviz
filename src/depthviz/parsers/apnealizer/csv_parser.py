# Copyright (c) 2024 - 2025 Noppanut Ploywong (@noppanut15) <noppanut.connect@gmail.com>
# Apache License 2.0 (see LICENSE file or http://www.apache.org/licenses/LICENSE-2.0)


"""A module for parsing a CSV file containing depth data from Apnealizer."""

import csv
from depthviz.parsers.generic.generic_divelog_parser import (
    DiveLogFileNotFoundError,
    InvalidTimeValueError,
    InvalidDepthValueError,
    EmptyFileError,
)

from depthviz.parsers.generic.csv.csv_parser import (
    DiveLogCsvParser,
    DiveLogCsvInvalidHeaderError,
)


class ApnealizerCsvParser(DiveLogCsvParser):
    """A class to parse a CSV file containing depth data."""

    def __init__(self, depth_mode: str = "raw") -> None:
        """Initializes the ApnealizerCsvParser object.

        Args:
            depth_mode: The depth mode to use for parsing the CSV file.
        """
        super().__init__(depth_mode=depth_mode)

    def parse(self, file_path: str) -> None:
        """Parses a CSV file containing depth data.

        Args:
            file_path: Path to the CSV file containing depth data.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file, delimiter=",")
                for row in reader:
                    if "Time" in row and "Depth" in row:
                        try:
                            self.time_data.append(float(row["Time"]))
                        except ValueError as e:
                            raise InvalidTimeValueError(
                                "Invalid CSV: Invalid time values"
                            ) from e
                        try:
                            self.depth_data.append(float(row["Depth"]))
                        except ValueError as e:
                            raise InvalidDepthValueError(
                                "Invalid CSV: Invalid depth values"
                            ) from e
                    else:
                        raise DiveLogCsvInvalidHeaderError(
                            "Invalid CSV: Target header not found"
                        )
            if not self.depth_data or not self.time_data:
                raise EmptyFileError("Invalid CSV: File is empty")
        except FileNotFoundError as e:
            raise DiveLogFileNotFoundError(
                f"Invalid CSV: File not found: {file_path}"
            ) from e

        # Convert depth data according to the depth mode
        self.depth_mode_execute()

    def get_time_data(self) -> list[float]:
        """Returns the time data parsed from the CSV file.

        Returns:
            The time data parsed from the CSV file.
        """
        return self.time_data

    def get_depth_data(self) -> list[float]:
        """Returns the depth data parsed from the CSV file.

        Returns:
            The depth data parsed from the CSV file.
        """
        return self.depth_data

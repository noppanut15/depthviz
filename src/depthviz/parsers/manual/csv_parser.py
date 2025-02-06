# Copyright (c) 2024 - 2025 Noppanut Ploywong (@noppanut15) <noppanut.connect@gmail.com>
# Apache License 2.0 (see LICENSE file or http://www.apache.org/licenses/LICENSE-2.0)


"""A module for parsing a CSV file containing depth data for manual input."""

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


class ManualCsvParser(DiveLogCsvParser):
    """A class to parse a CSV file containing depth data."""

    def __init__(self, depth_mode: str = "raw") -> None:
        """Initializes the ManualCsvParser object.

        Args:
            depth_mode: The depth mode to be used for the parser.
        """
        super().__init__(depth_mode=depth_mode)

    def parse(self, file_path: str) -> None:
        """Parses a CSV file containing depth data.

        Args:
            file_path: Path to the CSV file containing depth data.

        Raises:
            DiveLogFileNotFoundError: If the CSV file is not found.
            InvalidTimeValueError: If the time value in the CSV file is invalid.
            InvalidDepthValueError: If the depth value in the CSV file is invalid.
            DiveLogCsvInvalidHeaderError: If the headers in the CSV file are invalid.
            EmptyFileError: If the CSV file is empty.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file, delimiter=",")
                for i, row in enumerate(reader):
                    # The row in the CSV file
                    excel_row = i + 2
                    if "Time" in row and "Depth" in row:
                        try:
                            time_value = float(row["Time"])
                            if time_value < 0:
                                raise InvalidTimeValueError(
                                    f"Invalid CSV: Invalid time value at row {excel_row}, "
                                    "the value must be positive"
                                )
                            self.time_data.append(time_value)
                        except ValueError as e:
                            raise InvalidTimeValueError(
                                f"Invalid CSV: Invalid time value at row {excel_row}"
                            ) from e
                        try:
                            depth_value = float(row["Depth"])
                            if depth_value < 0:
                                raise InvalidDepthValueError(
                                    f"Invalid CSV: Invalid depth value at row {excel_row}, "
                                    "the value must be positive"
                                )
                            self.depth_data.append(depth_value)
                        except ValueError as e:
                            raise InvalidDepthValueError(
                                f"Invalid CSV: Invalid depth values at row {excel_row}"
                            ) from e
                    else:
                        raise DiveLogCsvInvalidHeaderError(
                            "Invalid CSV: Invalid headers in CSV file, make sure "
                            "there are 'Time' and 'Depth' columns in the CSV file"
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

"""
This module contains the ManualCsvParser class 
which is used to parse a CSV file from the user's manual input.
"""

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
    """
    A class to parse a CSV file containing depth data.
    """

    def __init__(self) -> None:
        self.__time_data: list[float] = []
        self.__depth_data: list[float] = []

    def parse(self, file_path: str) -> None:
        """
        Parses a CSV file containing depth data.
        Args:
            file_path: Path to the CSV file containing depth data.
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
                            self.__time_data.append(time_value)
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
                            self.__depth_data.append(depth_value)
                        except ValueError as e:
                            raise InvalidDepthValueError(
                                f"Invalid CSV: Invalid depth values at row {excel_row}"
                            ) from e
                    else:
                        raise DiveLogCsvInvalidHeaderError(
                            "Invalid CSV: Invalid headers in CSV file, make sure "
                            "there are 'Time' and 'Depth' columns in the CSV file"
                        )
            if not self.__depth_data or not self.__time_data:
                raise EmptyFileError("Invalid CSV: File is empty")
        except FileNotFoundError as e:
            raise DiveLogFileNotFoundError(
                f"Invalid CSV: File not found: {file_path}"
            ) from e

    def get_time_data(self) -> list[float]:
        """
        Returns the time data parsed from the CSV file.
        Returns:
            The time data parsed from the CSV file.
        """
        return self.__time_data

    def get_depth_data(self) -> list[float]:
        """
        Returns the depth data parsed from the CSV file.
        Returns:
            The depth data parsed from the CSV file.
        """
        return self.__depth_data

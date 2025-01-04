"""
This module contains the ApnealizerCsvParser class 
which is used to parse a CSV file from the Apnealizer software.
"""

import csv
from depthviz.parsers.generic.csv.csv_parser import (
    CsvParser,
    CsvFileNotFoundError,
    EmptyFileError,
    InvalidDepthValueError,
    InvalidHeaderError,
)


class ApnealizerCsvParser(CsvParser):
    """
    A class to parse a CSV file containing depth data.
    """

    def __init__(self) -> None:
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
                for row in reader:
                    if "Depth" in row:
                        try:
                            self.__depth_data.append(float(row["Depth"]))
                        except ValueError as e:
                            raise InvalidDepthValueError(
                                "Invalid CSV: Invalid depth values"
                            ) from e
                    else:
                        raise InvalidHeaderError("Invalid CSV: Target header not found")
            if not self.__depth_data:
                raise EmptyFileError("Invalid CSV: File is empty")
        except FileNotFoundError as e:
            raise CsvFileNotFoundError(
                f"Invalid CSV: File not found: {file_path}"
            ) from e

    def get_depth_data(self) -> list[float]:
        """
        Returns the depth data parsed from the CSV file.
        Returns:
            The depth data parsed from the CSV file.
        """
        return self.__depth_data
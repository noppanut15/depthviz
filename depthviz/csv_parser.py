"""
This module contains the CsvParser class which is used to parse a CSV file containing depth data.
"""

import csv
# import sys

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

class CsvParser:
    """
    A class to parse a CSV file containing depth data.
    """
    def __init__(self):
        self.depth_data = []

    def parse(self, file_path):
        """
        Parses a CSV file containing depth data.
        Args:
            file_path: Path to the CSV file containing depth data.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file, delimiter=',')
                for row in reader:
                    if 'Depth' in row:
                        try:
                            self.depth_data.append(float(row['Depth']))
                        except ValueError as e:
                            raise InvalidDepthValueError("Invalid CSV: Invalid depth values") from e
                    else:
                        raise InvalidHeaderError("Invalid CSV: Target header not found")
            if not self.depth_data:
                raise EmptyFileError("Invalid CSV: File is empty")
        except FileNotFoundError as e:
            raise CsvFileNotFoundError(f"Invalid CSV: File not found: {file_path}") from e
        except KeyError as e:
            raise InvalidHeaderError("Invalid CSV: Target header not found") from e
        except ValueError as e:
            raise InvalidDepthValueError("Invalid CSV: Invalid depth values") from e

    def get_depth_data(self):
        """
        Returns the depth data.
        """
        return self.depth_data

# if __name__ == '__main__':
#     if len(sys.argv) != 2:
#         print("Usage: python csv_parser.py <file_path>")
#         sys.exit(1)

#     csv_file_path = sys.argv[1]
#     csv_parser = CsvParser()
#     try:
#         csv_parser.parse(csv_file_path)
#         print(csv_parser.get_depth_data())
#     except CsvParserError as e:
#         print(e)
#         sys.exit(1)
#     sys.exit(0)

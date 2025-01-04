"""
Unit tests for the ApnealizerCsvParser class.
"""

import os
import pytest
from depthviz.parsers.apnealizer.csv_parser import ApnealizerCsvParser
from depthviz.parsers.generic.csv.csv_parser import (
    InvalidHeaderError,
    InvalidDepthValueError,
    EmptyFileError,
    CsvFileNotFoundError,
)


class TestApnealizerCsvParser:
    """
    Test class for the ApnealizerCsvParser
    """

    def test_parse_valid_csv(self, request: pytest.FixtureRequest) -> None:
        """
        Test parsing a valid CSV file.
        """
        file_path = str(
            request.path.parent.joinpath("data", "valid_depth_data_trimmed.csv")
        )
        csv_parser = ApnealizerCsvParser()
        csv_parser.parse(file_path)
        assert csv_parser.get_depth_data() == [
            0.76,
            1.22,
            2.58,
            3.25,
            3.14,
            3.68,
            5.0,
            6.31,
            6.27,
            6.76,
        ]

    def test_parse_invalid_csv_x_header(self, request: pytest.FixtureRequest) -> None:
        """
        Test parsing a CSV file with an invalid header.
        """
        file_path = str(
            request.path.parent.joinpath("data", "invalid_data_x_header.csv")
        )
        csv_parser = ApnealizerCsvParser()
        with pytest.raises(InvalidHeaderError) as e:
            csv_parser.parse(file_path)
        assert str(e.value) == "Invalid CSV: Target header not found"

    def test_parse_empty_csv(self, request: pytest.FixtureRequest) -> None:
        """
        Test parsing an empty CSV file.
        """
        file_path = str(request.path.parent.joinpath("data", "empty_file.csv"))
        csv_parser = ApnealizerCsvParser()
        with pytest.raises(EmptyFileError) as e:
            csv_parser.parse(file_path)
        assert str(e.value) == "Invalid CSV: File is empty"

    def test_parse_invalid_csv_missing_depth(
        self, request: pytest.FixtureRequest
    ) -> None:
        """
        Test parsing a CSV file with missing depth values.
        """
        file_path = str(
            request.path.parent.joinpath("data", "invalid_data_x_depth.csv")
        )
        csv_parser = ApnealizerCsvParser()
        with pytest.raises(InvalidDepthValueError) as e:
            csv_parser.parse(file_path)
        assert str(e.value) == "Invalid CSV: Invalid depth values"

    def test_parse_invalid_csv_missing_file(
        self, request: pytest.FixtureRequest
    ) -> None:
        """
        Test parsing a missing CSV file.
        """
        file_path = str(request.path.parent.joinpath("data", "missing_file_xyz.csv"))
        csv_parser = ApnealizerCsvParser()
        assert not os.path.exists(file_path)
        with pytest.raises(CsvFileNotFoundError) as e:
            csv_parser.parse(file_path)
        assert str(e.value) == f"Invalid CSV: File not found: {file_path}"

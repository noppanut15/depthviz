"""
Unit tests for the ManualCsvParser class.
"""

import os
import pytest
from depthviz.parsers.manual.csv_parser import ManualCsvParser
from depthviz.parsers.generic.generic_divelog_parser import (
    DiveLogFileNotFoundError,
    InvalidTimeValueError,
    InvalidDepthValueError,
    EmptyFileError,
)

from depthviz.parsers.generic.csv.csv_parser import (
    DiveLogCsvInvalidHeaderError,
)


class TestManualCsvParser:
    """
    Test class for the ManualCsvParser
    """

    def test_parse_valid_csv(self, request: pytest.FixtureRequest) -> None:
        """
        Test parsing a valid CSV file.
        """
        file_path = str(
            request.path.parent.joinpath(
                "data", "manual", "valid_depth_data_trimmed.csv"
            )
        )
        csv_parser = ManualCsvParser()
        csv_parser.parse(file_path)
        assert csv_parser.get_depth_data() == [
            0.0,
            5.0,
            0.0,
        ]
        assert csv_parser.get_time_data() == [
            0.0,
            5.0,
            10.0,
        ]

    def test_parse_invalid_csv_x_header(self, request: pytest.FixtureRequest) -> None:
        """
        Test parsing a CSV file with an invalid header.
        """
        file_path = str(
            request.path.parent.joinpath("data", "manual", "invalid_data_x_header.csv")
        )
        csv_parser = ManualCsvParser()
        with pytest.raises(DiveLogCsvInvalidHeaderError) as e:
            csv_parser.parse(file_path)
        assert (
            str(e.value)
            == "Invalid CSV: Invalid headers in CSV file, make sure there are 'Time' and 'Depth' columns in the CSV file"
        )

    def test_parse_empty_csv(self, request: pytest.FixtureRequest) -> None:
        """
        Test parsing an empty CSV file.
        """
        file_path = str(
            request.path.parent.joinpath("data", "manual", "empty_file.csv")
        )
        csv_parser = ManualCsvParser()
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
            request.path.parent.joinpath("data", "manual", "invalid_data_x_depth.csv")
        )
        csv_parser = ManualCsvParser()
        with pytest.raises(InvalidDepthValueError) as e:
            csv_parser.parse(file_path)
        assert str(e.value) == "Invalid CSV: Invalid depth values at row 2"

    def test_parse_invalid_csv_missing_file(
        self, request: pytest.FixtureRequest
    ) -> None:
        """
        Test parsing a missing CSV file.
        """
        file_path = str(
            request.path.parent.joinpath("data", "manual", "missing_file_xyz.csv")
        )
        csv_parser = ManualCsvParser()
        assert not os.path.exists(file_path)
        with pytest.raises(DiveLogFileNotFoundError) as e:
            csv_parser.parse(file_path)
        assert str(e.value) == f"Invalid CSV: File not found: {file_path}"

    def test_parse_invalid_csv_missing_time(
        self, request: pytest.FixtureRequest
    ) -> None:
        """
        Test parsing a CSV file with missing time values.
        """
        file_path = str(
            request.path.parent.joinpath(
                "data", "manual", "invalid_time_depth_mismatched.csv"
            )
        )
        csv_parser = ManualCsvParser()
        with pytest.raises(InvalidTimeValueError) as e:
            csv_parser.parse(file_path)
        assert str(e.value) == "Invalid CSV: Invalid time value at row 11"

    def test_parse_invalid_csv_negative_depth(
        self, request: pytest.FixtureRequest
    ) -> None:
        """
        Test parsing a CSV file with negative depth values.
        """
        file_path = str(
            request.path.parent.joinpath(
                "data", "manual", "invalid_data_negative_depth.csv"
            )
        )
        csv_parser = ManualCsvParser()
        with pytest.raises(InvalidDepthValueError) as e:
            csv_parser.parse(file_path)
        assert (
            str(e.value)
            == "Invalid CSV: Invalid depth value at row 3, the value must be positive"
        )

    def test_parse_invalid_csv_negative_time(
        self, request: pytest.FixtureRequest
    ) -> None:
        """
        Test parsing a CSV file with negative time values.
        """
        file_path = str(
            request.path.parent.joinpath(
                "data", "manual", "invalid_data_negative_time.csv"
            )
        )
        csv_parser = ManualCsvParser()
        with pytest.raises(InvalidTimeValueError) as e:
            csv_parser.parse(file_path)
        assert (
            str(e.value)
            == "Invalid CSV: Invalid time value at row 4, the value must be positive"
        )

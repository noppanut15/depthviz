# Copyright (c) 2024 - 2025 Noppanut Ploywong (@noppanut15) <noppanut.connect@gmail.com>
# Apache License 2.0 (see LICENSE file or http://www.apache.org/licenses/LICENSE-2.0)


"""Unit tests for the ApnealizerCsvParser class."""

import os
from unittest.mock import patch, Mock
import pytest
from depthviz.parsers.apnealizer.csv_parser import ApnealizerCsvParser
from depthviz.parsers.generic.generic_divelog_parser import (
    DiveLogFileNotFoundError,
    InvalidTimeValueError,
    InvalidDepthValueError,
    EmptyFileError,
)

from depthviz.parsers.generic.csv.csv_parser import (
    DiveLogCsvInvalidHeaderError,
)


class TestApnealizerCsvParser:
    """Test class for the ApnealizerCsvParser."""

    def test_parse_valid_csv(self, request: pytest.FixtureRequest) -> None:
        """Test parsing a valid CSV file."""
        file_path = str(
            request.path.parent.joinpath(
                "data", "apnealizer", "valid_depth_data_trimmed.csv"
            )
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

    @pytest.mark.parametrize("depth_mode", ["raw", "zero-based"])
    @patch(
        "depthviz.parsers.apnealizer.csv_parser.ApnealizerCsvParser.depth_mode_execute"
    )
    def test_parse_valid_csv_depth_mode_exec(
        self,
        mock_depth_mode_execute: Mock,
        depth_mode: str,
        request: pytest.FixtureRequest,
    ) -> None:
        """Test parsing a valid CSV file with depth mode execution."""
        file_path = str(
            request.path.parent.joinpath(
                "data", "apnealizer", "valid_depth_data_trimmed.csv"
            )
        )
        csv_parser = ApnealizerCsvParser(depth_mode=depth_mode)
        csv_parser.parse(file_path)
        mock_depth_mode_execute.assert_called_once()

    def test_parse_invalid_csv_x_header(self, request: pytest.FixtureRequest) -> None:
        """Test parsing a CSV file with an invalid header."""
        file_path = str(
            request.path.parent.joinpath(
                "data", "apnealizer", "invalid_data_x_header.csv"
            )
        )
        csv_parser = ApnealizerCsvParser()
        with pytest.raises(DiveLogCsvInvalidHeaderError) as e:
            csv_parser.parse(file_path)
        assert str(e.value) == "Invalid CSV: Target header not found"

    def test_parse_empty_csv(self, request: pytest.FixtureRequest) -> None:
        """Test parsing an empty CSV file."""
        file_path = str(
            request.path.parent.joinpath("data", "apnealizer", "empty_file.csv")
        )
        csv_parser = ApnealizerCsvParser()
        with pytest.raises(EmptyFileError) as e:
            csv_parser.parse(file_path)
        assert str(e.value) == "Invalid CSV: File is empty"

    def test_parse_invalid_csv_missing_depth(
        self, request: pytest.FixtureRequest
    ) -> None:
        """Test parsing a CSV file with missing depth values."""
        file_path = str(
            request.path.parent.joinpath(
                "data", "apnealizer", "invalid_data_x_depth.csv"
            )
        )
        csv_parser = ApnealizerCsvParser()
        with pytest.raises(InvalidDepthValueError) as e:
            csv_parser.parse(file_path)
        assert str(e.value) == "Invalid CSV: Invalid depth values"

    def test_parse_invalid_csv_missing_file(
        self, request: pytest.FixtureRequest
    ) -> None:
        """Test parsing a missing CSV file."""
        file_path = str(
            request.path.parent.joinpath("data", "apnealizer", "missing_file_xyz.csv")
        )
        csv_parser = ApnealizerCsvParser()
        assert not os.path.exists(file_path)
        with pytest.raises(DiveLogFileNotFoundError) as e:
            csv_parser.parse(file_path)
        assert str(e.value) == f"Invalid CSV: File not found: {file_path}"

    def test_parse_invalid_csv_missing_time(
        self, request: pytest.FixtureRequest
    ) -> None:
        """Test parsing a CSV file with missing time values."""
        file_path = str(
            request.path.parent.joinpath(
                "data", "apnealizer", "invalid_time_depth_mismatched.csv"
            )
        )
        csv_parser = ApnealizerCsvParser()
        with pytest.raises(InvalidTimeValueError) as e:
            csv_parser.parse(file_path)
        assert str(e.value) == "Invalid CSV: Invalid time values"

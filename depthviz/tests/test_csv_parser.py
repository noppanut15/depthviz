"""
Unit tests for the CsvParser class.
"""
import os
import pytest
from depthviz.csv_parser import CsvParser, \
                                InvalidHeaderError, \
                                InvalidDepthValueError, \
                                EmptyFileError, \
                                CsvFileNotFoundError

class TestCsvParser:
    """
    Test class for the CsvParser
    """
    def test_parse_valid_csv(self, request: pytest.FixtureRequest):
        """
        Test parsing a valid CSV file.
        """
        file_path = request.path.parent.joinpath('data', 'valid_depth_data_trimmed.csv')
        csv_parser = CsvParser()
        csv_parser.parse(file_path)
        assert csv_parser.get_depth_data() == [0.76, 1.22, 2.58, 3.25, 3.14,\
                                                3.68, 5.0, 6.31, 6.27, 6.76]

    def test_parse_invalid_csv_x_header(self, request: pytest.FixtureRequest):
        """
        Test parsing a CSV file with an invalid header.
        """
        file_path = request.path.parent.joinpath('data', 'invalid_data_x_header.csv')
        csv_parser = CsvParser()
        with pytest.raises(InvalidHeaderError):
            csv_parser.parse(file_path)

    def test_parse_empty_csv(self, request: pytest.FixtureRequest):
        """
        Test parsing an empty CSV file.
        """
        file_path = request.path.parent.joinpath('data', 'empty_file.csv')
        csv_parser = CsvParser()
        with pytest.raises(EmptyFileError):
            csv_parser.parse(file_path)

    def test_parse_invalid_csv_missing_depth(self, request: pytest.FixtureRequest):
        """
        Test parsing a CSV file with missing depth values.
        """
        file_path = request.path.parent.joinpath('data', 'invalid_data_x_depth.csv')
        csv_parser = CsvParser()
        with pytest.raises(InvalidDepthValueError):
            csv_parser.parse(file_path)

    def test_parse_invalid_csv_missing_file(self, request: pytest.FixtureRequest):
        """
        Test parsing a missing CSV file.
        """
        file_path = request.path.parent.joinpath('data', 'missing_file_xyz.csv')
        csv_parser = CsvParser()
        assert not os.path.exists(file_path)
        with pytest.raises(CsvFileNotFoundError):
            csv_parser.parse(file_path)

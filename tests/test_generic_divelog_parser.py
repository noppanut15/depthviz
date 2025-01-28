# Copyright (c) 2024 - 2025 Noppanut Ploywong (@noppanut15) <noppanut.connect@gmail.com>
# Apache License 2.0 (see LICENSE file or http://www.apache.org/licenses/LICENSE-2.0)


"""
Unit tests for the DiveLogParser class.
"""

import pytest
from depthviz.parsers.generic.generic_divelog_parser import (
    DiveLogParser,
    DiveLogParserError,
)


class ConcreteDiveLogParser(DiveLogParser):
    """
    A concrete class that inherits from DiveLogParser for testing purposes.
    """

    def parse(self, _: str) -> None:
        """
        A dummy implementation of the parse method.
        """

    def get_time_data(self) -> list[float]:
        """
        A dummy implementation of the get_time_data method.
        """
        return self.time_data

    def get_depth_data(self) -> list[float]:
        """
        A dummy implementation of the get_depth_data method.
        """
        return self.depth_data


class TestDiveLogParser:
    """
    Test class for the DiveLogParser
    """

    def test_depth_mode_execute_raw(self) -> None:
        """
        Test depth_mode_execute method for raw mode.
        """

        dive_log_parser = ConcreteDiveLogParser(depth_mode="raw")
        dive_log_parser.depth_data = [1.0, 2.0, 3.0, 4.0]
        dive_log_parser.time_data = [1.0, 2.0, 3.0, 4.0]
        dive_log_parser.depth_mode_execute()
        assert dive_log_parser.depth_data == [1.0, 2.0, 3.0, 4.0]
        assert dive_log_parser.time_data == [1.0, 2.0, 3.0, 4.0]

    @pytest.mark.parametrize(
        "depth_data,time_data,expected_depth_data,expected_time_data",
        [
            (
                [1.0, 2.0, 3.0, 4.0],
                [1.0, 2.0, 3.0, 4.0],
                [0.0, 1.0, 2.0, 3.0, 4.0, 0.0],
                [0.0, 1.0, 2.0, 3.0, 4.0, 8.0],
            ),
            (
                [
                    1.02,
                    1.05,
                    2.4,
                    3.36,
                    2.23,
                    2.07,
                    1.05,
                    0.3,
                    0.35,
                    0.24,
                    0.35,
                    0.28,
                    0.31,
                ],
                [
                    1,
                    2,
                    3,
                    4,
                    5,
                    6,
                    7,
                    8,
                    9,
                    10,
                    11,
                    12,
                    13,
                ],
                [
                    0.0,
                    1.02,
                    1.05,
                    2.4,
                    3.36,
                    2.23,
                    2.07,
                    1.05,
                    0.0,
                ],
                # After step 2: [-0.02, 1, 2, 3, 4, 5, 6, 7, 8.05],
                [0, 1.02, 2.02, 3.02, 4.02, 5.02, 6.02, 7.02, 8.07],
            ),
            (
                [0.1, 0.9, 1, 2, 3, 2, 1, 0.2, 0.1],
                [1, 2, 3, 4, 5, 6, 7, 8, 9],
                [0.0, 0.1, 0.9, 1, 2, 3, 2, 1, 0.0],
                # After step 2: [0.9, 1, 2, 3, 4, 5, 6, 7, 8],
                [0, 0.1, 1.1, 2.1, 3.1, 4.1, 5.1, 6.1, 7.1],
            ),
        ],
    )
    def test_depth_mode_execute_zero_based(
        self,
        depth_data: list[float],
        time_data: list[float],
        expected_depth_data: list[float],
        expected_time_data: list[float],
    ) -> None:
        """
        Test depth_mode_execute method for zero-based mode.
        """

        dive_log_parser = ConcreteDiveLogParser(depth_mode="zero-based")
        dive_log_parser.depth_data = depth_data
        dive_log_parser.time_data = time_data
        dive_log_parser.depth_mode_execute()
        assert pytest.approx(dive_log_parser.depth_data) == expected_depth_data
        assert pytest.approx(dive_log_parser.time_data) == expected_time_data

    def test_depth_mode_execute_invalid_depth_mode(self) -> None:
        """
        Test depth_mode_execute method for invalid depth mode.
        """

        dive_log_parser = ConcreteDiveLogParser(depth_mode="invalid")
        with pytest.raises(DiveLogParserError):
            dive_log_parser.depth_mode_execute()

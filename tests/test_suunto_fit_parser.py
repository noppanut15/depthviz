# Copyright (c) 2024 - 2025 Noppanut Ploywong (@noppanut15) <noppanut.connect@gmail.com>
# Apache License 2.0 (see LICENSE file or http://www.apache.org/licenses/LICENSE-2.0)


"""Unit tests for the SuuntoFitParser class."""

from typing import Any, Union
from unittest.mock import patch, Mock
import pytest
from garmin_fit_sdk import Stream, Decoder
from depthviz.parsers.suunto.fit_parser import SuuntoFitParser
from depthviz.parsers.generic.fit.fit_parser import (
    DiveLogFitInvalidFitFileError,
    DiveLogFitInvalidFitFileTypeError,
    DiveLogFitDiveNotFoundError,
)
from depthviz.parsers.generic.generic_divelog_parser import (
    DiveLogFileNotFoundError,
)


class TestSuuntoFitParser:
    """Test class for the SuuntoFitParser."""

    def _mock_stream_from_file(self, _: Any) -> None:
        """A mock function for the Stream.from_file method."""

    def _mock_decoder_init(
        self,
        *args: Union[str, bool],
        **kwargs: Union[str, bool],
    ) -> None:
        """A mock function for the Decoder.__init__ method."""

    @pytest.mark.parametrize(
        "file_path, selected_dive_idx, expected_time_data, expected_depth_data",
        [
            # 6.41m dive (2024-10-16T13:47:17.000Z)
            (
                "FreeDiving_2024-10-16T16_33_30.fit",
                0,
                [
                    0.0,
                    1.0,
                    2.0,
                    3.0,
                    4.0,
                    5.0,
                    6.0,
                    7.0,
                    8.0,
                    9.0,
                    10.0,
                    11.0,
                    12.0,
                    13.0,
                    14.0,
                    15.0,
                    16.0,
                    17.0,
                    18.0,
                    19.0,
                    20.0,
                    21.0,
                    22.0,
                    23.0,
                    24.0,
                    25.0,
                    26.0,
                    27.0,
                    28.0,
                ],
                [
                    0.00,
                    3.02,
                    3.75,
                    4.45,
                    4.98,
                    5.49,
                    6.18,
                    6.41,
                    6.18,
                    6.18,
                    5.97,
                    5.31,
                    4.98,
                    4.64,
                    4.08,
                    3.56,
                    3.00,
                    2.08,
                    1.51,
                    1.16,
                    0.38,
                    0.06,
                    0.04,
                    0.02,
                    0.02,
                    0.02,
                    0.01,
                    0.01,
                    0.01,
                ],
            ),
            # 9.63m dive (2024-10-16T13:50:28.000Z)
            (
                "FreeDiving_2024-10-16T16_33_30.fit",
                1,
                [
                    0.0,
                    1.0,
                    2.0,
                    3.0,
                    4.0,
                    5.0,
                    6.0,
                    7.0,
                    8.0,
                    9.0,
                    10.0,
                    11.0,
                    12.0,
                    13.0,
                    14.0,
                    15.0,
                    16.0,
                    17.0,
                    18.0,
                    19.0,
                    20.0,
                    21.0,
                    22.0,
                    23.0,
                    24.0,
                    25.0,
                    26.0,
                    27.0,
                    28.0,
                    29.0,
                    30.0,
                    31.0,
                    32.0,
                    33.0,
                    34.0,
                    35.0,
                    36.0,
                    37.0,
                    38.0,
                    39.0,
                    40.0,
                    41.0,
                ],
                [
                    0.20,
                    0.22,
                    0.24,
                    0.30,
                    0.76,
                    1.34,
                    1.93,
                    2.50,
                    3.03,
                    3.61,
                    4.29,
                    5.00,
                    5.63,
                    6.25,
                    6.75,
                    6.91,
                    7.21,
                    7.75,
                    8.11,
                    8.51,
                    8.90,
                    9.28,
                    9.63,
                    9.20,
                    9.22,
                    9.20,
                    8.70,
                    8.01,
                    6.83,
                    6.05,
                    5.52,
                    5.04,
                    4.54,
                    4.04,
                    3.49,
                    2.89,
                    2.25,
                    1.76,
                    1.20,
                    0.15,
                    0.03,
                    0.02,
                ],
            ),
            # 5.93m dive (2024-10-16T13:54:16.000Z)
            (
                "FreeDiving_2024-10-16T16_33_30.fit",
                2,
                [
                    0.0,
                    1.0,
                    2.0,
                    3.0,
                    4.0,
                    5.0,
                    6.0,
                    7.0,
                    8.0,
                    9.0,
                    10.0,
                    11.0,
                    12.0,
                    13.0,
                    14.0,
                    15.0,
                    16.0,
                    17.0,
                    18.0,
                    19.0,
                    20.0,
                    21.0,
                    22.0,
                ],
                [
                    0.89,
                    1.69,
                    2.52,
                    3.33,
                    3.91,
                    4.19,
                    4.18,
                    4.35,
                    5.41,
                    5.93,
                    5.64,
                    5.30,
                    4.68,
                    3.98,
                    3.65,
                    2.94,
                    2.28,
                    1.67,
                    0.81,
                    0.15,
                    0.06,
                    0.02,
                    0.01,
                ],
            ),
            # 11.35m dive (2024-10-16T13:56:48.000Z)
            (
                "FreeDiving_2024-10-16T16_33_30.fit",
                3,
                [
                    0.0,
                    1.0,
                    2.0,
                    3.0,
                    4.0,
                    5.0,
                    6.0,
                    7.0,
                    8.0,
                    9.0,
                    10.0,
                    11.0,
                    12.0,
                    13.0,
                    14.0,
                    15.0,
                    16.0,
                    17.0,
                    18.0,
                    19.0,
                    20.0,
                    21.0,
                    22.0,
                    23.0,
                    24.0,
                    25.0,
                    26.0,
                    27.0,
                    28.0,
                    29.0,
                    30.0,
                    31.0,
                    32.0,
                    33.0,
                    34.0,
                    35.0,
                    36.0,
                    37.0,
                    38.0,
                    39.0,
                    40.0,
                    41.0,
                    42.0,
                    43.0,
                    44.0,
                    45.0,
                    46.0,
                    47.0,
                    48.0,
                    49.0,
                    50.0,
                ],
                [
                    0.09,
                    0.24,
                    0.26,
                    0.34,
                    0.34,
                    0.48,
                    1.03,
                    1.73,
                    2.22,
                    2.87,
                    3.54,
                    4.21,
                    4.71,
                    4.99,
                    5.57,
                    6.29,
                    7.04,
                    7.82,
                    8.62,
                    9.23,
                    9.79,
                    10.32,
                    10.83,
                    11.35,
                    11.25,
                    11.32,
                    10.76,
                    10.29,
                    9.45,
                    8.75,
                    8.17,
                    7.60,
                    6.92,
                    6.51,
                    6.10,
                    5.66,
                    5.19,
                    4.69,
                    4.23,
                    3.71,
                    3.11,
                    2.43,
                    1.78,
                    1.06,
                    0.22,
                    0.04,
                    0.01,
                    0.01,
                    0.01,
                    0.01,
                    0.01,
                ],
            ),
            # 10.29m dive (2024-10-16T14:00:58.000Z)
            (
                "FreeDiving_2024-10-16T16_33_30.fit",
                4,
                [
                    0.0,
                    1.0,
                    2.0,
                    3.0,
                    4.0,
                    5.0,
                    6.0,
                    7.0,
                    8.0,
                    9.0,
                    10.0,
                    11.0,
                    12.0,
                    13.0,
                    14.0,
                    15.0,
                    16.0,
                    17.0,
                    18.0,
                    19.0,
                    20.0,
                    21.0,
                    22.0,
                    23.0,
                    24.0,
                    25.0,
                    26.0,
                    27.0,
                    28.0,
                    29.0,
                    30.0,
                    31.0,
                    32.0,
                    33.0,
                    34.0,
                    35.0,
                    36.0,
                    37.0,
                    38.0,
                    39.0,
                    40.0,
                    41.0,
                    42.0,
                    43.0,
                    44.0,
                    45.0,
                    46.0,
                    47.0,
                    48.0,
                    49.0,
                    50.0,
                ],
                [
                    0.21,
                    0.26,
                    0.30,
                    0.32,
                    0.36,
                    0.75,
                    1.55,
                    2.00,
                    2.47,
                    3.13,
                    3.79,
                    4.47,
                    5.04,
                    5.65,
                    6.30,
                    6.88,
                    7.39,
                    7.67,
                    8.05,
                    8.52,
                    8.89,
                    9.24,
                    9.64,
                    9.92,
                    9.99,
                    10.19,
                    10.29,
                    10.12,
                    9.37,
                    8.96,
                    8.90,
                    8.37,
                    7.91,
                    7.52,
                    7.20,
                    6.98,
                    6.74,
                    6.54,
                    6.23,
                    5.90,
                    5.52,
                    5.09,
                    4.60,
                    4.43,
                    3.92,
                    3.35,
                    2.74,
                    1.99,
                    1.09,
                    0.27,
                    0.01,
                ],
            ),
            # 10.02m dive (2024-10-16T14:04:59.000Z)
            (
                "FreeDiving_2024-10-16T16_33_30.fit",
                5,
                [
                    0.0,
                    1.0,
                    2.0,
                    3.0,
                    4.0,
                    5.0,
                    6.0,
                    7.0,
                    8.0,
                    9.0,
                    10.0,
                    11.0,
                    12.0,
                    13.0,
                    14.0,
                    15.0,
                    16.0,
                    17.0,
                    18.0,
                    19.0,
                    20.0,
                    21.0,
                    22.0,
                    23.0,
                    24.0,
                    25.0,
                    26.0,
                    27.0,
                    28.0,
                    29.0,
                    30.0,
                    31.0,
                    32.0,
                    33.0,
                    34.0,
                    35.0,
                    36.0,
                    37.0,
                    38.0,
                    39.0,
                    40.0,
                    41.0,
                    42.0,
                    43.0,
                    44.0,
                    45.0,
                    46.0,
                    47.0,
                    48.0,
                    49.0,
                    50.0,
                    51.0,
                    52.0,
                    53.0,
                    54.0,
                    55.0,
                    56.0,
                    57.0,
                ],
                [
                    0.16,
                    0.17,
                    0.22,
                    0.29,
                    0.32,
                    0.34,
                    0.37,
                    0.48,
                    0.89,
                    1.58,
                    1.89,
                    2.27,
                    2.61,
                    3.12,
                    3.83,
                    4.54,
                    5.22,
                    5.91,
                    6.56,
                    7.13,
                    7.43,
                    7.77,
                    8.10,
                    8.55,
                    8.97,
                    9.37,
                    9.72,
                    9.92,
                    10.01,
                    10.02,
                    9.84,
                    9.70,
                    9.73,
                    9.74,
                    9.63,
                    9.10,
                    8.19,
                    7.54,
                    7.01,
                    6.52,
                    6.06,
                    5.63,
                    5.28,
                    5.18,
                    5.11,
                    4.73,
                    4.45,
                    4.00,
                    3.48,
                    3.12,
                    2.49,
                    1.35,
                    0.43,
                    0.01,
                    0.01,
                    0.01,
                    0.01,
                    0.01,
                ],
            ),
            # 11.42m dive (2024-10-16T14:09:47.000Z)
            (
                "FreeDiving_2024-10-16T16_33_30.fit",
                6,
                [
                    0.0,
                    1.0,
                    2.0,
                    3.0,
                    4.0,
                    5.0,
                    6.0,
                    7.0,
                    8.0,
                    9.0,
                    10.0,
                    11.0,
                    12.0,
                    13.0,
                    14.0,
                    15.0,
                    16.0,
                    17.0,
                    18.0,
                    19.0,
                    20.0,
                    21.0,
                    22.0,
                    23.0,
                    24.0,
                    25.0,
                    26.0,
                    27.0,
                    28.0,
                    29.0,
                    30.0,
                    31.0,
                    32.0,
                    33.0,
                    34.0,
                    35.0,
                    36.0,
                    37.0,
                    38.0,
                    39.0,
                    40.0,
                    41.0,
                    42.0,
                    43.0,
                    44.0,
                    45.0,
                    46.0,
                    47.0,
                ],
                [
                    0.31,
                    0.62,
                    1.23,
                    1.78,
                    2.39,
                    2.96,
                    3.43,
                    4.00,
                    4.70,
                    5.44,
                    6.18,
                    7.00,
                    7.79,
                    8.60,
                    9.12,
                    9.66,
                    10.21,
                    10.86,
                    11.40,
                    11.30,
                    11.42,
                    11.09,
                    10.45,
                    9.54,
                    8.71,
                    7.86,
                    7.64,
                    7.51,
                    7.34,
                    7.38,
                    7.51,
                    7.35,
                    6.99,
                    6.28,
                    5.53,
                    5.00,
                    4.65,
                    4.61,
                    4.30,
                    4.14,
                    4.02,
                    3.97,
                    3.31,
                    2.70,
                    2.00,
                    0.92,
                    0.16,
                    0.01,
                ],
            ),
        ],
    )
    def test_parse_valid_fit(
        self,
        request: pytest.FixtureRequest,
        file_path: str,
        selected_dive_idx: int,
        expected_time_data: list[float],
        expected_depth_data: list[float],
    ) -> None:
        """Test parsing a valid FIT file."""
        file_path = str(request.path.parent.joinpath("data", "suunto", file_path))
        fit_parser = SuuntoFitParser(selected_dive_idx=selected_dive_idx)
        fit_parser.parse(file_path)
        assert fit_parser.get_time_data() == expected_time_data
        assert fit_parser.get_depth_data() == expected_depth_data

    def test_parse_invalid_fit(
        self,
        request: pytest.FixtureRequest,
    ) -> None:
        """Test parsing an invalid FIT file."""
        file_path = str(
            request.path.parent.joinpath("data", "suunto", "invalid_file.fit")
        )
        fit_parser = SuuntoFitParser()

        with pytest.raises(DiveLogFitInvalidFitFileError) as e:
            fit_parser.parse(file_path)
        assert str(e.value) == f"Invalid FIT file: {file_path}"

    def test_parse_invalid_fit_no_file_id_mesgs(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test parsing a FIT file with no file_id_mesgs."""

        def mock_decoder_read(
            *_args: Union[str, bool],
            **_kwargs: Union[str, bool],
        ) -> tuple[dict[str, list[Any]], list[Any]]:
            """A mock function for the Decoder.read method."""
            return {"file_id_mesgs": []}, []

        file_path = "mock"

        fit_parser = SuuntoFitParser()
        monkeypatch.setattr(Stream, "from_file", self._mock_stream_from_file)
        monkeypatch.setattr(Decoder, "__init__", self._mock_decoder_init)
        monkeypatch.setattr(Decoder, "read", mock_decoder_read)
        with pytest.raises(DiveLogFitInvalidFitFileError) as e:
            fit_parser.parse(file_path)
        assert (
            str(e.value)
            == f"Invalid FIT file: {file_path}, cannot identify FIT type and manufacturer."
        )

    def test_parse_invalid_fit_wrong_file_type(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test parsing a FIT file with the wrong file type."""

        def mock_decoder_read(
            *_args: Union[str, bool],
            **_kwargs: Union[str, bool],
        ) -> tuple[dict[str, list[Any]], list[Any]]:
            """A mock function for the Decoder.read method."""
            return {"file_id_mesgs": [{"type": "workout"}]}, []

        file_path = "mock"

        fit_parser = SuuntoFitParser()
        monkeypatch.setattr(Stream, "from_file", self._mock_stream_from_file)
        monkeypatch.setattr(Decoder, "__init__", self._mock_decoder_init)
        monkeypatch.setattr(Decoder, "read", mock_decoder_read)
        with pytest.raises(DiveLogFitInvalidFitFileTypeError) as e:
            fit_parser.parse(file_path)
        assert (
            str(e.value)
            == "Invalid FIT file type: You must import 'activity', not 'workout'"
        )

    def test_parse_invalid_fit_wrong_manufacturer(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test parsing a FIT file with the wrong manufacturer."""

        def mock_decoder_read(
            *_args: Union[str, bool],
            **_kwargs: Union[str, bool],
        ) -> tuple[dict[str, list[Any]], list[Any]]:
            """A mock function for the Decoder.read method."""
            return {
                "file_id_mesgs": [{"type": "activity", "manufacturer": "garmin"}]
            }, []

        file_path = "mock"

        fit_parser = SuuntoFitParser()
        monkeypatch.setattr(Stream, "from_file", self._mock_stream_from_file)
        monkeypatch.setattr(Decoder, "__init__", self._mock_decoder_init)
        monkeypatch.setattr(Decoder, "read", mock_decoder_read)
        with pytest.raises(DiveLogFitInvalidFitFileTypeError) as e:
            fit_parser.parse(file_path)
        assert (
            str(e.value)
            == "Invalid FIT file: You must import Suunto Dive Computer data, not 'garmin'"
        )

    def test_empty_record_mesgs(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test parsing a FIT file with empty record_mesgs."""

        def mock_decoder_read(
            *_args: Union[str, bool],
            **_kwargs: Union[str, bool],
        ) -> tuple[dict[str, list[Any]], list[Any]]:
            """A mock function for the Decoder.read method."""
            return {
                "file_id_mesgs": [{"type": "activity", "manufacturer": "suunto"}],
                "record_mesgs": [
                    {"timestamp": 0, "depth": 0.0},
                    {"timestamp": 1, "depth": 3.0},
                    {"timestamp": 2, "depth": 0.0},
                ],
            }, []

        file_path = "mock"

        fit_parser = SuuntoFitParser(selected_dive_idx=0)
        monkeypatch.setattr(Stream, "from_file", self._mock_stream_from_file)
        monkeypatch.setattr(Decoder, "__init__", self._mock_decoder_init)
        monkeypatch.setattr(Decoder, "read", mock_decoder_read)
        with pytest.raises(DiveLogFitDiveNotFoundError) as e:
            fit_parser.parse(file_path)
        assert (
            str(e.value)
            == "Invalid FIT file: does not contain any dive data deeper than 3m."
        )

    def test_file_not_found(self) -> None:
        """Test parsing a FIT file that does not exist."""
        file_path = "invalid_file_path"

        fit_parser = SuuntoFitParser()
        with pytest.raises(DiveLogFileNotFoundError) as e:
            fit_parser.parse(file_path)
        assert str(e.value) == f"File not found: {file_path}"

    def test_select_dive_single_dive(self) -> None:
        """Test selecting a dive from a FIT file with a single dive."""
        dive_summary = [
            {
                "raw_data": [],
                "start_time": 1054149000,
                "end_time": 1054149060,
                "max_depth": 30.0,
                "bottom_time": 60,
            }
        ]
        fit_parser = SuuntoFitParser()
        assert fit_parser.select_dive(dive_summary) == 0

    def test_convert_time(self) -> None:
        """Test converting time from a FIT file to a human-readable format."""
        fit_epoch_time = 1098021928  # 2024-10-16T14:05:28.000Z
        fit_parser = SuuntoFitParser()
        assert (
            fit_parser.convert_fit_epoch_to_datetime(fit_epoch_time)
            == "2024-10-16 14:05:28 (GMT)"
        )

    @patch("builtins.input", return_value="2")
    def test_select_dive_multiple_dives(
        self,
        mock_input: Mock,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Test selecting a dive from a FIT file with multiple dives.

        Note:
            This test uses the mock_input fixture to simulate user input.

        Expected Output:
            Multiple dives found in the FIT file. Please select a dive to import:
            [1]: Dive 1: Start Time: 2023-05-27 19:10:00 (GMT), Max Depth: 30.0m, Bottom Time: 60.0s
            [2]: Dive 2: Start Time: 2023-05-27 19:11:00 (GMT), Max Depth: 20.0m, Bottom Time: 59.0s
        """
        dive_summary = [
            {
                "raw_data": [],
                "start_time": 1054149000,
                "end_time": 1054149060,
                "max_depth": 30.0,
                "bottom_time": 60,
            },
            {
                "raw_data": [],
                "start_time": 1054149060,
                "end_time": 1054149119,
                "max_depth": 20.0,
                "bottom_time": 59,
            },
        ]
        fit_parser = SuuntoFitParser()
        user_select_idx = fit_parser.select_dive(dive_summary)
        expected_idx = int(mock_input.return_value) - 1
        assert user_select_idx == expected_idx

        captured = capsys.readouterr()
        assert "Multiple dives found in the FIT file" in captured.out
        assert (
            "[1]: Dive 1: Start Time: 2023-05-27 19:10:00 (GMT), "
            "Max Depth: 30.0m, Bottom Time: 60.0s" in captured.out
        )
        assert (
            "[2]: Dive 2: Start Time: 2023-05-27 19:11:00 (GMT), "
            "Max Depth: 20.0m, Bottom Time: 59.0s" in captured.out
        )
        assert mock_input.call_count == 1

    @patch("builtins.input", return_value="xxx")
    def test_select_invalid_dive_non_number(
        self,
        mock_input: Mock,
    ) -> None:
        """Test selecting an invalid dive index."""
        dive_summary = [
            {
                "raw_data": [],
                "start_time": 1054149000,
                "end_time": 1054149060,
                "max_depth": 30.0,
                "bottom_time": 60,
            },
            {
                "raw_data": [],
                "start_time": 1054149060,
                "end_time": 1054149119,
                "max_depth": 20.0,
                "bottom_time": 59,
            },
        ]
        fit_parser = SuuntoFitParser()
        with pytest.raises(DiveLogFitDiveNotFoundError) as e:
            fit_parser.select_dive(dive_summary)
        assert (
            str(e.value)
            == f"Invalid Dive: Please enter a number between 1 and {len(dive_summary)}"
        )
        assert mock_input.call_count == 1

    @patch("builtins.input", return_value="3")
    def test_select_invalid_dive_idx(
        self, mock_input: Mock, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test parsing a FIT file with an invalid dive index."""

        def mock_decoder_read(
            *_args: Union[str, bool],
            **_kwargs: Union[str, bool],
        ) -> tuple[dict[str, list[Any]], list[Any]]:
            """A mock function for the Decoder.read method."""
            return {
                "file_id_mesgs": [{"type": "activity", "manufacturer": "suunto"}],
                "record_mesgs": [
                    {"timestamp": 0, "depth": 0.0},
                    {"timestamp": 1, "depth": 1.0},
                    {"timestamp": 2, "depth": 2.0},
                    {"timestamp": 3, "depth": 3.0},
                    {"timestamp": 4, "depth": 4.0},
                    {"timestamp": 5, "depth": 3.0},
                    {"timestamp": 6, "depth": 1.0},
                    {"timestamp": 7, "depth": 0.0},
                    {"timestamp": 8, "depth": 1.0},
                    {"timestamp": 9, "depth": 2.0},
                    {"timestamp": 10, "depth": 3.0},
                    {"timestamp": 11, "depth": 4.0},
                    {"timestamp": 12, "depth": 3.0},
                    {"timestamp": 13, "depth": 2.0},
                    {"timestamp": 14, "depth": 1.0},
                    {"timestamp": 15, "depth": 0.0},
                ],
            }, []

        file_path = "mock"

        fit_parser = SuuntoFitParser()
        monkeypatch.setattr(Stream, "from_file", self._mock_stream_from_file)
        monkeypatch.setattr(Decoder, "__init__", self._mock_decoder_init)
        monkeypatch.setattr(Decoder, "read", mock_decoder_read)

        with pytest.raises(DiveLogFitDiveNotFoundError) as e:
            fit_parser.parse(file_path)
        assert str(e.value) == "Invalid Dive: Please enter a number between 1 and 2"
        assert mock_input.call_count == 1

    @pytest.mark.parametrize("depth_mode", ["raw", "zero-based"])
    @patch("depthviz.parsers.suunto.fit_parser.SuuntoFitParser.depth_mode_execute")
    def test_parse_valid_fit_depth_mode_exec(
        self,
        mock_depth_mode_execute: Mock,
        depth_mode: str,
        request: pytest.FixtureRequest,
    ) -> None:
        """Test parsing a valid FIT file with depth mode execution."""
        file_path = str(
            request.path.parent.joinpath(
                "data",
                "suunto",
                "FreeDiving_2024-10-16T16_33_30.fit",
            )
        )
        parser = SuuntoFitParser(depth_mode=depth_mode, selected_dive_idx=0)
        parser.parse(file_path)
        mock_depth_mode_execute.assert_called_once()

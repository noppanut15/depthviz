# Copyright (c) 2024 - 2025 Noppanut Ploywong (@noppanut15) <noppanut.connect@gmail.com>
# Apache License 2.0 (see LICENSE file or http://www.apache.org/licenses/LICENSE-2.0)


"""Unit tests for the main CLI."""

import sys
import argparse
import pathlib
from typing import Any
from unittest import mock
import pytest
from depthviz.main import DepthvizApplication, run
from depthviz.parsers.generic.generic_divelog_parser import DiveLogParser
from depthviz.video.video_creator import (
    OverlayVideoCreatorError,
    DEFAULT_FONT,
    DEFAULT_STROKE_WIDTH,
)
from depthviz.video.time import TimeReportVideoCreatorError


# Mock the DEFAULT_VIDEO_SIZE constant to lower the resolution for faster tests.
@mock.patch("depthviz.main.DEFAULT_VIDEO_SIZE", (640, 360))
class TestMainCLI:
    """Test suite for the main CLI."""

    def _mock_depthviz_create_depth_video(
        self,
        output_path: str,
        *_args: Any,
        **_kwargs: Any,
    ) -> None:
        """Mock the DepthvizApplication create_depth_video method."""
        print(f"Depth video successfully created: {output_path}")

    def test_main(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test the main function."""
        with pytest.raises(SystemExit) as excinfo:
            app = DepthvizApplication()
            app.main()
        assert excinfo.value.code == 2
        captured = capsys.readouterr()
        assert "usage: " in captured.err
        assert (
            "error: the following arguments are required: -i/--input, -s/--source, -o/--output"
            in captured.err
        )

    def test_main_with_args(
        self,
        capsys: pytest.CaptureFixture[str],
        tmp_path: pathlib.Path,
        request: pytest.FixtureRequest,
    ) -> None:
        """Test the main function with arguments."""
        input_path = (
            request.path.parent / "data" / "apnealizer" / "valid_depth_data_trimmed.csv"
        )
        output_path = tmp_path / "test_main_with_args.mp4"
        sys.argv = [
            "main",
            "-i",
            str(input_path.as_posix()),
            "-s",
            "apnealizer",
            "-o",
            str(output_path.as_posix()),
        ]
        app = DepthvizApplication()
        app.main()
        captured = capsys.readouterr()
        assert (
            f"Depth video successfully created: {output_path.as_posix()}"
            in captured.out
        )

    def test_main_with_invalid_csv(
        self,
        capsys: pytest.CaptureFixture[str],
        tmp_path: pathlib.Path,
        request: pytest.FixtureRequest,
    ) -> None:
        """Test the main function with an invalid CSV."""
        input_path = (
            request.path.parent / "data" / "apnealizer" / "invalid_data_x_header.csv"
        )
        output_path = tmp_path / "test_main_with_invalid_csv.mp4"
        sys.argv = [
            "main",
            "-i",
            str(input_path.as_posix()),
            "-s",
            "apnealizer",
            "-o",
            str(output_path.as_posix()),
        ]

        app = DepthvizApplication()
        app.main()
        captured = capsys.readouterr()
        assert "Invalid CSV: Target header not found" in captured.out

    def test_main_without_args(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test the main function without arguments."""
        sys.argv = ["main"]
        app = DepthvizApplication()
        app.main()
        captured = capsys.readouterr()
        assert "usage: " in captured.err
        assert (
            "[-h] -i INPUT -s {apnealizer,shearwater,garmin,suunto,manual"
            in captured.err
        )

    def test_main_with_invalid_output_video_filetype(
        self,
        capsys: pytest.CaptureFixture[str],
        tmp_path: pathlib.Path,
        request: pytest.FixtureRequest,
    ) -> None:
        """Test the main function with an invalid output video file type."""
        input_path = (
            request.path.parent / "data" / "apnealizer" / "valid_depth_data_trimmed.csv"
        )
        output_path = tmp_path / "invalid.mp3"
        sys.argv = [
            "main",
            "-i",
            str(input_path.as_posix()),
            "-s",
            "apnealizer",
            "-o",
            str(output_path.as_posix()),
        ]
        app = DepthvizApplication()
        app.main()
        captured = capsys.readouterr()
        assert (
            "Invalid output file extension. Please provide a .mp4 file." in captured.out
        )

    def test_main_with_invalid_source(
        self,
        capsys: pytest.CaptureFixture[str],
        tmp_path: pathlib.Path,
        request: pytest.FixtureRequest,
    ) -> None:
        """Test the main function with an invalid source."""
        input_path = (
            request.path.parent / "data" / "apnealizer" / "valid_depth_data_trimmed.csv"
        )
        output_path = tmp_path / "test_main_with_args.mp4"
        sys.argv = [
            "main",
            "-i",
            str(input_path.as_posix()),
            "-s",
            "XXXXXXXX",
            "-o",
            str(output_path.as_posix()),
        ]
        with pytest.raises(SystemExit):
            app = DepthvizApplication()
            app.main()
        captured = capsys.readouterr()
        assert "error: argument -s/--source: invalid choice: 'XXXXXXXX'" in captured.err

    def test_main_with_invalid_source_direct_call_function(
        self, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Test the main function with an invalid source using direct function call."""
        mock_source = "random-stuff"

        def mock_parse_args(*_args: Any, **_kwargs: Any) -> argparse.Namespace:
            """Mock the parse_args function to inject nonexistent source."""
            return argparse.Namespace(
                input="test.csv",
                source=mock_source,
                output="test.mp4",
                decimal_places=0,
            )

        monkeypatch.setattr(argparse.ArgumentParser, "parse_args", mock_parse_args)
        app = DepthvizApplication()
        app.main()
        captured = capsys.readouterr()
        assert f"Source {mock_source} not supported." in captured.out

    def test_cli_run(self) -> None:
        """Test the entrypoint function."""
        sys.argv = ["main"]
        ret_code = run()
        assert ret_code == 1

    def test_main_with_args_shearwater(
        self,
        capsys: pytest.CaptureFixture[str],
        tmp_path: pathlib.Path,
        request: pytest.FixtureRequest,
    ) -> None:
        """Test the main function with arguments for Shearwater."""
        input_path = (
            request.path.parent / "data" / "shearwater" / "valid_depth_data_trimmed.xml"
        )
        output_path = tmp_path / "test_main_with_args_shearwater.mp4"
        sys.argv = [
            "main",
            "-i",
            str(input_path.as_posix()),
            "-s",
            "shearwater",
            "-o",
            str(output_path.as_posix()),
        ]
        app = DepthvizApplication()
        app.main()
        captured = capsys.readouterr()
        assert (
            f"Depth video successfully created: {output_path.as_posix()}"
            in captured.out
        )

    def test_main_with_args_manual_mode(
        self,
        capsys: pytest.CaptureFixture[str],
        tmp_path: pathlib.Path,
        request: pytest.FixtureRequest,
    ) -> None:
        """Test the main function with arguments for manual mode."""
        input_path = (
            request.path.parent / "data" / "manual" / "valid_depth_data_trimmed.csv"
        )
        output_path = tmp_path / "test_main_with_args_manual_mode.mp4"
        sys.argv = [
            "main",
            "-i",
            str(input_path.as_posix()),
            "-s",
            "manual",
            "-o",
            str(output_path.as_posix()),
        ]
        app = DepthvizApplication()
        app.main()
        captured = capsys.readouterr()
        assert (
            f"Depth video successfully created: {output_path.as_posix()}"
            in captured.out
        )

    def test_main_with_args_no_minus_option(
        self,
        capsys: pytest.CaptureFixture[str],
        tmp_path: pathlib.Path,
        request: pytest.FixtureRequest,
    ) -> None:
        """Test the main function with arguments for manual mode with no minus option."""
        input_path = (
            request.path.parent / "data" / "manual" / "valid_depth_data_trimmed.csv"
        )
        output_path = tmp_path / "test_main_with_args_no_minus_option.mp4"
        sys.argv = [
            "main",
            "-i",
            str(input_path.as_posix()),
            "-s",
            "manual",
            "-o",
            str(output_path.as_posix()),
            "--no-minus",
        ]
        app = DepthvizApplication()
        app.main()
        captured = capsys.readouterr()
        assert (
            f"Depth video successfully created: {output_path.as_posix()}"
            in captured.out
        )

    @mock.patch("depthviz.main.DepthvizApplication.create_depth_video")
    @mock.patch("depthviz.parsers.garmin.fit_parser.GarminFitParser.parse")
    def test_main_with_args_garmin(
        self,
        mock_parse: mock.Mock,
        mock_create_depth_video: mock.Mock,
        capsys: pytest.CaptureFixture[str],
        tmp_path: pathlib.Path,
    ) -> None:
        """Test the main function with arguments for Garmin."""
        input_path = tmp_path / "mock.fit"
        output_path = tmp_path / "test_main_with_args_garmin.mp4"
        sys.argv = [
            "main",
            "-i",
            str(input_path.as_posix()),
            "-s",
            "garmin",
            "-o",
            str(output_path.as_posix()),
        ]
        app = DepthvizApplication()

        # Mock the Garmin FIT parser parse method.
        mock_parse.side_effect = mock.Mock()
        # Mock the create_depth_video method.
        mock_create_depth_video.side_effect = self._mock_depthviz_create_depth_video
        app.main()
        captured = capsys.readouterr()

        assert (
            f"Depth video successfully created: {output_path.as_posix()}"
            in captured.out
        )
        mock_parse.assert_called_once_with(file_path=input_path.as_posix())
        mock_create_depth_video.assert_called_once_with(
            divelog_parser=mock.ANY,
            output_path=output_path.as_posix(),
            decimal_places=0,
            no_minus=False,
            font=DEFAULT_FONT,
            bg_color="black",
            stroke_width=DEFAULT_STROKE_WIDTH,
        )

    @pytest.mark.parametrize(
        "decimal_places, output, expected_is_valid, expected_output_message",
        [
            (0, "test.mp4", True, ""),
            (1, "test.mp4", True, ""),
            (2, "test.mp4", True, ""),
            (
                3,
                "test.mp4",
                False,
                "Invalid value for decimal places. Valid values: 0, 1, 2.",
            ),
            (
                -1,
                "test.mp4",
                False,
                "Invalid value for decimal places. Valid values: 0, 1, 2.",
            ),
            (
                0,
                "test.mp3",
                False,
                "Invalid output file extension. Please provide a .mp4 file.",
            ),
            (
                0,
                "xx",
                False,
                "Invalid output file extension. Please provide a .mp4 file.",
            ),
        ],
    )
    def test_is_user_input_valid(
        self,
        decimal_places: int,
        output: str,
        expected_is_valid: bool,
        expected_output_message: str,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Test the is_user_input_valid method."""
        app = DepthvizApplication()
        args = argparse.Namespace(decimal_places=decimal_places, output=output)
        is_valid = app.is_user_input_valid(args)
        output_message, _ = capsys.readouterr()
        assert is_valid is expected_is_valid
        assert output_message.strip() == expected_output_message

    @mock.patch("depthviz.main.DepthReportVideoCreator.save")
    @mock.patch("depthviz.main.DepthReportVideoCreator.render_depth_report_video")
    @mock.patch("depthviz.main.DepthReportVideoCreator")
    def test_create_depth_video_failure(
        self,
        mock_depth_report_video_creator: mock.Mock,
        mock_render_depth_report_video: mock.Mock,
        mock_save: mock.Mock,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Test the create_depth_video method for failure in video creation."""
        # Create an instance of the main application.
        app = DepthvizApplication()

        # Mock the DiveLogParser class and its methods.
        divelog_parser = mock.Mock(spec=DiveLogParser)
        divelog_parser.get_time_data = mock.Mock(return_value=[0, 1, 2, 3])
        divelog_parser.get_depth_data = mock.Mock(return_value=[0.0, 1.5, 2.0])

        # Mock the DepthReportVideoCreator class and its methods.
        mock_depth_report_video_creator.return_value = mock_depth_report_video_creator
        mock_render_depth_report_video.side_effect = OverlayVideoCreatorError(
            "Error rendering video"
        )

        # Call the create_depth_video method with the mocked objects.
        output_path = "test.mp4"
        decimal_places = 2
        no_minus = False

        ret_code = app.create_depth_video(
            divelog_parser=divelog_parser,
            output_path=output_path,
            decimal_places=decimal_places,
            no_minus=no_minus,
            font=DEFAULT_FONT,
        )

        # Check the return code and the captured output.
        assert ret_code == 1
        captured = capsys.readouterr()
        assert "Error rendering video" in captured.out

        # Check the method calls.
        divelog_parser.get_time_data.assert_called_once()
        divelog_parser.get_depth_data.assert_called_once()
        mock_render_depth_report_video.assert_called_once_with(
            time_data=[0, 1, 2, 3],
            depth_data=[0.0, 1.5, 2.0],
            decimal_places=decimal_places,
            minus_sign=True,
        )
        mock_save.assert_not_called()

    @mock.patch("depthviz.main.DepthvizApplication.create_depth_video")
    @mock.patch("depthviz.parsers.suunto.fit_parser.SuuntoFitParser.parse")
    def test_main_with_args_suunto(
        self,
        mock_parse: mock.Mock,
        mock_create_depth_video: mock.Mock,
        capsys: pytest.CaptureFixture[str],
        tmp_path: pathlib.Path,
    ) -> None:
        """Test the main function with arguments for Suunto."""
        input_path = tmp_path / "mock.fit"
        output_path = tmp_path / "test_main_with_args_suunto.mp4"
        sys.argv = [
            "main",
            "-i",
            str(input_path.as_posix()),
            "-s",
            "suunto",
            "-o",
            str(output_path.as_posix()),
        ]
        app = DepthvizApplication()

        # Mock the Suunto FIT parser parse method.
        mock_parse.side_effect = mock.Mock()
        # Mock the create_depth_video method.
        mock_create_depth_video.side_effect = self._mock_depthviz_create_depth_video
        app.main()
        captured = capsys.readouterr()

        assert (
            f"Depth video successfully created: {output_path.as_posix()}"
            in captured.out
        )
        mock_parse.assert_called_once_with(file_path=input_path.as_posix())
        mock_create_depth_video.assert_called_once_with(
            divelog_parser=mock.ANY,
            output_path=output_path.as_posix(),
            decimal_places=0,
            no_minus=False,
            font=DEFAULT_FONT,
            bg_color="black",
            stroke_width=DEFAULT_STROKE_WIDTH,
        )

    def test_main_with_args_font(
        self,
        capsys: pytest.CaptureFixture[str],
        tmp_path: pathlib.Path,
        request: pytest.FixtureRequest,
    ) -> None:
        """Test the main function with arguments for font."""
        input_path = (
            request.path.parent / "data" / "apnealizer" / "valid_depth_data_trimmed.csv"
        )
        output_path = tmp_path / "test_main_with_args_font.mp4"
        font_path = (
            request.path.parent / "data" / "assets" / "fonts" / "OpenSans-Regular.ttf"
        )
        sys.argv = [
            "main",
            "-i",
            str(input_path.as_posix()),
            "-s",
            "apnealizer",
            "-o",
            str(output_path.as_posix()),
            "--font",
            str(font_path.as_posix()),
        ]
        app = DepthvizApplication()
        app.main()
        captured = capsys.readouterr()
        assert (
            f"Depth video successfully created: {output_path.as_posix()}"
            in captured.out
        )

    def test_main_with_args_bg_color(
        self,
        capsys: pytest.CaptureFixture[str],
        tmp_path: pathlib.Path,
        request: pytest.FixtureRequest,
    ) -> None:
        """Test the main function with arguments for background color."""
        input_path = (
            request.path.parent / "data" / "apnealizer" / "valid_depth_data_trimmed.csv"
        )
        output_path = tmp_path / "test_main_with_args_bg_color.mp4"
        sys.argv = [
            "main",
            "-i",
            str(input_path.as_posix()),
            "-s",
            "apnealizer",
            "-o",
            str(output_path.as_posix()),
            "--bg-color",
            "green",
        ]
        app = DepthvizApplication()
        app.main()
        captured = capsys.readouterr()
        assert (
            f"Depth video successfully created: {output_path.as_posix()}"
            in captured.out
        )

    def test_main_with_args_stroke_width(
        self,
        capsys: pytest.CaptureFixture[str],
        tmp_path: pathlib.Path,
        request: pytest.FixtureRequest,
    ) -> None:
        """Test the main function with arguments for stroke width."""
        input_path = (
            request.path.parent / "data" / "apnealizer" / "valid_depth_data_trimmed.csv"
        )
        output_path = tmp_path / "test_main_with_args_stroke_width.mp4"
        sys.argv = [
            "main",
            "-i",
            str(input_path.as_posix()),
            "-s",
            "apnealizer",
            "-o",
            str(output_path.as_posix()),
            "--bg-color",
            "green",  # This makes the stroke color visible for testing
            "--stroke-width",
            "12",
        ]
        app = DepthvizApplication()
        app.main()
        captured = capsys.readouterr()
        assert (
            f"Depth video successfully created: {output_path.as_posix()}"
            in captured.out
        )

    def test_main_with_args_time_video(
        self,
        capsys: pytest.CaptureFixture[str],
        tmp_path: pathlib.Path,
        request: pytest.FixtureRequest,
    ) -> None:
        """Test the main function with arguments for time overlay video."""
        input_path = (
            request.path.parent / "data" / "apnealizer" / "valid_depth_data_trimmed.csv"
        )
        output_path = tmp_path / "FIM36m.mp4"
        time_output_path = tmp_path / "FIM36m_time.mp4"
        sys.argv = [
            "main",
            "-i",
            str(input_path.as_posix()),
            "-s",
            "apnealizer",
            "-o",
            str(output_path.as_posix()),
            "--time",
        ]
        app = DepthvizApplication()
        app.main()
        captured = capsys.readouterr()
        assert (
            f"Time video successfully created: {time_output_path.as_posix()}"
            in captured.out
        )
        assert time_output_path.exists()

    @mock.patch("depthviz.main.TimeReportVideoCreator.save")
    @mock.patch("depthviz.main.TimeReportVideoCreator.render_time_report_video")
    @mock.patch("depthviz.main.TimeReportVideoCreator")
    def test_create_time_video_failure(
        self,
        mock_time_report_video_creator: mock.Mock,
        mock_render_time_report_video: mock.Mock,
        mock_save: mock.Mock,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Test the create_time_video method for failure in video creation."""
        # Create an instance of the main application.
        app = DepthvizApplication()

        # Mock the DiveLogParser class and its methods.
        divelog_parser = mock.Mock(spec=DiveLogParser)
        divelog_parser.get_time_data = mock.Mock(return_value=[0, -1, 2, 3])

        # Mock the TimeReportVideoCreator class and its methods.
        mock_time_report_video_creator.return_value = mock_time_report_video_creator
        mock_render_time_report_video.side_effect = TimeReportVideoCreatorError(
            "The time data contains negative values."
        )

        # Call the create_time_video method with the mocked objects.
        output_path = "test.mp4"

        ret_code = app.create_time_video(
            divelog_parser=divelog_parser,
            output_path=output_path,
            font=DEFAULT_FONT,
        )

        # Check the return code and the captured output.
        assert ret_code == 1
        captured = capsys.readouterr()
        assert "The time data contains negative values." in captured.out

        # Check the exception type whether it is compatible with the expected exception.
        assert isinstance(
            mock_render_time_report_video.side_effect, OverlayVideoCreatorError
        )

        # Check the method calls.
        divelog_parser.get_time_data.assert_called_once()
        mock_render_time_report_video.assert_called_once_with(
            time_data=[0, -1, 2, 3],
        )
        mock_save.assert_not_called()

    # def test_main_with_args_depth_mode(
    #     self,
    #     capsys: pytest.CaptureFixture[str],
    #     tmp_path: pathlib.Path,
    #     request: pytest.FixtureRequest,
    # ) -> None:
    #     """
    #     Test the main function with arguments for depth-mode as zero-based
    #     to force the depth to start from zero and end with zero.
    #     """

    #     input_path = (
    #         request.path.parent / "data" / "apnealizer" / "valid_depth_data_trimmed.csv"
    #     )
    #     output_path = tmp_path / "test_main_with_args.mp4"
    #     sys.argv = [
    #         "main",
    #         "-i",
    #         str(input_path.as_posix()),
    #         "-s",
    #         "apnealizer",
    #         "-o",
    #         str(output_path.as_posix()),
    #         "--depth-mode",
    #         "zero-based",
    #     ]
    #     app = DepthvizApplication()
    #     app.main()
    #     captured = capsys.readouterr()
    #     assert (
    #         f"Depth video successfully created: {output_path.as_posix()}"
    #         in captured.out
    #     )

"""
Unit tests for the main CLI.
"""

import sys
import argparse
import pathlib
import pytest
from depthviz.main import DepthvizApplication, run


class TestMainCLI:
    """
    Test suite for the main CLI.
    """

    def test_main(self, capsys: pytest.CaptureFixture[str]) -> None:
        """
        Test the main function.
        """
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
        """
        Test the main function with arguments.
        """

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
        assert f"Video successfully created: {output_path.as_posix()}" in captured.out

    def test_main_with_invalid_csv(
        self,
        capsys: pytest.CaptureFixture[str],
        tmp_path: pathlib.Path,
        request: pytest.FixtureRequest,
    ) -> None:
        """
        Test the main function with an invalid CSV.
        """

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
        """
        Test the main function without arguments.
        """
        sys.argv = ["main"]
        app = DepthvizApplication()
        app.main()
        captured = capsys.readouterr()
        assert "usage: " in captured.err
        assert "[-h] -i INPUT -s {apnealizer,shearwater} -o OUTPUT [-v]" in captured.err

    def test_main_with_invalid_output_video_filetype(
        self,
        capsys: pytest.CaptureFixture[str],
        tmp_path: pathlib.Path,
        request: pytest.FixtureRequest,
    ) -> None:
        """
        Test the main function with an invalid output video file type.
        """

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
        assert "Invalid file format" in captured.out

    def test_main_with_invalid_source(
        self,
        capsys: pytest.CaptureFixture[str],
        tmp_path: pathlib.Path,
        request: pytest.FixtureRequest,
    ) -> None:
        """
        Test the main function with an invalid source.
        """
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
        """
        Test the main function with an invalid source using direct function call.
        """
        mock_source = "random-stuff"

        def mock_parse_args(  # type: ignore
            *args,  # pylint: disable=unused-argument
        ) -> argparse.Namespace:
            return argparse.Namespace(
                input="test.csv", source=mock_source, output="test.mp4"
            )

        monkeypatch.setattr(argparse.ArgumentParser, "parse_args", mock_parse_args)
        app = DepthvizApplication()
        app.main()
        captured = capsys.readouterr()
        assert f"Source {mock_source} not supported." in captured.out

    def test_cli_run(self) -> None:
        """
        Test the entrypoint function.
        """
        sys.argv = ["main"]
        ret_code = run()
        assert ret_code == 1

    def test_main_with_args_shearwater(
        self,
        capsys: pytest.CaptureFixture[str],
        tmp_path: pathlib.Path,
        request: pytest.FixtureRequest,
    ) -> None:
        """
        Test the main function with arguments for Shearwater.
        """

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
        assert f"Video successfully created: {output_path.as_posix()}" in captured.out

"""
Unit tests for the main CLI.
"""

import sys
import pathlib
import pytest
from depthviz.main_cli import main


class TestMainCLI:
    """
    Test suite for the main CLI.
    """

    def test_main(self, capsys: pytest.CaptureFixture[str]) -> None:
        """
        Test the main function.
        """
        with pytest.raises(SystemExit) as excinfo:
            main()
        assert excinfo.value.code == 2
        captured = capsys.readouterr()
        assert "usage: " in captured.err
        assert (
            "error: the following arguments are required: -i/--input, -s/--sample-rate, -o/--output"
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

        input_path = request.path.parent / "data" / "valid_depth_data_trimmed.csv"
        output_path = tmp_path / "test_main_with_args.mp4"
        sys.argv = [
            "main",
            "-i",
            str(input_path.as_posix()),
            "-s",
            "0.25",
            "-o",
            str(output_path.as_posix()),
        ]
        main()
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

        input_path = request.path.parent / "data" / "invalid_data_x_header.csv"
        output_path = tmp_path / "test_main_with_invalid_csv.mp4"
        sys.argv = [
            "main",
            "-i",
            str(input_path.as_posix()),
            "-s",
            "0.25",
            "-o",
            str(output_path.as_posix()),
        ]

        main()
        captured = capsys.readouterr()
        assert "Invalid CSV: Target header not found" in captured.out

    def test_main_without_args(self, capsys: pytest.CaptureFixture[str]) -> None:
        """
        Test the main function without arguments.
        """
        sys.argv = ["main"]
        main()
        captured = capsys.readouterr()
        assert "usage: " in captured.err
        assert "[-h] -i INPUT -s SAMPLE_RATE -o OUTPUT" in captured.err

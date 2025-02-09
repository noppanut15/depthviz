# Copyright (c) 2024 - 2025 Noppanut Ploywong (@noppanut15) <noppanut.connect@gmail.com>
# Apache License 2.0 (see LICENSE file or http://www.apache.org/licenses/LICENSE-2.0)


"""Unit tests for the depth module."""

import os.path
import pathlib
from typing import Any
import pytest
from depthviz.video.video_creator import (
    VideoNotRenderError,
    VideoFormatError,
    OverlayVideoCreatorError,
)
from depthviz.video.depth import DepthReportVideoCreator, DepthReportVideoCreatorError


class TestDepthReportVideoCreator:
    """Test the DepthReportVideoCreator class."""

    def test_render_depth_report_video(self) -> None:
        """Test the render_depth_report_video method."""
        # Create a DepthReportVideoCreator instance
        depth_report_video_creator = DepthReportVideoCreator()

        # Create a depth report video
        time_data = [
            0.25,
            0.5,
            0.75,
            1.0,
            1.25,
            1.5,
            1.75,
            2.0,
            2.25,
            2.5,
            2.75,
            3.0,
        ]
        depth_data = [0.1, 0.2, 0.3, 0.4, 0.5, 0.9, 1.3, 1.7, 2.1, 2.5, 2.9, 3.3]
        video = depth_report_video_creator.render_depth_report_video(
            time_data=time_data, depth_data=depth_data
        )

        # Check the video is not None
        assert video is not None

        # Check the duration of the video (seconds)
        assert video.duration == pytest.approx(3.76)

        # Check the number of clips in the video
        assert len(video.clips) == 4

        # Check the text of each clip in the video
        video_clip_texts = [video.clips[i].text for i in range(len(video.clips))]
        assert video_clip_texts == ["0m", "-1m", "-2m", "-3m"]

    def test_save_specific_dir(self, tmp_path: pathlib.Path) -> None:
        """Test the save method in a specific directory."""
        # Create a DepthReportVideoCreator instance
        depth_report_video_creator = DepthReportVideoCreator(fps=1)

        # Create a depth report video
        time_data = [1.0, 2.0, 3.0]
        depth_data = [0.1, 0.2, 0.3]
        video = depth_report_video_creator.render_depth_report_video(
            time_data=time_data, depth_data=depth_data
        )

        # Save the video to a file in directory tmp_path
        path = tmp_path / "test_depth_report_video.mp4"
        depth_report_video_creator.save(video=video, path=path.as_posix())

        assert path.exists()
        assert path.stat().st_size > 0
        assert path.suffix == ".mp4"

    def test_save_current_dir(self) -> None:
        """Test the save method in the current directory."""
        # Create a DepthReportVideoCreator instance
        depth_report_video_creator = DepthReportVideoCreator(fps=4)

        # Create a depth report video
        time_data = [0.25, 0.5, 0.75, 1.0]
        depth_data = [0.0, 1.0, 2.0, 3.0]
        video = depth_report_video_creator.render_depth_report_video(
            time_data=time_data, depth_data=depth_data
        )

        # Save the video to a file in the current directory
        path = ".depth_overlay.mp4"
        depth_report_video_creator.save(video=video, path=path)

        assert os.path.exists(".depth_overlay.mp4")

    def test_save_to_nonexistent_path(self, tmp_path: pathlib.Path) -> None:
        """Test the save method with a nonexistent path."""
        # Create a DepthReportVideoCreator instance
        depth_report_video_creator = DepthReportVideoCreator(fps=1)

        # Create a depth report video
        time_data = [1.0, 2.0, 3.0]
        depth_data = [0.1, 0.2, 0.3]
        video = depth_report_video_creator.render_depth_report_video(
            time_data=time_data, depth_data=depth_data
        )

        # Save the video to a nonexistent path
        wrong_path = tmp_path / "non_existent_dir" / "test_depth_report_video.mp4"
        with pytest.raises(FileNotFoundError) as e:
            depth_report_video_creator.save(video=video, path=wrong_path.as_posix())
        assert str(e.value) == f"Parent directory does not exist: {wrong_path.parent}"

    def test_save_without_file_name(self, tmp_path: pathlib.Path) -> None:
        """Test the save method without a file name."""
        # Create a DepthReportVideoCreator instance
        depth_report_video_creator = DepthReportVideoCreator(fps=1)

        # Create a depth report video
        time_data = [1.0, 2.0, 3.0]
        depth_data = [0.1, 0.2, 0.3]
        video = depth_report_video_creator.render_depth_report_video(
            time_data=time_data, depth_data=depth_data
        )

        # Save the video to a file without a file name
        wrong_path = tmp_path
        with pytest.raises(NameError) as e:
            depth_report_video_creator.save(video=video, path=wrong_path.as_posix())
        assert (
            str(e.value)
            == f"{wrong_path} is a directory, please add a file name to the path. \
                        (e.g., path/to/mydepth_video.mp4)"
        )

    def test_save_video_not_rendered(self, tmp_path: pathlib.Path) -> None:
        """Test the save method with a video not rendered."""
        # Create a DepthReportVideoCreator instance
        depth_report_video_creator = DepthReportVideoCreator(fps=1)
        video = None
        # Save the video to a file without rendering it
        path = tmp_path / "test_depth_report_video.mp4"
        with pytest.raises(VideoNotRenderError) as e:
            depth_report_video_creator.save(video=video, path=path.as_posix())
        assert str(e.value) == "Cannot save video because it has not been rendered yet."

    def test_save_video_wrong_format(self, tmp_path: pathlib.Path) -> None:
        """Test the save method with a wrong file format."""
        # Create a DepthReportVideoCreator instance
        depth_report_video_creator = DepthReportVideoCreator(fps=1)

        # Create a depth report video
        time_data = [1.0, 2.0, 3.0]
        depth_data = [0.1, 0.2, 0.3]
        video = depth_report_video_creator.render_depth_report_video(
            time_data=time_data, depth_data=depth_data
        )

        # Save the video to a file with a wrong file format
        wrong_path = tmp_path / "test_depth_report_video.avi"
        with pytest.raises(VideoFormatError) as e:
            depth_report_video_creator.save(video=video, path=wrong_path.as_posix())
        assert str(e.value) == "Invalid file format: The file format must be .mp4"

    def test_render_depth_video_with_invalid_input(self) -> None:
        """Test the render_depth_report_video method with invalid input.

        Note:
            Test with different length between time and depth data
        """
        # Create a DepthReportVideoCreator instance
        depth_report_video_creator = DepthReportVideoCreator(fps=1)

        # Create a depth report video with invalid input
        time_data = [0.1, 0.2, 0.3]
        depth_data = [0.1, 0.2]
        with pytest.raises(DepthReportVideoCreatorError) as e:
            _ = depth_report_video_creator.render_depth_report_video(
                time_data=time_data, depth_data=depth_data
            )
        assert (
            str(e.value)
            == "Interpolation Error; (Error: Times and depths lists must have the same length.)"
        )

    @pytest.mark.parametrize(
        "decimal_places, expected_texts",
        [
            (0, ["0m", "-1m", "-2m", "-3343m"]),
            (1, ["0.0m", "-0.1m", "-0.3m", "-1.3m", "-1.5m", "-3343.3m"]),
            (2, ["0.00m", "-0.13m", "-0.27m", "-1.34m", "-1.54m", "-3343.32m"]),
        ],
    )
    def test_render_depth_video_with_decimal_places(
        self, decimal_places: int, expected_texts: list[str]
    ) -> None:
        """Test the render_depth_report_video method with decimal places."""
        # Create a DepthReportVideoCreator instance
        depth_report_video_creator = DepthReportVideoCreator(fps=1)

        # Create a depth report video with decimal places
        time_data = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
        depth_data = [0.001, 0.13344, 0.26667, 1.345, 1.54444, 3343.32343]
        video = depth_report_video_creator.render_depth_report_video(
            time_data=time_data, depth_data=depth_data, decimal_places=decimal_places
        )

        # Check the video is not None
        assert video is not None

        # Check the duration of the video (seconds)
        assert video.duration == 6

        # Check the number of clips in the video
        assert len(video.clips) == len(expected_texts)

        # Check the text of each clip in the video
        video_clip_texts = [video.clips[i].text for i in range(len(video.clips))]
        assert video_clip_texts == expected_texts

    @pytest.mark.parametrize(
        "decimal_places",
        [-1, 3, 4, None, "string", 1.5, 0.5, 0.0],
    )
    def test_render_depth_video_with_invalid_decimal_places(
        self, decimal_places: Any
    ) -> None:
        """Test the render_depth_report_video method with invalid decimal places."""
        # Create a DepthReportVideoCreator instance
        depth_report_video_creator = DepthReportVideoCreator(fps=1)

        # Create a depth report video with invalid decimal places
        time_data = [1.0, 2.0, 3.0]
        depth_data = [0.1, 0.2, 0.3]
        with pytest.raises(DepthReportVideoCreatorError) as e:
            _ = depth_report_video_creator.render_depth_report_video(
                time_data=time_data,
                depth_data=depth_data,
                decimal_places=decimal_places,
            )
        assert (
            str(e.value)
            == "Invalid decimal places value; must be a number between 0 and 2."
        )

    @pytest.mark.parametrize(
        "minus_sign, decimal_places, expected_texts",
        [
            (True, 0, ["0m", "-1m", "-2m", "-3343m"]),
            (False, 0, ["0m", "1m", "2m", "3343m"]),
            (True, 1, ["-0.1m", "-0.2m", "-0.3m", "-1.2m", "-2.0m", "-3343.3m"]),
            (False, 1, ["0.1m", "0.2m", "0.3m", "1.2m", "2.0m", "3343.3m"]),
            (True, 2, ["-0.10m", "-0.20m", "-0.30m", "-1.23m", "-2.00m", "-3343.33m"]),
            (False, 2, ["0.10m", "0.20m", "0.30m", "1.23m", "2.00m", "3343.33m"]),
        ],
    )
    def test_render_depth_video_with_no_minus_sign_option(
        self, minus_sign: bool, decimal_places: int, expected_texts: list[str]
    ) -> None:
        """Test the render_depth_report_video method with no minus option."""
        # Create a DepthReportVideoCreator instance
        depth_report_video_creator = DepthReportVideoCreator(fps=1)

        # Create a depth report video with no minus option
        time_data = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
        depth_data = [0.1, 0.2, 0.3, 1.233, 2.0, 3343.33]
        video = depth_report_video_creator.render_depth_report_video(
            time_data=time_data,
            depth_data=depth_data,
            decimal_places=decimal_places,
            minus_sign=minus_sign,
        )

        # Check the video is not None
        assert video is not None

        # Check the duration of the video (seconds)
        assert video.duration == 6

        # Check the number of clips in the video
        assert len(video.clips) == len(expected_texts)

        # Check the text of each clip in the video
        video_clip_texts = [video.clips[i].text for i in range(len(video.clips))]
        assert video_clip_texts == expected_texts

    def test_render_depth_report_video_with_user_font(
        self, request: pytest.FixtureRequest
    ) -> None:
        """Test the render_depth_report_video method with a user-specified font."""
        file_path = str(
            request.path.parent.joinpath(
                "data", "assets", "fonts", "OpenSans-Regular.ttf"
            )
        )

        # Create a DepthReportVideoCreator instance
        depth_report_video_creator = DepthReportVideoCreator(fps=1, font=file_path)

        # Create a depth report video with a user font
        time_data = [0.0, 1.0, 2.0, 3.0]
        depth_data = [0.0, 1.0, 2.0, 3.0]
        video = depth_report_video_creator.render_depth_report_video(
            time_data=time_data, depth_data=depth_data
        )

        # Check the video is not None
        assert video is not None

        # Check the duration of the video (seconds)
        assert video.duration == 4

        # Check the number of clips in the video
        assert len(video.clips) == 4

        # Check the text of each clip in the video
        video_clip_texts = [video.clips[i].text for i in range(len(video.clips))]
        assert video_clip_texts == ["0m", "-1m", "-2m", "-3m"]

    @pytest.mark.parametrize(
        "font, expected_error_prefix",
        [
            ("nonexistent.ttf", "Font file not found: "),
            ("", "Font you provided is not a file: "),
            ("invalid_font.ttf", "Error loading font file: "),
            ("invalid_font_filetype.txt", "Error loading font file: "),
        ],
    )
    def test_render_depth_report_video_with_user_font_invalid_file(
        self, request: pytest.FixtureRequest, font: str, expected_error_prefix: str
    ) -> None:
        """Test the render_depth_report_video method with a user-specified font."""
        file_path = str(request.path.parent.joinpath("data", "assets", "fonts", font))

        with pytest.raises(OverlayVideoCreatorError) as e:
            # Create a DepthReportVideoCreator instance
            _ = DepthReportVideoCreator(fps=1, font=file_path)

        assert f"{expected_error_prefix}{file_path}" in str(e.value)

    @pytest.mark.parametrize(
        "bg_color",
        [
            "#000000",
            "black",
            "green",
        ],
    )
    def test_render_depth_report_video_with_bg_color(self, bg_color: str) -> None:
        """Test the render_depth_report_video method with a background color."""
        _ = DepthReportVideoCreator(fps=1, bg_color=bg_color)

    @pytest.mark.parametrize(
        "bg_color",
        ["#00000", "blackk", "greenn", ""],
    )
    def test_render_depth_report_video_with_invalid_bg_color(
        self, bg_color: str
    ) -> None:
        """Test the render_depth_report_video method with an invalid background color."""
        with pytest.raises(OverlayVideoCreatorError) as e:
            _ = DepthReportVideoCreator(fps=1, bg_color=bg_color)

        assert "Invalid background color: " in str(e.value)

    @pytest.mark.parametrize(
        "stroke_width",
        [1, 2, 3],
    )
    def test_render_depth_report_video_with_stroke_width(
        self, stroke_width: int
    ) -> None:
        """Test the render_depth_report_video method with a stroke width."""
        _ = DepthReportVideoCreator(fps=1, stroke_width=stroke_width)

    @pytest.mark.parametrize(
        "stroke_width",
        [-1, "", "a"],
    )
    def test_render_depth_report_video_with_invalid_stroke_width(
        self, stroke_width: Any
    ) -> None:
        """Test the render_depth_report_video method with an invalid stroke width."""
        with pytest.raises(OverlayVideoCreatorError) as e:
            _ = DepthReportVideoCreator(fps=1, stroke_width=stroke_width)

        assert "Invalid stroke width; must be a positive number." in str(e.value)

# Copyright (c) 2024 - 2025 Noppanut Ploywong (@noppanut15) <noppanut.connect@gmail.com>
# Apache License 2.0 (see LICENSE file or http://www.apache.org/licenses/LICENSE-2.0)


"""Module to create a timer video."""

import math
from typing import Union
from moviepy import VideoClip
from depthviz.video.video_creator import (
    OverlayVideoCreator,
    OverlayVideoCreatorError,
    DEFAULT_FONT,
    DEFAULT_BG_COLOR,
    DEFAULT_STROKE_WIDTH,
    DEFAULT_VIDEO_SIZE,
)


class TimeReportVideoCreatorError(OverlayVideoCreatorError):
    """Base class for exceptions in this module."""


class TimeReportVideoCreator(OverlayVideoCreator):
    """Class to create a video that reports the depth in meters from an array input."""

    def __init__(
        self,
        font: str = DEFAULT_FONT,
        bg_color: str = DEFAULT_BG_COLOR,
        stroke_width: int = DEFAULT_STROKE_WIDTH,
        size: tuple[int, int] = DEFAULT_VIDEO_SIZE,
    ):
        """Initializes the TimeReportVideoCreator object.

        Args:
            font: The font file path.
            bg_color: The background color in hexadecimal format or color name.
            stroke_width: The stroke width.
            size: The video size.
        """
        super().__init__(
            font=font,
            bg_color=bg_color,
            stroke_width=stroke_width,
            size=size,
            fps=4,  # Set the frame rate to 4 fps
        )

    def _convert_time_to_text(self, time: float) -> str:
        """Converts a time value to a text string.

        Args:
            time: The time value in seconds.

        Returns:
            The time value as mm:ss.
        """
        minutes = int(time // 60)
        seconds = int(time % 60)
        return f"{minutes:02d}:{seconds:02d}"

    def render_time_report_video(
        self,
        time_data: list[float],
    ) -> VideoClip:
        """Creates a video that reports the depth in meters from an array input.

        Args:
            time_data: An array of time values in seconds.

        Returns:
            The processed video.
        """
        # Check the time data is not empty
        if not time_data:
            raise TimeReportVideoCreatorError("The time data is empty.")

        # Check the time data is positive
        if any(time < 0 for time in time_data):
            raise TimeReportVideoCreatorError("The time data contains negative values.")

        # Create a list of time frames
        time_frame_list: list[dict[str, Union[str, float]]] = []
        start = 0
        end = math.ceil(time_data[-1] - time_data[0])
        for time in range(start, end + 1):
            for _ in range(self.fps):
                time_frame_list.append(
                    {"text": self._convert_time_to_text(time), "duration": 1 / self.fps}
                )
        full_video = super().render_text_video(time_frame_list)
        return full_video

    def to_time_output_path(self, path: str) -> str:
        """Convert a video path to a time output path by adding a suffix `_time`.

        Args:
            path: The video path.

        Returns:
            The time output path.
        """
        path_split = path.split(".")
        path_split[-2] += "_time"
        return ".".join(path_split)

    def save(
        self, video: VideoClip, path: str, progress_bar_desc: str = "Exporting"
    ) -> None:
        """Save the video to a file.

        Args:
            video: The video to save.
            path: The path to save the video to.
            progress_bar_desc: The description for the progress bar.
        """
        # Add a suffix `_time` to the file name
        path = self.to_time_output_path(path)
        super().save(video=video, path=path, progress_bar_desc=progress_bar_desc)

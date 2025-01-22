"""
Module to create a timer video.
"""

import math
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
    """
    Class to create a video that reports the depth in meters from an array input.
    """

    def __init__(
        self,
        font: str = DEFAULT_FONT,
        bg_color: str = DEFAULT_BG_COLOR,
        stroke_width: int = DEFAULT_STROKE_WIDTH,
        size: tuple[int, int] = DEFAULT_VIDEO_SIZE,
    ):
        super().__init__(
            font=font,
            bg_color=bg_color,
            stroke_width=stroke_width,
            size=size,
            fps=1,  # Set the frame rate to 1 fps
        )

    def _convert_time_to_text(self, time: float) -> str:
        """
        Converts a time value to a text string.

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
        """
        Creates a video that reports the depth in meters from an array input.

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
        time_frame_list = []
        start = 0
        end = math.ceil(time_data[-1] - time_data[0])
        for time in range(start, end + 1):
            time_frame_list.append(
                {"text": self._convert_time_to_text(time), "duration": 1}
            )
        full_video = super().render_text_video(time_frame_list)
        return full_video

    def save(
        self, video: VideoClip, path: str, progress_bar_desc: str = "Exporting"
    ) -> None:
        """
        Save the video to a file.

        Args:
            video: The video to save.
            path: The path to save the video to.
        """
        # Add a suffix `_time` to the file name
        path = path.split(".")
        path[-2] += "_time"
        path = ".".join(path)
        super().save(video=video, path=path, progress_bar_desc=progress_bar_desc)

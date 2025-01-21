"""
Module to create a video that reports the depth in meters from an array input.
"""

import os.path
from typing import Tuple, cast
from moviepy import TextClip, VideoClip, concatenate_videoclips
from tqdm import tqdm
from depthviz.logger import DepthVizProgessBarLogger
from depthviz.optimizer.linear_interpolation import (
    LinearInterpolationDepth,
    LinearInterpolationDepthError,
)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_FONT = os.path.abspath(
    os.path.join(BASE_DIR, "assets/fonts/Open_Sans/static/OpenSans-Bold.ttf")
)


class DepthReportVideoCreatorError(Exception):
    """Base class for exceptions in this module."""


class VideoNotRenderError(DepthReportVideoCreatorError):
    """Exception raised for video not rendered errors."""


class VideoFormatError(DepthReportVideoCreatorError):
    """Exception raised for invalid video format errors."""


class DepthReportVideoCreator:
    """
    Class to create a video that reports the depth in meters from an array input.
    """

    def __init__(
        self,
        font: str = DEFAULT_FONT,
        fontsize: int = 100,
        interline: int = -20,
        color: str = "white",
        bg_color: str = "black",
        stroke_color: str = "black",
        stroke_width: int = 2,
        align: str = "center",
        size: Tuple[int, int] = (640, 360),
        fps: int = 25,
    ):
        self.font = font
        self.fontsize = fontsize
        self.interline = interline
        self.color = color
        self.bg_color = bg_color
        self.stroke_color = stroke_color
        self.stroke_width = stroke_width
        self.align = align
        self.size = size
        self.fps = fps
        self.final_video = None
        self.progress_bar_logger_config = {
            "unit": "f",
            "color": "#3982d8",
            "ncols": 70,
        }

        # Validate the font file
        self.__font_validate()
        # Validate the background color
        self.__bg_color_validate()
        # Validate the stroke width
        if not isinstance(stroke_width, int) or stroke_width < 0:
            raise DepthReportVideoCreatorError(
                "Invalid stroke width; must be a positive number."
            )

    def __clip_duration_in_seconds(
        self, current_pos: int, time_data: list[float]
    ) -> float:
        """
        Returns the total duration of the video in seconds.

        Args:
            current_pos: The current position in the array.
            time_data: An array of time values in seconds.

        Returns:
            The total duration of the video in seconds.
        """
        if current_pos == len(time_data) - 1:
            # If it's the last element, return the difference between the last two elements
            return abs(time_data[current_pos] - time_data[current_pos - 1])
        # Otherwise, return the difference between the current and next element
        return abs(time_data[current_pos + 1] - time_data[current_pos])

    def render_depth_report_video(
        self,
        time_data: list[float],
        depth_data: list[float],
        decimal_places: int = 0,
        minus_sign: bool = True,
    ) -> None:
        """
        Creates a video that reports the depth in meters from an array input.

        Args:
            time_data: An array of time values in seconds.
            depth_data: An array of depth values in meters.
            decimal_places: The number of decimal places to round the depth values to.
            minus_sign: A boolean value to determine if the minus sign should be displayed.

        Returns:
            The processed video.
        """
        # Check the decimal places value
        if (
            not isinstance(decimal_places, int)
            or decimal_places < 0
            or decimal_places > 2
        ):
            raise DepthReportVideoCreatorError(
                "Invalid decimal places value; must be a number between 0 and 2."
            )
        # Interpolate the depth data
        try:
            interpolated_depth = LinearInterpolationDepth(
                times=time_data, depths=depth_data, fps=self.fps
            )
            interpolated_depths = interpolated_depth.get_interpolated_depths()
            interpolated_times = interpolated_depth.get_interpolated_times()
            # Create a text clip for each depth value and track the progress with a progress bar
            clips = []
            clip_count = len(interpolated_times)
            for i in tqdm(
                iterable=range(clip_count),
                desc="Rendering",
                colour=str(self.progress_bar_logger_config["color"]),
                unit=str(self.progress_bar_logger_config["unit"]),
                ncols=cast(int, self.progress_bar_logger_config["ncols"]),
                bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} ({remaining} remaining)",
                leave=False,
            ):
                duration = self.__clip_duration_in_seconds(i, interpolated_times)
                if decimal_places == 0:
                    rounded_current_depth = round(interpolated_depths[i])
                    if rounded_current_depth == 0:
                        text = "0m"
                    else:
                        text = f"{'-' if minus_sign else ''}{rounded_current_depth}m"
                else:
                    current_depth = round(interpolated_depths[i], decimal_places)
                    if current_depth == 0:
                        text = f"{0:.{decimal_places}f}m"
                    else:
                        text = f"{'-' if minus_sign else ''}{current_depth:.{decimal_places}f}m"

                clip = TextClip(
                    text=text,
                    font=self.font,
                    font_size=self.fontsize,
                    interline=self.interline,
                    color=self.color,
                    bg_color=self.bg_color,
                    stroke_color=self.stroke_color,
                    stroke_width=self.stroke_width,
                    text_align=self.align,
                    size=self.size,
                    duration=duration,
                )
                clips.append(clip)

            # Concatenate all the clips into a single video
            self.final_video = concatenate_videoclips(clips)
        except LinearInterpolationDepthError as e:
            raise DepthReportVideoCreatorError(f"Interpolation Error; ({e})") from e

    def save(self, path: str) -> None:
        """
        Saves the video to a file.

        Args:
            path: The path to save the video (expected file format: .mp4).
        """
        parent_dir = os.path.dirname(path)
        if parent_dir == "":
            parent_dir = "./"
        if os.path.exists(parent_dir):
            if os.path.isdir(path):
                raise NameError(
                    f"{path} is a directory, please add a file name to the path. \
                        (e.g., path/to/mydepth_video.mp4)"
                )
            if self.final_video is not None:
                if not path.endswith(".mp4"):
                    raise VideoFormatError(
                        "Invalid file format: The file format must be .mp4"
                    )
                self.final_video.write_videofile(
                    path,
                    fps=self.fps,
                    logger=DepthVizProgessBarLogger(
                        description="Exporting",
                        unit=self.progress_bar_logger_config["unit"],
                        color=self.progress_bar_logger_config["color"],
                        ncols=self.progress_bar_logger_config["ncols"],
                    ),
                )
            else:
                raise VideoNotRenderError(
                    "Cannot save video because it has not been rendered yet."
                )
        else:
            raise FileNotFoundError(f"Parent directory does not exist: {parent_dir}")

    def get_video(self) -> VideoClip:
        """
        Returns the processed video.

        Returns:
            The processed video.
        """
        return self.final_video

    def __font_validate(self) -> None:
        """
        Validates the font file.

        Args:
            font: The font file path.
        """
        # Check if the font file exists
        if not os.path.exists(self.font):
            raise DepthReportVideoCreatorError(f"Font file not found: {self.font}")

        # Check if the font file is a file
        if not os.path.isfile(self.font):
            raise DepthReportVideoCreatorError(
                f"Font you provided is not a file: {self.font}"
            )

        # Check if the font file is a valid font file
        try:
            TextClip(font=self.font, text="Test", font_size=1)
        except ValueError as e:
            raise DepthReportVideoCreatorError(
                f"Error loading font file: {self.font}, "
                "make sure it's a valid font file (TrueType or OpenType font)."
            ) from e

    def __bg_color_validate(self) -> None:
        """
        Validates the background color.
        """
        # Check if the background color is a valid color
        try:
            TextClip(
                text="Test",
                font=self.font,
                font_size=self.fontsize,
                bg_color=self.bg_color,
            )
        except ValueError as e:
            raise DepthReportVideoCreatorError(
                f"Invalid background color: {self.bg_color}"
            ) from e

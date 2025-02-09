# Copyright (c) 2024 - 2025 Noppanut Ploywong (@noppanut15) <noppanut.connect@gmail.com>
# Apache License 2.0 (see LICENSE file or http://www.apache.org/licenses/LICENSE-2.0)


"""Module to create a video that reports the depth in meters from an array input."""

from typing import Union
from moviepy import VideoClip
from depthviz.video.video_creator import OverlayVideoCreator, OverlayVideoCreatorError
from depthviz.optimizer.linear_interpolation import (
    LinearInterpolationDepth,
    LinearInterpolationDepthError,
)


class DepthReportVideoCreatorError(OverlayVideoCreatorError):
    """Base class for exceptions in this module."""


class DepthReportVideoCreator(OverlayVideoCreator):
    """Class to create a video that reports the depth in meters from an array input."""

    def __clip_duration_in_seconds(
        self, current_pos: int, time_data: list[float]
    ) -> float:
        """Returns the total duration of the video in seconds.

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
    ) -> VideoClip:
        """Creates a video that reports the depth in meters from an array input.

        Args:
            time_data: An array of time values in seconds.
            depth_data: An array of depth values in meters.
            decimal_places: The number of decimal places to round the depth values to.
            minus_sign: A boolean value to determine if the minus sign should be displayed.

        Returns:
            The processed video.

        Raises:
            DepthReportVideoCreatorError: If the decimal places value is invalid
            DepthReportVideoCreatorError: If there is an error in the interpolation process
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

            depth_frame_list: list[dict[str, Union[str, float]]] = []
            previous_text = "NA"
            clip_count = len(interpolated_times)
            for i in range(clip_count):
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
                # Check if the text is the same as the previous text to reduce the number of clips
                # with the same text for better performance when rendering
                if text != previous_text:
                    # Append the text and duration to the list
                    depth_frame_list.append({"text": text, "duration": duration})
                    previous_text = text
                else:
                    # If the text is the same, just add the duration to the last clip
                    previous_duration = float(depth_frame_list[-1]["duration"])
                    depth_frame_list[-1]["duration"] = previous_duration + duration

            full_video = super().render_text_video(depth_frame_list)
            return full_video
        except LinearInterpolationDepthError as e:
            raise DepthReportVideoCreatorError(f"Interpolation Error; ({e})") from e

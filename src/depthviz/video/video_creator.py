# Copyright (c) 2024 - 2025 Noppanut Ploywong (@noppanut15) <noppanut.connect@gmail.com>
# Apache License 2.0 (see LICENSE file or http://www.apache.org/licenses/LICENSE-2.0)


"""Generic video creator module to create a video from an array input."""

import os.path
from typing import Tuple, cast, Union
from moviepy import TextClip, VideoClip, concatenate_videoclips
from tqdm import tqdm
from depthviz.video.logger import DepthVizProgessBarLogger

# Default values
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_FONT = os.path.abspath(
    os.path.join(BASE_DIR, "../assets/fonts/Open_Sans/static/OpenSans-Bold.ttf")
)
DEFAULT_VIDEO_SIZE = (960, 540)
DEFAULT_VIDEO_SIZE_FOR_TESTING = (640, 360)
DEFAULT_BG_COLOR = "black"
DEFAULT_STROKE_WIDTH = 5


class OverlayVideoCreatorError(Exception):
    """Base class for exceptions in this module."""


class VideoNotRenderError(OverlayVideoCreatorError):
    """Exception raised for video not rendered errors."""


class VideoFormatError(OverlayVideoCreatorError):
    """Exception raised for invalid video format errors."""


class OverlayVideoCreator:
    """Generic class to create an overlay video from an array input."""

    def __init__(
        self,
        font: str = DEFAULT_FONT,
        interline: int = -20,
        color: str = "white",
        bg_color: str = DEFAULT_BG_COLOR,
        stroke_color: str = "black",
        stroke_width: int = DEFAULT_STROKE_WIDTH,
        align: str = "center",
        size: Tuple[int, int] = DEFAULT_VIDEO_SIZE_FOR_TESTING,
        bitrate: str = "5000k",
        fps: int = 25,
    ):
        """Initializes the video creator.

        Args:
            font: The font file path.
            interline: The space between lines.
            color: The text color.
            bg_color: The background color.
            stroke_color: The stroke color.
            stroke_width: The stroke width.
            align: The text alignment.
            size: The video size.
            bitrate: The video bitrate.
            fps: The video frame rate.

        Raises:
            OverlayVideoCreatorError: An error occurred when validating the font file.
            OverlayVideoCreatorError: An error occurred when validating the background color.
            OverlayVideoCreatorError: An error occurred when validating the stroke width.
        """
        self.font = font
        self.fontsize = int(
            size[1] * 120 / 360
        )  # 120 is the default font size for 640x360 resolution
        self.interline = interline
        self.color = color
        self.bg_color = bg_color
        self.stroke_color = stroke_color
        self.stroke_width = stroke_width
        self.align = align
        self.size = size
        self.bitrate = bitrate
        self.fps = fps
        self.progress_bar_logger_config = {
            "unit": "f",
            "color": "#23aae1",
            "ncols": 80,
        }

        # Validate the font file
        self.__font_validate()
        # Validate the background color
        self.__bg_color_validate()
        # Validate the stroke width
        if not isinstance(stroke_width, int) or stroke_width < 0:
            raise OverlayVideoCreatorError(
                "Invalid stroke width; must be a positive number."
            )

    def render_text_video(
        self,
        text_list: list[dict[str, Union[str, float]]],
        progress_bar_desc: str = "Rendering",
    ) -> VideoClip:
        """Creates a video from an array input.

        Args:
            text_list: A list of dictionaries containing the text and duration for each frame.
            progress_bar_desc: The description for the progress bar.

        Returns:
            The processed video.

        Raises:
            VideoNotRenderError: An error occurred when the video is not rendered yet.
            VideoFormatError: An error occurred when the file format is invalid.
        """
        # Create a text clip for each text value and track the progress with a progress bar
        clips = []
        clip_count = len(text_list)
        for i in tqdm(
            iterable=range(clip_count),
            desc=progress_bar_desc,
            colour=str(self.progress_bar_logger_config["color"]),
            unit=str(self.progress_bar_logger_config["unit"]),
            ncols=cast(int, self.progress_bar_logger_config["ncols"]),
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} ({remaining} remaining)",
            leave=False,
        ):

            clip = TextClip(
                text=text_list[i]["text"],
                font=self.font,
                font_size=self.fontsize,
                interline=self.interline,
                color=self.color,
                bg_color=self.bg_color,
                stroke_color=self.stroke_color,
                stroke_width=self.stroke_width,
                text_align=self.align,
                size=self.size,
                duration=text_list[i]["duration"],
            )
            clips.append(clip)

        # Concatenate all the clips into a single video
        full_video = concatenate_videoclips(clips)
        return full_video

    def save(
        self, video: VideoClip, path: str, progress_bar_desc: str = "Exporting"
    ) -> None:
        """Saves the video to a file.

        Args:
            video: The video to save.
            path: The path to save the video (expected file format: .mp4).
            progress_bar_desc: The description for the progress bar.

        Raises:
            FileNotFoundError: An error occurred when the parent directory does not exist.
            VideoNotRenderError: An error occurred when the video is not rendered yet.
            VideoFormatError: An error occurred when the file format is invalid.
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
            if video is not None:
                if not path.endswith(".mp4"):
                    raise VideoFormatError(
                        "Invalid file format: The file format must be .mp4"
                    )
                video.write_videofile(
                    path,
                    fps=self.fps,
                    bitrate=self.bitrate,
                    logger=DepthVizProgessBarLogger(
                        description=progress_bar_desc,
                        unit=cast(str, self.progress_bar_logger_config["unit"]),
                        color=cast(str, self.progress_bar_logger_config["color"]),
                        ncols=cast(int, self.progress_bar_logger_config["ncols"]),
                    ),
                )
            else:
                raise VideoNotRenderError(
                    "Cannot save video because it has not been rendered yet."
                )
        else:
            raise FileNotFoundError(f"Parent directory does not exist: {parent_dir}")

    def __font_validate(self) -> None:
        """Validates the font file.

        Raises:
            OverlayVideoCreatorError: An error occurred when the font file is not found.
            OverlayVideoCreatorError: An error occurred when the font file is not a file.
            OverlayVideoCreatorError: An error occurred when the font file is invalid.
        """
        # Check if the font file exists
        if not os.path.exists(self.font):
            raise OverlayVideoCreatorError(f"Font file not found: {self.font}")

        # Check if the font file is a file
        if not os.path.isfile(self.font):
            raise OverlayVideoCreatorError(
                f"Font you provided is not a file: {self.font}"
            )

        # Check if the font file is a valid font file
        try:
            TextClip(font=self.font, text="Test", font_size=1)
        except ValueError as e:
            raise OverlayVideoCreatorError(
                f"Error loading font file: {self.font}, "
                "make sure it's a valid font file (TrueType or OpenType font)."
            ) from e

    def __bg_color_validate(self) -> None:
        """Validates the background color.

        Raises:
            OverlayVideoCreatorError: An error occurred when the background color is invalid.
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
            raise OverlayVideoCreatorError(
                f"Invalid background color: {self.bg_color}"
            ) from e

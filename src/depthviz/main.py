# Copyright (c) 2024 - 2025 Noppanut Ploywong (@noppanut15) <noppanut.connect@gmail.com>
# Apache License 2.0 (see LICENSE file or http://www.apache.org/licenses/LICENSE-2.0)


"""Main module for the depthviz command line interface.

This module contains the DepthvizApplication class which is responsible for
handling the depthviz command line interface. The DepthvizApplication class
parses the command line arguments, validates the user input, and creates the
depth overlay video.

Notes:
    The DepthvizApplication class is designed to be used as a standalone
    command line interface. It can be run directly from the command line
    using the `python -m depthviz` command or by running the `depthviz` 
    if the package is installed.
"""

import sys
import argparse
from depthviz.__version__ import __version__
from depthviz.parsers.generic.generic_divelog_parser import (
    DiveLogParser,
    DiveLogParserError,
)
from depthviz.parsers.apnealizer.csv_parser import ApnealizerCsvParser
from depthviz.parsers.shearwater.shearwater_xml_parser import ShearwaterXmlParser
from depthviz.parsers.garmin.fit_parser import GarminFitParser
from depthviz.parsers.suunto.fit_parser import SuuntoFitParser
from depthviz.parsers.manual.csv_parser import ManualCsvParser
from depthviz.video.video_creator import (
    OverlayVideoCreatorError,
    DEFAULT_FONT,
    DEFAULT_VIDEO_SIZE,
    DEFAULT_BG_COLOR,
    DEFAULT_STROKE_WIDTH,
)
from depthviz.video.depth import DepthReportVideoCreator
from depthviz.video.time import TimeReportVideoCreator
from depthviz.banner import Banner


class DepthvizApplication:
    """Class to handle the depthviz command line interface.

    Attributes:
        parser: Argument parser for the command line interface.
        required_args: Group for required arguments in the parser.
    """

    def __init__(self) -> None:
        """Initialize the DepthvizApplication class."""
        self.parser = argparse.ArgumentParser(
            prog="depthviz",
            description="Generate depth overlay videos from your dive log.",
        )
        # REQUIRED ARGUMENTS
        self.required_args = self.parser.add_argument_group("required arguments")
        self.required_args.add_argument(
            "-i",
            "--input",
            help="Path to the file containing your dive log.",
            required=True,
        )
        self.required_args.add_argument(
            "-s",
            "--source",
            help="Source where the dive log was downloaded from. \
                This is required to correctly parse your data.",
            choices=["apnealizer", "shearwater", "garmin", "suunto", "manual"],
            required=True,
        )
        self.required_args.add_argument(
            "-o", "--output", help="Path or filename of the video file.", required=True
        )
        # OPTIONAL ARGUMENTS
        self.parser.add_argument(
            "-d",
            "--decimal-places",
            help="Number of decimal places to round the depth. Valid values: 0, 1, 2. (default: 0)",
            type=int,
            default=0,
        )
        self.parser.add_argument(
            "--no-minus",
            help="Hide the minus sign for depth values.",
            action="store_true",
        )
        self.parser.add_argument(
            "--font", help="Path to the font file.", type=str, default=DEFAULT_FONT
        )
        self.parser.add_argument(
            "--bg-color",
            help=f"Background color of the video. (default: {DEFAULT_BG_COLOR})",
            type=str,
            default=DEFAULT_BG_COLOR,
        )
        self.parser.add_argument(
            "--stroke-width",
            help="Width of the stroke around the text in pixels. "
            f"(default: {DEFAULT_STROKE_WIDTH})",
            type=int,
            default=DEFAULT_STROKE_WIDTH,
        )
        self.parser.add_argument(
            "--depth-mode",
            help="Control how the depth is displayed. (default: raw)",
            type=str,
            choices=["raw", "zero-based"],
            default="raw",
        )
        self.parser.add_argument(
            "--time", help="Create a time overlay video.", action="store_true"
        )
        self.parser.add_argument(
            "-v",
            "--version",
            action="version",
            version=f"%(prog)s version {__version__}",
        )

    def create_depth_video(
        self,
        divelog_parser: DiveLogParser,
        output_path: str,
        decimal_places: int,
        font: str,
        no_minus: bool = False,
        bg_color: str = DEFAULT_BG_COLOR,
        stroke_width: int = DEFAULT_STROKE_WIDTH,
    ) -> int:
        """Create the depth overlay video.

        Args:
            divelog_parser: DiveLogParser object containing the parsed dive log data.
            output_path: Path to save the output video file.
            decimal_places: Number of decimal places to round the depth.
            font: Path to the font file.
            no_minus: Hide the minus sign for depth values.
            bg_color: Background color of the video.
            stroke_width: Width of the stroke around the text in pixels.

        Returns:
            int: Return code for the depth overlay video creation.

        Exceptions:
            OverlayVideoCreatorError: An error occurred during the video creation.
        """
        try:
            time_data_from_divelog = divelog_parser.get_time_data()
            depth_data_from_divelog = divelog_parser.get_depth_data()
            depth_report_video_creator = DepthReportVideoCreator(
                fps=25,
                font=font,
                bg_color=bg_color,
                stroke_width=stroke_width,
                size=DEFAULT_VIDEO_SIZE,
            )
            video = depth_report_video_creator.render_depth_report_video(
                time_data=time_data_from_divelog,
                depth_data=depth_data_from_divelog,
                decimal_places=decimal_places,
                minus_sign=not no_minus,
            )
            depth_report_video_creator.save(video=video, path=output_path)
        except OverlayVideoCreatorError as e:
            print(e)
            return 1

        print(f"Depth video successfully created: {output_path}")
        return 0

    def create_time_video(
        self,
        divelog_parser: DiveLogParser,
        output_path: str,
        font: str,
        bg_color: str = DEFAULT_BG_COLOR,
        stroke_width: int = DEFAULT_STROKE_WIDTH,
    ) -> int:
        """Create the time overlay video.

        Args:
            divelog_parser: DiveLogParser object containing the parsed dive log data.
            output_path: Path to save the output video file.
            font: Path to the font file.
            bg_color: Background color of the video.
            stroke_width: Width of the stroke around the text in pixels.

        Returns:
            int: Return code for the time overlay video creation.

        Exceptions:
            OverlayVideoCreatorError: An error occurred during the video creation.
        """
        try:
            time_data_from_divelog = divelog_parser.get_time_data()
            time_report_video_creator = TimeReportVideoCreator(
                font=font,
                bg_color=bg_color,
                stroke_width=stroke_width,
                size=DEFAULT_VIDEO_SIZE,
            )
            video = time_report_video_creator.render_time_report_video(
                time_data=time_data_from_divelog
            )
            time_report_video_creator.save(video=video, path=output_path)
        except OverlayVideoCreatorError as e:
            print(e)
            return 1

        print(
            "Time video successfully created: "
            f"{time_report_video_creator.to_time_output_path(output_path)}"
        )
        return 0

    def is_user_input_valid(self, args: argparse.Namespace) -> bool:
        """Check if the user input is valid.

        Args:
            args: Parsed command line arguments.

        Returns:
            bool: True if the user input is valid, False otherwise.
        """
        if args.decimal_places not in [0, 1, 2]:
            print("Invalid value for decimal places. Valid values: 0, 1, 2.")
            return False

        if args.output[-4:] != ".mp4":
            print("Invalid output file extension. Please provide a .mp4 file.")
            return False

        return True

    def main(self) -> int:
        """Main method for the depthviz command line interface.

        This method parses the command line arguments, validates the user input,
        and creates the depth overlay video.

        Returns:
            int: Return code for the depthviz command line interface.

        Exceptions:
            DiveLogParserError: An error occurred during the dive log parsing.

        Notes:
            The main method is the entry point for the depthviz command line interface.
            It is called when the depthviz module is run as a script using the `depthviz` command.

            Currently, the main method supports the following sources:
                - Apnealizer CSV files
                - Shearwater XML files
                - Garmin FIT files
                - Suunto FIT files
                - Manual CSV files
        """
        if len(sys.argv) == 1:
            self.parser.print_help(sys.stderr)
            return 1

        args = self.parser.parse_args(sys.argv[1:])

        # Print the depthviz banner
        Banner.print_banner()

        # Check if the user input is valid before analyzing the dive log
        # This is to avoid long processing times for invalid input
        if not self.is_user_input_valid(args):
            return 1

        divelog_parser: DiveLogParser
        if args.source == "apnealizer":
            divelog_parser = ApnealizerCsvParser(depth_mode=args.depth_mode)
        elif args.source == "shearwater":
            divelog_parser = ShearwaterXmlParser(depth_mode=args.depth_mode)
        elif args.source == "garmin":
            divelog_parser = GarminFitParser(depth_mode=args.depth_mode)
        elif args.source == "suunto":
            divelog_parser = SuuntoFitParser(depth_mode=args.depth_mode)
        elif args.source == "manual":
            divelog_parser = ManualCsvParser(depth_mode=args.depth_mode)
        else:
            print(f"Source {args.source} not supported.")
            return 1

        try:
            divelog_parser.parse(file_path=args.input)
        except DiveLogParserError as e:
            print(e)
            return 1

        ret_code = self.create_depth_video(
            divelog_parser=divelog_parser,
            output_path=args.output,
            decimal_places=args.decimal_places,
            no_minus=args.no_minus,
            font=args.font,
            bg_color=args.bg_color,
            stroke_width=args.stroke_width,
        )

        # Exit if the depth overlay video creation failed
        if ret_code != 0:
            return ret_code

        # Create a time overlay video
        if args.time:
            ret_code = self.create_time_video(
                divelog_parser=divelog_parser,
                output_path=args.output,
                font=args.font,
                bg_color=args.bg_color,
                stroke_width=args.stroke_width,
            )

        return ret_code


def run() -> int:
    """Run the depthviz command line interface.

    Returns:
        int: Return code for the depthviz command line interface.
    """
    app = DepthvizApplication()
    exit_code: int = app.main()
    return exit_code


if __name__ == "__main__":
    run()

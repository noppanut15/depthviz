"""
This module provides the command line interface for the depthviz package.
"""

import sys
import argparse
from depthviz._version import __version__
from depthviz.parsers.generic.generic_divelog_parser import (
    DiveLogParser,
    DiveLogParserError,
)
from depthviz.parsers.apnealizer.csv_parser import ApnealizerCsvParser
from depthviz.parsers.shearwater.shearwater_xml_parser import ShearwaterXmlParser
from depthviz.parsers.garmin.fit_parser import GarminFitParser
from depthviz.parsers.suunto.fit_parser import SuuntoFitParser
from depthviz.parsers.manual.csv_parser import ManualCsvParser
from depthviz.core import (
    DepthReportVideoCreator,
    DepthReportVideoCreatorError,
    DEFAULT_FONT,
)

# Banner for the command line interface
BANNER = """
     _,-._
    / \\_/ \\    d e p t h v i z
    >-(_)-<
    \\_/ \\_/    ~~~~~~~~~~~~~~~
      `-'
"""


class DepthvizApplication:
    """
    Class to handle the depthviz command line interface.
    """

    def __init__(self) -> None:
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
            help="Background color of the video. (default: black)",
            type=str,
            default="black",
        )
        self.parser.add_argument(
            "--stroke-width",
            help="Width of the stroke around the text in pixels. (default: 2)",
            type=int,
            default=2,
        )

        self.parser.add_argument(
            "-v",
            "--version",
            action="version",
            version=f"%(prog)s version {__version__}",
        )

    def create_video(
        self,
        divelog_parser: DiveLogParser,
        output_path: str,
        decimal_places: int,
        font: str,
        no_minus: bool = False,
        bg_color: str = "black",
        stroke_width: int = 2,
    ) -> int:
        """
        Create the depth overlay video.
        """
        try:
            time_data_from_divelog = divelog_parser.get_time_data()
            depth_data_from_divelog = divelog_parser.get_depth_data()
            depth_report_video_creator = DepthReportVideoCreator(
                fps=25, font=font, bg_color=bg_color, stroke_width=stroke_width
            )
            depth_report_video_creator.render_depth_report_video(
                time_data=time_data_from_divelog,
                depth_data=depth_data_from_divelog,
                decimal_places=decimal_places,
                minus_sign=not no_minus,
            )
            depth_report_video_creator.save(output_path)
        except DepthReportVideoCreatorError as e:
            print(e)
            return 1

        print(f"Video successfully created: {output_path}")
        return 0

    def is_user_input_valid(self, args: argparse.Namespace) -> bool:
        """
        Check if the user input is valid.
        """
        if args.decimal_places not in [0, 1, 2]:
            print("Invalid value for decimal places. Valid values: 0, 1, 2.")
            return False

        if args.output[-4:] != ".mp4":
            print("Invalid output file extension. Please provide a .mp4 file.")
            return False

        return True

    def main(self) -> int:
        """
        Main function for the depthviz command line interface.
        """
        if len(sys.argv) == 1:
            self.parser.print_help(sys.stderr)
            return 1

        args = self.parser.parse_args(sys.argv[1:])

        print(BANNER)

        # Check if the user input is valid before analyzing the dive log
        # This is to avoid long processing times for invalid input
        if not self.is_user_input_valid(args):
            return 1

        divelog_parser: DiveLogParser
        if args.source == "apnealizer":
            divelog_parser = ApnealizerCsvParser()
        elif args.source == "shearwater":
            divelog_parser = ShearwaterXmlParser()
        elif args.source == "garmin":
            divelog_parser = GarminFitParser()
        elif args.source == "suunto":
            divelog_parser = SuuntoFitParser()
        elif args.source == "manual":
            divelog_parser = ManualCsvParser()
        else:
            print(f"Source {args.source} not supported.")
            return 1

        try:
            divelog_parser.parse(file_path=args.input)
        except DiveLogParserError as e:
            print(e)
            return 1

        return self.create_video(
            divelog_parser=divelog_parser,
            output_path=args.output,
            decimal_places=args.decimal_places,
            no_minus=args.no_minus,
            font=args.font,
            bg_color=args.bg_color,
            stroke_width=args.stroke_width,
        )


def run() -> int:
    """
    Entry point for the depthviz command line interface.
    """
    app = DepthvizApplication()
    exit_code: int = app.main()
    return exit_code


if __name__ == "__main__":
    run()

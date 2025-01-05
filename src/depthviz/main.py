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
from depthviz.core import DepthReportVideoCreator, DepthReportVideoCreatorError


class DepthvizApplication:
    """
    Class to handle the depthviz command line interface.
    """

    def __init__(self) -> None:
        self.banner = """
 #####  ###### #####  ##### #    # #    # # ###### 
 #    # #      #    #   #   #    # #    # #     #  
 #    # #####  #    #   #   ###### #    # #    #   
 #    # #      #####    #   #    # #    # #   #    
 #    # #      #        #   #    #  #  #  #  #     
 #####  ###### #        #   #    #   ##   # ###### 
"""
        self.parser = argparse.ArgumentParser(
            prog="depthviz",
            description="Generate depth overlay videos from your dive log.",
        )
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
            choices=["apnealizer", "shearwater"],
            required=True,
        )
        self.required_args.add_argument(
            "-o", "--output", help="Path or filename of the video file.", required=True
        )
        self.parser.add_argument(
            "-v",
            "--version",
            action="version",
            version=f"%(prog)s version {__version__}",
        )

    def create_video(self, divelog_parser: DiveLogParser, output_path: str) -> int:
        """
        Create the depth overlay video.
        """
        try:
            time_data_from_divelog = divelog_parser.get_time_data()
            depth_data_from_divelog = divelog_parser.get_depth_data()
            depth_report_video_creator = DepthReportVideoCreator()
            depth_report_video_creator.render_depth_report_video(
                time_data=time_data_from_divelog, depth_data=depth_data_from_divelog
            )
            depth_report_video_creator.save(output_path, fps=25)
        except DepthReportVideoCreatorError as e:
            print(e)
            return 1

        print("===================================================")
        print(f"Video successfully created: {output_path}")
        return 0

    def main(self) -> int:
        """
        Main function for the depthviz command line interface.
        """
        print(self.banner)
        if len(sys.argv) == 1:
            self.parser.print_help(sys.stderr)
            return 1

        print("===================================================")

        args = self.parser.parse_args(sys.argv[1:])

        if args.source == "apnealizer":
            divelog_parser = ApnealizerCsvParser()
        elif args.source == "shearwater":
            divelog_parser = ShearwaterXmlParser()
        else:
            print(f"Source {args.source} not supported.")
            return 1

        try:
            divelog_parser.parse(file_path=args.input)
        except DiveLogParserError as e:
            print(e)
            return 1

        return self.create_video(divelog_parser=divelog_parser, output_path=args.output)


def run() -> int:
    """
    Entry point for the depthviz command line interface.
    """
    app = DepthvizApplication()
    exit_code: int = app.main()
    return exit_code


if __name__ == "__main__":
    run()

"""
This module provides the command line interface for the depthviz package.
"""

import sys
import argparse
from depthviz._version import __version__
from depthviz.parsers.apnealizer.csv_parser import ApnealizerCsvParser
from depthviz.parsers.generic.csv.csv_parser import CsvParserError
from depthviz.core import DepthReportVideoCreator, DepthReportVideoCreatorError

BANNER = """
 #####  ###### #####  ##### #    # #    # # ###### 
 #    # #      #    #   #   #    # #    # #     #  
 #    # #####  #    #   #   ###### #    # #    #   
 #    # #      #####    #   #    # #    # #   #    
 #    # #      #        #   #    #  #  #  #  #     
 #####  ###### #        #   #    #   ##   # ###### 
"""


def main() -> int:
    """
    Main function for the depthviz command line interface.
    """
    print(BANNER)
    parser = argparse.ArgumentParser(
        prog="depthviz", description="Generate depth overlay videos from your dive log."
    )
    required_args = parser.add_argument_group("required arguments")
    required_args.add_argument(
        "-i",
        "--input",
        help="Path to the CSV file containing your dive log.",
        required=True,
    )
    required_args.add_argument(
        "-o", "--output", help="Path or filename of the video file.", required=True
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s version {__version__}",
    )

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        return 1

    print("===================================================")
    args = parser.parse_args(sys.argv[1:])

    # Parse the Apnealizer CSV file
    csv_parser = ApnealizerCsvParser()
    try:
        csv_parser.parse(args.input)
    except CsvParserError as e:
        print(e)
        return 1

    # Create the video
    try:
        time_data_from_csv = csv_parser.get_time_data()
        depth_data_from_csv = csv_parser.get_depth_data()
        depth_report_video_creator = DepthReportVideoCreator()
        depth_report_video_creator.render_depth_report_video(
            time_data=time_data_from_csv, depth_data=depth_data_from_csv
        )
        depth_report_video_creator.save(args.output, fps=25)
    except DepthReportVideoCreatorError as e:
        print(e)
        return 1

    print("===================================================")
    print(f"Video successfully created: {args.output}")
    return 0


def run() -> int:
    """
    Entry point for the depthviz command line interface.
    """
    exit_code: int = main()
    return exit_code


if __name__ == "__main__":
    run()

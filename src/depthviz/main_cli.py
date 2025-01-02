"""
This module provides the command line interface for the depthviz package.
"""

import sys
import argparse
from depthviz.csv_parser import CsvParser, CsvParserError
from depthviz.core import DepthReportVideoCreator

BANNER = """
 #####  ###### #####  ##### #    # #    # # ###### 
 #    # #      #    #   #   #    # #    # #     #  
 #    # #####  #    #   #   ###### #    # #    #   
 #    # #      #####    #   #    # #    # #   #    
 #    # #      #        #   #    #  #  #  #  #     
 #####  ###### #        #   #    #   ##   # ###### 
"""


def main():
    """
    Main function for the depthviz command line interface.
    """
    print(BANNER)
    parser = argparse.ArgumentParser(
        description="Generate depth overlay videos from your dive log."
    )
    required_args = parser.add_argument_group("required arguments")
    required_args.add_argument(
        "-i",
        "--input",
        help="Path to the CSV file containing depth data.",
        required=True,
    )
    required_args.add_argument(
        "-s",
        "--sample-rate",
        help="Sample rate of your dive computer in seconds. \
            The sample rate controls how often information from the dive is saved to the dive log. \
            (e.g., 1, 0.50, 0.25)",
        required=True,
    )
    required_args.add_argument(
        "-o", "--output", help="Path or filename of the video file.", required=True
    )

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        return 1

    print("===================================================")
    args = parser.parse_args(sys.argv[1:])

    # Parse the CSV file
    csv_parser = CsvParser()
    try:
        csv_parser.parse(args.input)
    except CsvParserError as e:
        print(e)
        return 1

    # Create the video
    depth_data_from_csv = csv_parser.get_depth_data()
    depth_report_video_creator = DepthReportVideoCreator(
        sample_rate=float(args.sample_rate)
    )
    depth_report_video_creator.render_depth_report_video(depth_data_from_csv)

    # Write the video to a file
    depth_report_video_creator.save(args.output, fps=25)
    print("===================================================")
    print(f"Video successfully created: {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

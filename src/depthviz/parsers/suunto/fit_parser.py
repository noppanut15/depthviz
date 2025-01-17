"""
This module contains the SuuntoFitParser class 
which is used to parse a Suunto FIT file from Suunto App
"""

import math
from typing import cast, Union
from datetime import datetime, timezone
from garmin_fit_sdk import Decoder, Stream

from depthviz.parsers.generic.generic_divelog_parser import DiveLogFileNotFoundError
from depthviz.parsers.generic.fit.fit_parser import (
    DiveLogFitParser,
    DiveLogFitInvalidFitFileError,
    DiveLogFitInvalidFitFileTypeError,
    DiveLogFitDiveNotFoundError,
)
from pprint import pprint

# Constants
CUT_OFF_DEPTH = 1.5  # The depth which the dive is considered to have started or ended


class SuuntoFitParser(DiveLogFitParser):
    """
    A class to parse a FIT file containing depth data.
    """

    def __init__(self, selected_dive_idx: int = -1) -> None:
        self.__time_data: list[float] = []
        self.__depth_data: list[float] = []

        # Select the dive to be parsed (in case of multiple dives in FIT file)
        self.__selected_dive_idx = selected_dive_idx

    def convert_fit_epoch_to_datetime(self, fit_epoch: int) -> str:
        """
        A method to convert the epoch time in the FIT file to a human-readable datetime string.
        """
        epoch = fit_epoch + 631065600
        return datetime.fromtimestamp(epoch, timezone.utc).strftime(
            "%Y-%m-%d %H:%M:%S (GMT)"
        )

    #     def select_dive(self, dive_summary: list[dict[str, Union[int, float]]]) -> int:
    #         """
    #         A method to prompt the user to select a dive from the FIT file,
    #         if there are multiple dives in the file.
    #         """
    #         if len(dive_summary) == 1:
    #             return 0
    #         print("Multiple dives found in the FIT file. Please select a dive to import:\n")
    #         for idx, dive in enumerate(dive_summary):
    #             start_time = self.convert_fit_epoch_to_datetime(
    #                 cast(int, dive.get("start_time"))
    #             )
    #             print(
    #                 f"[{idx + 1}]: Dive {idx + 1}: Start Time: {start_time}, "
    #                 f"Max Depth: {cast(float, dive.get('max_depth')):.1f}m, "
    #                 f"Bottom Time: {cast(float, dive.get('bottom_time')):.1f}s"
    #             )
    #         try:
    #             selected_dive_idx = (
    #                 int(
    #                     input(
    #                         f"\nEnter the dive number to import [1-{len(dive_summary)}]: "
    #                     )
    #                 )
    #                 - 1
    #             )
    #             print()
    #         except ValueError as e:
    #             raise DiveLogFitDiveNotFoundError(
    #                 f"Invalid Dive: Please enter a number between 1 and {len(dive_summary)}"
    #             ) from e

    #         if selected_dive_idx >= len(dive_summary) or selected_dive_idx < 0:
    #             raise DiveLogFitDiveNotFoundError(
    #                 f"Invalid Dive: Please enter a number between 1 and {len(dive_summary)}"
    #             )
    #         return selected_dive_idx

    def parse(self, file_path: str) -> None:
        """
        A method to parse a Suunto FIT file containing depth data.
        """
        try:
            stream = Stream.from_file(file_path)
            decoder = Decoder(stream)
            messages, errors = decoder.read(convert_datetimes_to_dates=False)
            if errors:
                raise errors[0]
        except RuntimeError as e:
            raise DiveLogFitInvalidFitFileError(f"Invalid FIT file: {file_path}") from e
        except FileNotFoundError as e:
            raise DiveLogFileNotFoundError(f"File not found: {file_path}") from e

        try:
            file_id_mesgs = messages.get("file_id_mesgs", [])
            file_type = file_id_mesgs[0].get("type")
            manufacturer = file_id_mesgs[0].get("manufacturer")
        except (TypeError, IndexError) as e:
            raise DiveLogFitInvalidFitFileError(
                f"Invalid FIT file: {file_path}, cannot identify FIT type and manufacturer."
            ) from e

        if file_type != "activity":
            raise DiveLogFitInvalidFitFileTypeError(
                f"Invalid FIT file type: You must import 'activity', not '{file_type}'"
            )

        if manufacturer != "suunto":
            raise DiveLogFitInvalidFitFileTypeError(
                f"Invalid FIT file: You must import Suunto Dive Computer data, not '{manufacturer}'"
            )

        dive_summary = []

        records = messages.get("record_mesgs", [])

        raw_extracted_dive_logs = []
        current_dive = None
        previous_depth = 0
        previous_record = None
        descending = False
        ascending = False

        for record in records:
            timestamp = record.get("timestamp")
            depth = record.get("depth")

            if depth > 0:
                if current_dive is None:
                    current_dive = {
                        "data": [],
                        "max_depth": 0,
                    }
                    if previous_record is not None:
                        current_dive["data"].append(
                            {
                                "timestamp": previous_record.get("timestamp"),
                                "depth": previous_record.get("depth"),
                            }
                        )
                    raw_extracted_dive_logs.append(current_dive)

                if depth > CUT_OFF_DEPTH:
                    descending = True
                if descending and depth < CUT_OFF_DEPTH:
                    ascending = True

                if not descending and depth < previous_depth:
                    current_dive = None
                    descending = False
                    ascending = False
                if descending and ascending and depth > previous_depth:
                    current_dive = None
                    descending = False
                    ascending = False

                if current_dive is not None:
                    current_dive["data"].append(
                        {"timestamp": timestamp, "depth": depth}
                    )
                    current_dive["max_depth"] = max(current_dive["max_depth"], depth)

                previous_depth = depth
            else:
                current_dive = None
                descending = False
                ascending = False
            previous_record = record

        # Dive Summary
        for log in raw_extracted_dive_logs:
            if log["max_depth"] > 3:
                start_time = log["data"][0]["timestamp"]
                end_time = log["data"][-1]["timestamp"]
                max_depth = log["max_depth"]
                bottom_time = end_time - start_time
                dive_summary.append(
                    {
                        "raw_data": log["data"],
                        "start_time": start_time,
                        "end_time": end_time,
                        "max_depth": max_depth,
                        "bottom_time": bottom_time,
                    }
                )
        if not dive_summary:
            raise DiveLogFitDiveNotFoundError(
                f"Invalid FIT file: {file_path} does not contain any dive data deeper than 3m."
            )

        # TODO: A prompt to select the dive if there are multiple dives in the FIT file
        #         # A prompt to select the dive if there are multiple dives in the FIT file
        #         if self.__selected_dive_idx == -1:
        #             self.__selected_dive_idx = self.select_dive(dive_summary)

        # Parse the depth data for the selected dive
        records = dive_summary[self.__selected_dive_idx].get("raw_data", [])
        first_timestamp = None
        for record in records:
            timestamp = record.get("timestamp")
            if first_timestamp is None:
                first_timestamp = timestamp
            time = float(timestamp - first_timestamp)
            depth = record.get("depth")
            self.__time_data.append(time)
            self.__depth_data.append(depth)

        if not self.__time_data or not self.__depth_data:
            raise DiveLogFitDiveNotFoundError(
                f"Invalid Dive Data: Dive data not found in FIT file: {file_path}"
            )

    def get_time_data(self) -> list[float]:
        """
        Returns the time data parsed from the FIT file.
        Returns:
            The time data parsed from the FIT file.
        """
        return self.__time_data

    def get_depth_data(self) -> list[float]:
        """
        Returns the depth data parsed from the FIT file.
        Returns:
            The depth data parsed from the FIT file.
        """
        return self.__depth_data

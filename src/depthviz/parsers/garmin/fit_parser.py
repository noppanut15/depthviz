"""
This module contains the GarminFitParser class 
which is used to parse a Garmin FIT file from Garmin Connect
"""

import math
from typing import cast
from garmin_fit_sdk import Decoder, Stream

from depthviz.parsers.generic.generic_divelog_parser import DiveLogFileNotFoundError
from depthviz.parsers.generic.fit.fit_parser import (
    DiveLogFitParser,
    DiveLogFitInvalidFitFileError,
    DiveLogFitInvalidFitFileTypeError,
    DiveLogFitDiveNotFoundError,
)


class GarminFitParser(DiveLogFitParser):
    """
    A class to parse a FIT file containing depth data.
    """

    def __init__(self, selected_dive_idx: int = 0) -> None:
        self.__time_data: list[float] = []
        self.__depth_data: list[float] = []
        self.__margin_start_time = 2

        # Select the dive to be parsed (in case of multiple dives in FIT file)
        self.__selected_dive_idx = selected_dive_idx
        # TODO: Add a check to see if the selected dive index is valid

    def parse(self, file_path: str) -> None:
        """
        A method to parse a FIT file containing depth data.
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
        except (TypeError, IndexError) as e:
            raise DiveLogFitInvalidFitFileError(
                f"Invalid FIT file: {file_path}, cannot identify FIT type."
            ) from e

        if file_type != "activity":
            raise DiveLogFitInvalidFitFileTypeError(
                f"Invalid FIT file type: You must import 'activity', not '{file_type}'"
            )

        dive_summary = []
        dive_summary_mesgs = messages.get("dive_summary_mesgs", [])

        for dive_summary_mesg in dive_summary_mesgs:
            if dive_summary_mesg.get("reference_mesg") != "lap":
                continue
            lap_idx = dive_summary_mesg.get("reference_index")
            lap_mesg = messages.get("lap_mesgs")[lap_idx]
            bottom_time = dive_summary_mesg.get("bottom_time")
            start_time = lap_mesg.get("start_time")
            end_time = math.ceil(start_time + bottom_time)
            dive_summary.append(
                {
                    "start_time": start_time,
                    "end_time": end_time,
                    "max_depth": dive_summary_mesg.get("max_depth"),
                    "avg_depth": dive_summary_mesg.get("avg_depth"),
                    "bottom_time": bottom_time,
                }
            )

        if not dive_summary:
            raise DiveLogFitDiveNotFoundError(
                f"Invalid FIT file: {file_path} does not contain any dive data"
            )

        if (
            self.__selected_dive_idx >= len(dive_summary)
            or self.__selected_dive_idx < 0
        ):
            raise DiveLogFitDiveNotFoundError(
                f"Invalid Dive Index: {self.__selected_dive_idx} is not a valid dive index"
            )

        records = messages.get("record_mesgs", [])
        first_timestamp = None

        for record in records:
            timestamp_now = cast(int, record.get("timestamp"))
            start_time = cast(
                int, dive_summary[self.__selected_dive_idx].get("start_time")
            )
            end_time = cast(int, dive_summary[self.__selected_dive_idx].get("end_time"))

            # Skip the records before the dive starts
            if timestamp_now < start_time - self.__margin_start_time:
                continue
            # After the dive ends, stop getting the depth data
            if timestamp_now > end_time:
                break

            if first_timestamp is None:
                first_timestamp = timestamp_now

            time = float(timestamp_now - first_timestamp)
            depth = cast(float, record.get("depth"))
            self.__time_data.append(time)
            self.__depth_data.append(depth)

            # If the depth is 0, the dive is considered to be ended
            if round(depth, 3) == 0:
                break

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

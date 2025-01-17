"""
This module contains the SuuntoFitParser class 
which is used to parse a Suunto FIT file from Suunto App
"""

from typing import cast, Union, Any
from datetime import datetime, timezone
from garmin_fit_sdk import Decoder, Stream

from depthviz.parsers.generic.generic_divelog_parser import DiveLogFileNotFoundError
from depthviz.parsers.generic.fit.fit_parser import (
    DiveLogFitParser,
    DiveLogFitInvalidFitFileError,
    DiveLogFitInvalidFitFileTypeError,
    DiveLogFitDiveNotFoundError,
)

# Constants
CUT_OFF_DEPTH = 1.5  # The depth which the dive is considered to have started or ended
LOWEST_MAX_DEPTH = 3  # The minimum depth for a dive to be considered valid


class SuuntoFitParser(DiveLogFitParser):
    """
    A class to parse a FIT file containing depth data.
    """

    def __init__(self, selected_dive_idx: int = -1) -> None:
        self.__time_data: list[float] = []
        self.__depth_data: list[float] = []

        # Select the dive to be parsed (in case of multiple dives in FIT file)
        self.__selected_dive_idx = selected_dive_idx

        # Internal variables for extracting dive logs
        self.__current_dive: dict[str, Any] = {}
        self.__descended: bool = False
        self.__ascended: bool = False

    def __reset_dive_state(self) -> None:
        """
        A method to reset the internal state of the dive extraction process.
        This is used to reset the state when a new dive is detected.
        """
        self.__current_dive = {}
        self.__descended = False
        self.__ascended = False

    def convert_fit_epoch_to_datetime(self, fit_epoch: int) -> str:
        """
        A method to convert the epoch time in the FIT file to a human-readable datetime string.
        """
        epoch = fit_epoch + 631065600
        return datetime.fromtimestamp(epoch, timezone.utc).strftime(
            "%Y-%m-%d %H:%M:%S (GMT)"
        )

    def select_dive(
        self, dive_summary: list[dict[str, Union[int, float, object]]]
    ) -> int:
        """
        A method to prompt the user to select a dive from the FIT file,
        if there are multiple dives in the file.
        """
        if len(dive_summary) == 1:
            return 0
        print("Multiple dives found in the FIT file. Please select a dive to import:\n")
        for idx, dive in enumerate(dive_summary):
            start_time = self.convert_fit_epoch_to_datetime(
                cast(int, dive.get("start_time"))
            )
            print(
                f"[{idx + 1}]: Dive {idx + 1}: Start Time: {start_time}, "
                f"Max Depth: {cast(float, dive.get('max_depth')):.1f}m, "
                f"Bottom Time: {cast(float, dive.get('bottom_time')):.1f}s"
            )
        try:
            selected_dive_idx = (
                int(
                    input(
                        f"\nEnter the dive number to import [1-{len(dive_summary)}]: "
                    )
                )
                - 1
            )
            print()
        except ValueError as e:
            raise DiveLogFitDiveNotFoundError(
                f"Invalid Dive: Please enter a number between 1 and {len(dive_summary)}"
            ) from e

        if selected_dive_idx >= len(dive_summary) or selected_dive_idx < 0:
            raise DiveLogFitDiveNotFoundError(
                f"Invalid Dive: Please enter a number between 1 and {len(dive_summary)}"
            )
        return selected_dive_idx

    def parse(self, file_path: str) -> None:
        """
        A method to parse a Suunto FIT file containing depth data.
        """
        messages = self.__read_fit_file(file_path)
        self.__validate_fit_file(messages, file_path)
        dive_summary = self.__extract_dive_logs(messages)
        self.__parse_selected_dive(dive_summary)

    def __read_fit_file(self, file_path: str) -> dict[str, Any]:
        """
        A method to read the FIT file and extract the messages from it.
        """
        try:
            stream = Stream.from_file(file_path)
            decoder = Decoder(stream)
            messages, errors = decoder.read(convert_datetimes_to_dates=False)
            if errors:
                raise errors[0]
            return cast(dict[str, Any], messages)
        except RuntimeError as e:
            raise DiveLogFitInvalidFitFileError(f"Invalid FIT file: {file_path}") from e
        except FileNotFoundError as e:
            raise DiveLogFileNotFoundError(f"File not found: {file_path}") from e

    def __validate_fit_file(self, messages: dict[str, Any], file_path: str) -> None:
        """
        A method to validate the FIT file by checking the FIT type and manufacturer.
        """
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

    def __extract_dive_logs(
        self, messages: dict[str, Any]
    ) -> list[dict[str, Union[int, float, object]]]:
        """
        A method to extract the dive logs from the records in the FIT file.
        """
        dive_summary = []
        raw_extracted_dive_logs: list[dict[str, Any]] = []
        records = messages.get("record_mesgs", [])

        # Used for comparing the depth values to detect the start and end of a dive
        previous_depth = 0
        previous_record = None

        for record in records:
            timestamp = record.get("timestamp")
            depth = record.get("depth")

            if depth > 0:
                # Create a new dive log if the depth is greater than 0 and the current dive is None
                if not self.__current_dive:
                    self.__current_dive = {
                        "data": [],
                        "max_depth": 0,
                    }
                    # Add the previous record that has been cut off to the current dive
                    if previous_record is not None:
                        self.__current_dive["data"].append(
                            {
                                "timestamp": previous_record.get("timestamp"),
                                "depth": previous_record.get("depth"),
                            }
                        )
                    raw_extracted_dive_logs.append(self.__current_dive)

                # Detect the start and end of a dive
                # It will not intervene with the data if the depth is more than the CUT_OFF_DEPTH
                if depth > CUT_OFF_DEPTH:
                    self.__descended = True
                if self.__descended and depth < CUT_OFF_DEPTH:
                    self.__ascended = True

                # Reset the dive state if:
                # 1. Diver descends and ascends without reaching the CUT_OFF_DEPTH
                # 2. After ascending past the CUT_OFF_DEPTH, the diver descends again
                # This is to filter out surface intervals and multiple dives in the same file
                if not self.__descended and depth < previous_depth:
                    self.__reset_dive_state()
                if self.__descended and self.__ascended and depth > previous_depth:
                    self.__reset_dive_state()

                # Add the depth data to the current dive if it passes the checks (not getting reset)
                if self.__current_dive:
                    self.__current_dive["data"].append(
                        {"timestamp": timestamp, "depth": depth}
                    )
                    self.__current_dive["max_depth"] = max(
                        self.__current_dive["max_depth"], depth
                    )

                # Save the previous depth for comparison
                previous_depth = depth
            else:
                # Reset the dive state if the depth is 0
                self.__reset_dive_state()
            # Save the previous record for adding to the next dive if it is cut off but valid
            previous_record = record

        # Dive summary contains the dive logs that are deeper than LOWEST_MAX_DEPTH
        for log in raw_extracted_dive_logs:
            if log["max_depth"] > LOWEST_MAX_DEPTH:
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
                "Invalid FIT file: does not contain any dive data "
                f"deeper than {LOWEST_MAX_DEPTH}m."
            )
        return dive_summary

    def __parse_selected_dive(self, dive_summary: list[dict[str, Any]]) -> None:
        """
        A method to parse the selected dive from the dive summary
        and save them as time and depth data.
        """
        # A prompt to select the dive if there are multiple dives in the FIT file
        if self.__selected_dive_idx == -1:
            self.__selected_dive_idx = self.select_dive(dive_summary)

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

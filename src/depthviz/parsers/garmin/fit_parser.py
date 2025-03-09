# Copyright (c) 2024 - 2025 Noppanut Ploywong (@noppanut15) <noppanut.connect@gmail.com>
# Apache License 2.0 (see LICENSE file or http://www.apache.org/licenses/LICENSE-2.0)


"""A module for parsing a FIT file containing depth data from Garmin dive computers."""

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


class GarminFitParser(DiveLogFitParser):
    """A class to parse a FIT file containing depth data."""

    def __init__(self, selected_dive_idx: int = -1, depth_mode: str = "raw") -> None:
        """Initializes the GarminFitParser object.

        Args:
            selected_dive_idx: The index of the dive to be parsed.
            depth_mode: The depth mode to use for parsing the FIT file.

        Note:
            If there are multiple dives in the FIT file, the user will be prompted to select a dive
            to import. The selected dive will be stored in the `__selected_dive_idx` attribute.
        """
        super().__init__(depth_mode=depth_mode)
        self.__margin_start_time = 2

        # Select the dive to be parsed (in case of multiple dives in FIT file)
        self.__selected_dive_idx = selected_dive_idx

    def convert_fit_epoch_to_datetime(self, fit_epoch: int) -> str:
        """Convert the epoch time in the FIT file to a human-readable datetime string.

        Note:
            The FIT epoch is not a standard Unix epoch.
            Must add 631065600 to the FIT epoch to convert it to a Unix epoch.

        Args:
            fit_epoch: The FIT epoch time in the FIT file.

        Returns:
            A human-readable datetime string in the format "%Y-%m-%d %H:%M:%S (GMT)".
        """
        epoch = fit_epoch + 631065600
        return datetime.fromtimestamp(epoch, timezone.utc).strftime(
            "%Y-%m-%d %H:%M:%S (GMT)"
        )

    def select_dive(self, dive_summary: list[dict[str, Union[int, float]]]) -> int:
        """Prompt the user to select a dive from the FIT file.

        Note:
            If there is only one dive in the FIT file, it will be automatically selected.

        Args:
            dive_summary: A list of dictionaries containing dive summary information.

        Returns:
            The index of the selected dive.
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
        """A method to parse a FIT file containing depth data.

        Args:
            file_path: Path to the FIT file containing depth data.

        Raises:
            DiveLogFitInvalidFitFileError: If the FIT file is invalid.
            DiveLogFileNotFoundError: If the FIT file is not found.
            DiveLogFitInvalidFitFileTypeError: If the FIT file type is invalid.
                (e.g., not 'activity')
            DiveLogFitDiveNotFoundError: If the dive data is not found in the FIT file.

        Note:
            The FIT file must contain 'activity' type data to be imported.
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

        # A prompt to select the dive if there are multiple dives in the FIT file
        if self.__selected_dive_idx == -1:
            self.__selected_dive_idx = self.select_dive(dive_summary)

        records = messages.get("record_mesgs", [])
        first_timestamp = None
        max_depth_reached = False

        for record in records:
            timestamp_now = cast(int, record.get("timestamp"))
            start_time = cast(
                int, dive_summary[self.__selected_dive_idx].get("start_time")
            )
            end_time = cast(int, dive_summary[self.__selected_dive_idx].get("end_time"))
            max_depth = cast(
                float, dive_summary[self.__selected_dive_idx].get("max_depth")
            )

            # Skip the records before the dive starts
            if timestamp_now < start_time - self.__margin_start_time:
                continue

            # Calculate the time and depth data
            if first_timestamp is None:
                first_timestamp = timestamp_now

            time = float(timestamp_now - first_timestamp)
            depth = cast(float, record.get("depth"))

            # After the dive ends, get the depth data until the current depth > the previous depth
            # This is to get all the depth data until the dive "actually" ends
            previous_depth = self.depth_data[-1] if self.depth_data else -1
            previous_time = self.time_data[-1] if self.time_data else -1
            if timestamp_now > end_time:
                if depth > previous_depth:
                    break
                # Avoid jummping too far ahead (not the current dive anymore)
                # Note: Garmin normally records the depth every 1s, otherwise the dive has ended.
                if time > previous_time + 2:
                    break

            # Append the time and depth data
            self.time_data.append(time)
            self.depth_data.append(depth)

            # Check if the max depth is reached to avoid stopping the dive too early
            if not max_depth_reached and math.floor(depth) == math.floor(max_depth):
                max_depth_reached = True

            # If the depth is 0 and the max depth is reached, stop getting the depth data
            if round(depth, 3) == 0 and max_depth_reached:
                break

        if not self.time_data or not self.depth_data:
            raise DiveLogFitDiveNotFoundError(
                f"Invalid Dive Data: Dive data not found in FIT file: {file_path}"
            )

        # Convert depth data according to the depth mode
        self.depth_mode_execute()

    def get_time_data(self) -> list[float]:
        """Returns the time data parsed from the FIT file.

        Returns:
            The time data parsed from the FIT file.
        """
        return self.time_data

    def get_depth_data(self) -> list[float]:
        """Returns the depth data parsed from the FIT file.

        Returns:
            The depth data parsed from the FIT file.
        """
        return self.depth_data

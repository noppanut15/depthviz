# Copyright (c) 2024 - 2025 Noppanut Ploywong (@noppanut15) <noppanut.connect@gmail.com>
# Apache License 2.0 (see LICENSE file or http://www.apache.org/licenses/LICENSE-2.0)


"""This module contains the ShearwaterXmlParser class.

The ShearwaterXmlParser class is used to parse a XML file containing depth data 
from a Shearwater dive computer.

Constants (related to the hydrostatic pressure calculation):
    WATER_DENSITY_FRESH: The water density value for freshwater in kg/m³.
    WATER_DENSITY_EN13319: The water density value for EN13319 standard in kg/m³.
    WATER_DENSITY_SALT: The water density value for saltwater in kg/m³.
    GRAVITY: The gravitational acceleration value in m/s².

Note:
    Depth is not measured directly. Dive computers measure pressure, and convert this to depth 
    based on an assumed density of water. Water density varies by type. 

    The weight of salts dissolved in saltwater make it heavier than freshwater. 

    If two dive computers are using different densities of water, 
    then their displayed depths will differ.

    The water type can be adjusted on the Shearwater Dive Computer. 

    In the System Setup->Mode Setup menu, the Salinity setting can be set to 
    Fresh, EN13319, or Salt.

    The EN13319 (European CE standard for dive computers) value is between fresh and salt 
    and is the default value. 
    The EN13319 value corresponds to a 10m increase in depth for pressure increase of 1 bar.

    The density value used for each setting is:

    Fresh Water = 1000kg/m³
    EN13319 = 1019.7 kg/m³ (to be precise, according to the EN13319 standard)
    Salt Water = 1030 kg/m³

    Reference: https://shearwater.com/pages/perdix-support
"""

import xml.etree.ElementTree as ET

from depthviz.parsers.generic.generic_divelog_parser import (
    DiveLogFileNotFoundError,
    InvalidTimeValueError,
    InvalidDepthValueError,
)

from depthviz.parsers.generic.xml.xml_parser import (
    DiveLogXmlParser,
    DiveLogXmlParserError,
    DiveLogXmlInvalidRootElementError,
    DiveLogXmlInvalidElementError,
    DiveLogXmlFileContentUnreadableError,
)


WATER_DENSITY_FRESH = 1000
WATER_DENSITY_EN13319 = 1019.7
WATER_DENSITY_SALT = 1030
GRAVITY = 9.80665


class InvalidSurfacePressureValueError(DiveLogXmlParserError):
    """Exception raised for invalid surface pressure values."""


class ShearwaterXmlParser(DiveLogXmlParser):
    """A class to parse a XML file containing depth data.

    Attributes:
        time_data: A list of time data parsed from the XML file.
        depth_data: A list of depth data parsed from the XML file.
        depth_mode: The depth mode setting for the depth data.
        __start_surface_pressure: The start surface pressure value.
        __water_density: The water density value for the hydrostatic pressure calculation.
        __depth_unit: The unit of the depth data. (mbar, m)
    """

    def __init__(self, salinity: str = "en13319", depth_mode: str = "raw") -> None:
        """Initializes the ShearwaterXmlParser with the specified salinity setting.

        Args:
            salinity: The salinity setting for the water density calculation.
                      Can be "fresh", "en13319", or "salt". Default is "en13319".
            depth_mode: The depth mode setting for the depth data.

        Raises:
            ValueError: If the salinity setting is invalid.
        """
        super().__init__(depth_mode=depth_mode)
        self.__start_surface_pressure: float = 0
        self.__water_density: float = WATER_DENSITY_EN13319
        salinity = salinity.lower()
        if salinity == "salt":
            self.__water_density = WATER_DENSITY_SALT
        elif salinity == "fresh":
            self.__water_density = WATER_DENSITY_FRESH
        elif salinity != "en13319":
            raise ValueError(
                "Invalid salinity setting: Must be 'fresh', 'en13319', or 'salt'"
            )
        self.__depth_unit: str = ""

    def __get_dive_log(self, file_path: str) -> ET.Element:
        """Returns the dive log element from the XML root.

        Args:
            file_path: Path to the XML file containing depth data.

        Returns:
            The dive log element from the XML root.

        Raises:
            DiveLogXmlInvalidRootElementError: If the root element is not 'dive'.
            DiveLogFileNotFoundError: If the file is not found.
            DiveLogXmlFileContentUnreadableError: If the file content is unreadable.
        """
        try:
            root = ET.parse(file_path, parser=ET.XMLParser(encoding="utf-8")).getroot()
            if root.tag != "dive":
                raise DiveLogXmlInvalidRootElementError(
                    "Invalid XML: Target root not found"
                )
            dive_log = root.find("diveLog")
            if dive_log is None:
                raise DiveLogXmlInvalidElementError("Invalid XML: Dive log not found")
        except FileNotFoundError as e:
            raise DiveLogFileNotFoundError(
                f"Invalid XML: File not found: {file_path}"
            ) from e
        except ET.ParseError as e:
            raise DiveLogXmlFileContentUnreadableError(
                "Invalid XML: File content unreadable"
            ) from e
        return dive_log

    def __get_dive_log_records(self, dive_log: ET.Element) -> ET.Element:
        """Returns the dive log records element from the dive log.

        Args:
            dive_log: The dive log element from the XML root.

        Returns:
            The dive log records element from the dive log.

        Raises:
            DiveLogXmlInvalidElementError: If required elements are not found.
        """
        dive_log_records = dive_log.find("diveLogRecords")
        if dive_log_records is None:
            raise DiveLogXmlInvalidElementError(
                "Invalid XML: Dive log records not found"
            )
        return dive_log_records

    def __set_start_surface_pressure(self, dive_log: ET.Element) -> None:
        """Sets the start surface pressure value.

        Args:
            dive_log: The dive log element from the XML root.

        Raises:
            DiveLogXmlInvalidElementError: If required elements are not found.
            InvalidSurfacePressureValueError: If the surface pressure value is invalid
        """
        try:
            start_surface_pressure = dive_log.find("startSurfacePressure")
            if start_surface_pressure is None:
                raise DiveLogXmlInvalidElementError(
                    "Invalid XML: Start surface pressure not found"
                )
            self.__start_surface_pressure = float(str(start_surface_pressure.text))
        except ValueError as e:
            raise InvalidSurfacePressureValueError(
                "Invalid XML: Invalid start surface pressure value"
            ) from e

    def __find_depth_meter(self, mbar_pressure: float, water_density: float) -> float:
        """Calculates the depth in meters based on the hydrostatic pressure.

        Args:
            mbar_pressure: The pressure in millibars.
            water_density: The water density in kg/m³.

        Returns:
            The depth in meters based on the hydrostatic pressure.
        """
        pascal_pressure = mbar_pressure * 100
        return pascal_pressure / (water_density * GRAVITY)

    def __get_current_time(self, dive_log_record: ET.Element) -> float:
        """Returns the current time (in seconds) from the dive log record.

        Args:
            dive_log_record: The dive log record element.

        Returns:
            The current time in seconds

        Raises:
            DiveLogXmlInvalidElementError: If required elements are not found.
            InvalidTimeValueError: If time values are invalid.
        """
        try:
            current_time = dive_log_record.find("currentTime")
            if current_time is None:
                raise DiveLogXmlInvalidElementError("Invalid XML: Time not found")
            msec_time = float(str(current_time.text))
            time = msec_time / 1000
            return time
        except ValueError as e:
            raise InvalidTimeValueError("Invalid XML: Invalid time values") from e

    def __get_current_depth(self, dive_log_record: ET.Element) -> float:
        """Returns the current depth (in meters) from the dive log record.

        Args:
            dive_log_record: The dive log record element.

        Returns:
            The current depth in meters.

        Raises:
            DiveLogXmlInvalidElementError: If required elements are not found.
            InvalidDepthValueError: If depth values are invalid.
        """
        try:
            current_depth_txt = dive_log_record.find("currentDepth")
            if current_depth_txt is None:
                raise DiveLogXmlInvalidElementError("Invalid XML: Depth not found")
            current_depth = float(str(current_depth_txt.text))
        except ValueError as e:
            raise InvalidDepthValueError("Invalid XML: Invalid depth values") from e

        # Get the unit of the depth data
        # If the depth unit is not set, determine the unit based on the current depth value
        if self.__depth_unit == "":
            # If the current depth is greater than 500, assume the unit is in millibars
            # Note: The lowest atmospheric pressure is around 870 mbar
            if current_depth > 500:
                self.__depth_unit = "mbar"
            else:
                self.__depth_unit = "m"

        # Convert the depth value to meters if the unit is in millibars
        if self.__depth_unit == "mbar":
            # Calculate the hydrostatic pressure by subtracting the current pressure
            # (absolute pressure) from the start surface pressure, return 0 if negative
            mbar_hydrostatic_pressure = max(
                current_depth - self.__start_surface_pressure, 0
            )
            # Find the depth in meters based on the hydrostatic pressure formula
            depth_meter = self.__find_depth_meter(
                mbar_hydrostatic_pressure, self.__water_density
            )
        else:
            depth_meter = current_depth
        return depth_meter

    def parse(self, file_path: str) -> None:
        """Parses a XML file containing depth data.

        Args:
            file_path: Path to the XML file containing depth data.

        Raises:
            DiveLogFileNotFoundError: If the file is not found.
            DiveLogXmlFileContentUnreadableError: If the file content is unreadable.
            DiveLogXmlInvalidRootElementError: If the root element is not 'dive'.
            DiveLogXmlInvalidElementError: If required elements are not found.
            InvalidSurfacePressureValueError: If the surface pressure value is invalid.
            InvalidTimeValueError: If time values are invalid.
            InvalidDepthValueError: If depth values are invalid.
        """
        # Get the dive log element from the XML root
        dive_log = self.__get_dive_log(file_path)

        # Set the start surface pressure value
        self.__set_start_surface_pressure(dive_log)

        # Get the dive log records element from the dive log
        dive_log_records = self.__get_dive_log_records(dive_log)

        # Save the time and depth data from each sampling log record
        for dive_log_record in dive_log_records:
            time = self.__get_current_time(dive_log_record)
            depth_meter = self.__get_current_depth(dive_log_record)
            self.time_data.append(time)
            self.depth_data.append(round(depth_meter, 2))

        # Convert depth data according to the depth mode
        self.depth_mode_execute()

    def get_time_data(self) -> list[float]:
        """Returns the time data parsed from the XML file.

        Returns:
            The time data parsed from the XML file.
        """
        return self.time_data

    def get_depth_data(self) -> list[float]:
        """Returns the depth data parsed from the XML file.

        Returns:
            The depth data parsed from the XML file.
        """
        return self.depth_data

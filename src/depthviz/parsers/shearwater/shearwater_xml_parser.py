"""
This module contains the ShearwaterXmlParser class 
which is used to parse a XML file from the Shearwater Cloud.
===============================================================================

Depth is not measured directly. Dive computers measure pressure, and convert this to depth 
based on an assumed density of water. Water density varies by type. 

The weight of salts dissolved in saltwater make it heavier than freshwater. 

If two dive computers are using different densities of water, 
then their displayed depths will differ.

The water type can be adjusted on the Shearwater Dive Computer. 

In the System Setup->Mode Setup menu, the Salinity setting can be set to Fresh, EN13319, or Salt.

The EN13319 (European CE standard for dive computers) value is between fresh and salt 
and is the default value. 
The EN13319 value corresponds to a 10m increase in depth for pressure increase of 1 bar.

The density value used for each setting is:

Fresh Water = 1000kg/m³
EN13319 = 1020 kg/m³
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

# Constants related to the hydrostatic pressure calculation
WATER_DENSITY_FRESH = 1000
WATER_DENSITY_EN13319 = 1019.7  # To be precise to the EN13319 standard
WATER_DENSITY_SALT = 1030
GRAVITY = 9.80665


class InvalidSurfacePressureValueError(DiveLogXmlParserError):
    """Exception raised for invalid surface pressure values."""


class ShearwaterXmlParser(DiveLogXmlParser):
    """
    A class to parse a XML file containing depth data.

    Attributes:
        __time_data: A list of time data parsed from the XML file.
        __depth_data: A list of depth data parsed from the XML file.
        __start_surface_pressure: The start surface pressure value.
        __water_density: The water density value used for the hydrostatic pressure calculation
    Methods:
        __init__(salinity: str = "en13319") -> None:
            Initializes the ShearwaterXmlParser with the specified salinity setting.
        __get_dive_log(file_path: str) -> ET.Element:
            Returns the dive log element from the XML root.
        __get_dive_log_records(dive_log: ET.Element) -> ET.Element:
            Returns the dive log records element from the dive log.
        __set_start_surface_pressure(dive_log: ET.Element) -> None:
            Sets the start surface pressure value.
        __find_depth_meter(mbar_pressure: float, water_density: float) -> float:
            Calculates the depth in meters based on the hydrostatic pressure.
        __get_current_time(dive_log_record: ET.Element) -> float:
            Returns the current time (in seconds) from the dive log record.
        __get_current_depth(dive_log_record: ET.Element) -> float:
            Returns the current depth (in meters) from the dive log record.
        parse(file_path: str) -> None:
            Parses a XML file containing depth data.
        get_time_data() -> list[float]:
            Returns the time data parsed from the XML file.
        get_depth_data() -> list[float]:
            Returns the depth data parsed from the XML file.
    """

    def __init__(self, salinity: str = "en13319") -> None:
        """
        Initializes the ShearwaterXmlParser with the specified salinity setting.
        Args:
            salinity: The salinity setting for the water density calculation.
                      Can be "fresh", "en13319", or "salt". Default is "en13319".
        Raises:
            ValueError: If the salinity setting is invalid.
        """
        self.__time_data: list[float] = []
        self.__depth_data: list[float] = []
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

    def __get_dive_log(self, file_path: str) -> ET.Element:
        """
        Returns the dive log element from the XML root.
        Args:
            file_path: Path to the XML file containing depth data.
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
        """
        Returns the dive log records element from the dive log.
        Args:
            dive_log: The dive log element from the XML root.
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
        """
        Sets the start surface pressure value.
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
        """
        Calculates the depth in meters based on the hydrostatic pressure.
        Args:
            mbar_pressure: The pressure in millibars.
            water_density: The water density in kg/m³.
        """
        pascal_pressure = mbar_pressure * 100
        return pascal_pressure / (water_density * GRAVITY)

    def __get_current_time(self, dive_log_record: ET.Element) -> float:
        """
        Returns the current time (in seconds) from the dive log record.
        Args:
            dive_log_record: The dive log record element.
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
        """
        Returns the current depth (in meters) from the dive log record.
        Args:
            dive_log_record: The dive log record element.
        Raises:
            DiveLogXmlInvalidElementError: If required elements are not found.
            InvalidDepthValueError: If depth values are invalid.
        """
        try:
            current_depth = dive_log_record.find("currentDepth")
            if current_depth is None:
                raise DiveLogXmlInvalidElementError("Invalid XML: Depth not found")
            mbar_absolute_pressure = float(str(current_depth.text))
        except ValueError as e:
            raise InvalidDepthValueError("Invalid XML: Invalid depth values") from e

        # Calculate the hydrostatic pressure by subtracting the current pressure
        # from the start surface pressure, return 0 if negative
        mbar_hydrostatic_pressure = max(
            mbar_absolute_pressure - self.__start_surface_pressure, 0
        )
        # Find the depth in meters based on the hydrostatic pressure formula
        depth_meter = self.__find_depth_meter(
            mbar_hydrostatic_pressure, self.__water_density
        )
        return depth_meter

    def parse(self, file_path: str) -> None:
        """
        Parses a XML file containing depth data.
        Args:
            file_path: Path to the XML file containing depth data.
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
            self.__time_data.append(time)
            self.__depth_data.append(round(depth_meter, 2))

    def get_time_data(self) -> list[float]:
        """
        Returns the time data parsed from the XML file.
        Returns:
            The time data parsed from the XML file.
        """
        return self.__time_data

    def get_depth_data(self) -> list[float]:
        """
        Returns the depth data parsed from the XML file.
        Returns:
            The depth data parsed from the XML file.
        """
        return self.__depth_data

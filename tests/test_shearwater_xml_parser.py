# Copyright (c) 2024 - 2025 Noppanut Ploywong (@noppanut15) <noppanut.connect@gmail.com>
# Apache License 2.0 (see LICENSE file or http://www.apache.org/licenses/LICENSE-2.0)


"""
Unit tests for the ShearwaterXmlParser class.
"""

import os
from unittest.mock import patch, Mock
import pytest
from depthviz.parsers.shearwater.shearwater_xml_parser import (
    ShearwaterXmlParser,
    InvalidSurfacePressureValueError,
)
from depthviz.parsers.generic.generic_divelog_parser import (
    DiveLogFileNotFoundError,
    InvalidTimeValueError,
    InvalidDepthValueError,
)

from depthviz.parsers.generic.xml.xml_parser import (
    DiveLogXmlInvalidRootElementError,
    DiveLogXmlInvalidElementError,
    DiveLogXmlFileContentUnreadableError,
)


class TestShearwaterXmlParser:
    """
    Test class for the ShearwaterXmlParser
    """

    def test_parse_valid_xml_salinity_salt(
        self, request: pytest.FixtureRequest
    ) -> None:
        """
        Test parsing a valid XML file.
        """
        file_path = str(
            request.path.parent.joinpath(
                "data", "shearwater", "valid_depth_data_trimmed.xml"
            )
        )
        xml_parser = ShearwaterXmlParser(salinity="salt")
        xml_parser.parse(file_path)
        assert xml_parser.get_depth_data() == [
            0.76,
            1.22,
            2.58,
            3.25,
            3.14,
            3.68,
            5.0,
            6.31,
            6.27,
            6.76,
        ]
        assert xml_parser.get_time_data() == [
            0.0,
            1.0,
            2.0,
            3.0,
            4.0,
            5.0,
            6.0,
            7.0,
            8.0,
            9.0,
        ]

    def test_parse_valid_xml_salinity_fresh(
        self, request: pytest.FixtureRequest
    ) -> None:
        """
        Test parsing a valid XML file.
        """
        file_path = str(
            request.path.parent.joinpath(
                "data", "shearwater", "valid_depth_data_trimmed.xml"
            )
        )
        xml_parser = ShearwaterXmlParser(salinity="fresh")
        xml_parser.parse(file_path)
        assert xml_parser.get_depth_data() == [
            0.79,
            1.25,
            2.66,
            3.34,
            3.23,
            3.79,
            5.15,
            6.5,
            6.45,
            6.96,
        ]
        assert xml_parser.get_time_data() == [
            0.0,
            1.0,
            2.0,
            3.0,
            4.0,
            5.0,
            6.0,
            7.0,
            8.0,
            9.0,
        ]

    def test_parse_valid_xml_salinity_en13319(
        self, request: pytest.FixtureRequest
    ) -> None:
        """
        Test parsing a valid XML file.
        """
        file_path = str(
            request.path.parent.joinpath(
                "data", "shearwater", "valid_depth_data_trimmed.xml"
            )
        )
        xml_parser = ShearwaterXmlParser(salinity="en13319")
        xml_parser.parse(file_path)
        assert xml_parser.get_depth_data() == [
            0.77,
            1.23,
            2.61,
            3.28,
            3.17,
            3.72,
            5.05,
            6.37,
            6.33,
            6.83,
        ]
        assert xml_parser.get_time_data() == [
            0.0,
            1.0,
            2.0,
            3.0,
            4.0,
            5.0,
            6.0,
            7.0,
            8.0,
            9.0,
        ]

    def test_parse_invalid_xml_x_element_start_surface_pressure(
        self, request: pytest.FixtureRequest
    ) -> None:
        """
        Test parsing a XML file with an invalid startSurfacePressure element.
        """
        file_path = str(
            request.path.parent.joinpath(
                "data",
                "shearwater",
                "invalid_data_x_element_start_surface_pressure.xml",
            )
        )
        xml_parser = ShearwaterXmlParser()
        with pytest.raises(DiveLogXmlInvalidElementError) as e:
            xml_parser.parse(file_path)
        assert str(e.value) == "Invalid XML: Start surface pressure not found"

    def test_parse_invalid_xml_x_element_root(
        self, request: pytest.FixtureRequest
    ) -> None:
        """
        Test parsing a XML file with an invalid root element.
        """
        file_path = str(
            request.path.parent.joinpath(
                "data",
                "shearwater",
                "invalid_data_x_element_root.xml",
            )
        )
        xml_parser = ShearwaterXmlParser()
        with pytest.raises(DiveLogXmlInvalidRootElementError) as e:
            xml_parser.parse(file_path)
        assert str(e.value) == "Invalid XML: Target root not found"

    def test_parse_invalid_xml_x_element_time(
        self, request: pytest.FixtureRequest
    ) -> None:
        """
        Test parsing a XML file with an invalid time element.
        """
        file_path = str(
            request.path.parent.joinpath(
                "data",
                "shearwater",
                "invalid_data_x_element_time.xml",
            )
        )
        xml_parser = ShearwaterXmlParser()
        with pytest.raises(DiveLogXmlInvalidElementError) as e:
            xml_parser.parse(file_path)
        assert str(e.value) == "Invalid XML: Time not found"

    def test_parse_invalid_xml_x_element_depth(
        self, request: pytest.FixtureRequest
    ) -> None:
        """
        Test parsing a XML file with an invalid depth element.
        """
        file_path = str(
            request.path.parent.joinpath(
                "data",
                "shearwater",
                "invalid_data_x_element_depth.xml",
            )
        )
        xml_parser = ShearwaterXmlParser()
        with pytest.raises(DiveLogXmlInvalidElementError) as e:
            xml_parser.parse(file_path)

        assert str(e.value) == "Invalid XML: Depth not found"

    def test_parse_invalid_xml_x_value_start_surface_pressure(
        self, request: pytest.FixtureRequest
    ) -> None:
        """
        Test parsing a XML file with an invalid startSurfacePressure value.
        """
        file_path = str(
            request.path.parent.joinpath(
                "data",
                "shearwater",
                "invalid_data_x_value_start_surface_pressure.xml",
            )
        )
        xml_parser = ShearwaterXmlParser()
        with pytest.raises(InvalidSurfacePressureValueError) as e:
            xml_parser.parse(file_path)

        assert str(e.value) == "Invalid XML: Invalid start surface pressure value"

    def test_parse_invalid_xml_x_value_time(
        self, request: pytest.FixtureRequest
    ) -> None:
        """
        Test parsing a XML file with an invalid time value.
        """
        file_path = str(
            request.path.parent.joinpath(
                "data",
                "shearwater",
                "invalid_data_x_value_time.xml",
            )
        )
        xml_parser = ShearwaterXmlParser()
        with pytest.raises(InvalidTimeValueError) as e:
            xml_parser.parse(file_path)

        assert str(e.value) == "Invalid XML: Invalid time values"

    def test_parse_invalid_xml_x_value_depth(
        self, request: pytest.FixtureRequest
    ) -> None:
        """
        Test parsing a XML file with an invalid depth value.
        """
        file_path = str(
            request.path.parent.joinpath(
                "data",
                "shearwater",
                "invalid_data_x_value_depth.xml",
            )
        )
        xml_parser = ShearwaterXmlParser()
        with pytest.raises(InvalidDepthValueError) as e:
            xml_parser.parse(file_path)

        assert str(e.value) == "Invalid XML: Invalid depth values"

    def test_parse_invalid_xml_missing_file(
        self, request: pytest.FixtureRequest
    ) -> None:
        """
        Test parsing a missing XML file.
        """
        file_path = str(
            request.path.parent.joinpath(
                "data",
                "shearwater",
                "missing_file_xyz.xml",
            )
        )
        xml_parser = ShearwaterXmlParser()
        assert not os.path.exists(file_path)
        with pytest.raises(DiveLogFileNotFoundError) as e:
            xml_parser.parse(file_path)
        assert str(e.value) == f"Invalid XML: File not found: {file_path}"

    def test_parse_empty_xml(self, request: pytest.FixtureRequest) -> None:
        """
        Test parsing an empty XML file.
        """
        file_path = str(
            request.path.parent.joinpath(
                "data",
                "shearwater",
                "invalid_empty_file.xml",
            )
        )
        xml_parser = ShearwaterXmlParser()
        with pytest.raises(DiveLogXmlFileContentUnreadableError) as e:
            xml_parser.parse(file_path)
        assert str(e.value) == "Invalid XML: File content unreadable"

    def test_parse_invalid_xml_missing_divelog(
        self, request: pytest.FixtureRequest
    ) -> None:
        """
        Test parsing a XML file with missing diveLog element.
        """
        file_path = str(
            request.path.parent.joinpath(
                "data",
                "shearwater",
                "invalid_data_x_element_divelog.xml",
            )
        )
        xml_parser = ShearwaterXmlParser()
        with pytest.raises(DiveLogXmlInvalidElementError) as e:
            xml_parser.parse(file_path)
        assert str(e.value) == "Invalid XML: Dive log not found"

    def test_parse_invalid_missing_divelog_records(
        self, request: pytest.FixtureRequest
    ) -> None:
        """
        Test parsing a XML file with missing diveLogRecords element.
        """
        file_path = str(
            request.path.parent.joinpath(
                "data",
                "shearwater",
                "invalid_data_x_element_divelog_records.xml",
            )
        )
        xml_parser = ShearwaterXmlParser()
        with pytest.raises(DiveLogXmlInvalidElementError) as e:
            xml_parser.parse(file_path)
        assert str(e.value) == "Invalid XML: Dive log records not found"

    def test_invalid_salinity(self) -> None:
        """
        Test parsing a XML file with invalid salinity.
        """
        with pytest.raises(ValueError) as e:
            ShearwaterXmlParser(salinity="invalid")
        assert (
            str(e.value)
            == "Invalid salinity setting: Must be 'fresh', 'en13319', or 'salt'"
        )

    @pytest.mark.parametrize("depth_mode", ["raw", "zero-based"])
    @patch(
        "depthviz.parsers.shearwater.shearwater_xml_parser.ShearwaterXmlParser.depth_mode_execute"
    )
    def test_parse_valid_xml_depth_mode_exec(
        self,
        mock_depth_mode_execute: Mock,
        depth_mode: str,
        request: pytest.FixtureRequest,
    ) -> None:
        """
        Test parsing a valid XML file with depth mode execution.
        """
        file_path = str(
            request.path.parent.joinpath(
                "data",
                "shearwater",
                "valid_depth_data_trimmed.xml",
            )
        )
        parser = ShearwaterXmlParser(depth_mode=depth_mode)
        parser.parse(file_path)
        mock_depth_mode_execute.assert_called_once()

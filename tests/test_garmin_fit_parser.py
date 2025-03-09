# Copyright (c) 2024 - 2025 Noppanut Ploywong (@noppanut15) <noppanut.connect@gmail.com>
# Apache License 2.0 (see LICENSE file or http://www.apache.org/licenses/LICENSE-2.0)


"""Unit tests for the GarminFitParser class."""

from typing import Any, Union
from unittest.mock import patch, Mock
import pytest
from garmin_fit_sdk import Stream, Decoder
from depthviz.parsers.garmin.fit_parser import GarminFitParser
from depthviz.parsers.generic.fit.fit_parser import (
    DiveLogFitInvalidFitFileError,
    DiveLogFitInvalidFitFileTypeError,
    DiveLogFitDiveNotFoundError,
)
from depthviz.parsers.generic.generic_divelog_parser import (
    DiveLogFileNotFoundError,
)


class TestGarminFitParser:
    """Test class for the GarminFitParser."""

    def _mock_stream_from_file(self, _: Any) -> None:
        """A mock function for the Stream.from_file method."""

    def _mock_decoder_init(
        self,
        *args: Union[str, bool],
        **kwargs: Union[str, bool],
    ) -> None:
        """A mock function for the Decoder.__init__ method."""

    @pytest.mark.parametrize(
        "file_path, selected_dive_idx, expected_time_data, expected_depth_data",
        [
            # 21.89m dive (27/05/2023 13:44:16)
            (
                "11211432883_ACTIVITY.fit",
                0,
                [
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
                    10.0,
                    11.0,
                    12.0,
                    13.0,
                    14.0,
                    15.0,
                    16.0,
                    17.0,
                    18.0,
                    19.0,
                    20.0,
                    21.0,
                    22.0,
                    23.0,
                    24.0,
                    33.0,
                    34.0,
                    35.0,
                    36.0,
                    37.0,
                    38.0,
                    39.0,
                    40.0,
                    41.0,
                    42.0,
                    43.0,
                    44.0,
                    45.0,
                    46.0,
                    47.0,
                    48.0,
                    49.0,
                    50.0,
                    51.0,
                    52.0,
                    53.0,
                    54.0,
                    55.0,
                    56.0,
                    57.0,
                    58.0,
                    59.0,
                    60.0,
                    61.0,
                    62.0,
                    63.0,
                ],
                [
                    1.974,
                    2.816,
                    3.634,
                    4.457,
                    5.382,
                    6.352,
                    7.27,
                    8.191,
                    9.176,
                    10.145,
                    11.112,
                    12.124,
                    13.102,
                    14.083,
                    15.083,
                    16.011,
                    17.028,
                    18.044,
                    18.983,
                    19.919,
                    20.634,
                    21.004,
                    21.341,
                    21.529,
                    21.751,
                    21.513,
                    20.769,
                    20.073,
                    19.341,
                    18.584,
                    17.888,
                    17.228,
                    16.563,
                    15.902,
                    15.291,
                    14.634,
                    13.993,
                    13.313,
                    12.607,
                    11.908,
                    11.28,
                    10.612,
                    9.907,
                    9.219,
                    8.482,
                    7.785,
                    7.02,
                    5.815,
                    4.654,
                    3.702,
                    2.868,
                    2.101,
                    1.333,
                    0.556,
                    0.342,
                    0,
                ],
            ),
            # 28.62m dive (27/05/2023 14:16:16)
            (
                "11211432883_ACTIVITY.fit",
                1,
                [
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
                    10.0,
                    11.0,
                    12.0,
                    13.0,
                    14.0,
                    15.0,
                    16.0,
                    17.0,
                    18.0,
                    19.0,
                    20.0,
                    21.0,
                    22.0,
                    23.0,
                    24.0,
                    25.0,
                    26.0,
                    27.0,
                    28.0,
                    29.0,
                    30.0,
                    31.0,
                    34.0,
                    35.0,
                    36.0,
                    37.0,
                    38.0,
                    39.0,
                    40.0,
                    41.0,
                    42.0,
                    43.0,
                    44.0,
                    45.0,
                    46.0,
                    47.0,
                    48.0,
                    49.0,
                    50.0,
                    51.0,
                    52.0,
                    53.0,
                    54.0,
                    55.0,
                    56.0,
                    57.0,
                    58.0,
                    59.0,
                    60.0,
                    61.0,
                    62.0,
                    63.0,
                    64.0,
                    65.0,
                    66.0,
                    67.0,
                    68.0,
                    69.0,
                    70.0,
                ],
                [
                    1.3,
                    1.799,
                    2.538,
                    3.41,
                    4.32,
                    5.227,
                    6.143,
                    7.127,
                    8.129,
                    9.085,
                    10.059,
                    11.025,
                    12.035,
                    13.092,
                    14.129,
                    15.181,
                    16.199,
                    17.186,
                    17.978,
                    18.62,
                    19.43,
                    20.403,
                    21.45,
                    22.501,
                    23.43,
                    24.388,
                    25.356,
                    26.456,
                    26.933,
                    27.596,
                    28.222,
                    28.538,
                    28.005,
                    27.15,
                    26.283,
                    25.468,
                    24.664,
                    23.842,
                    23.008,
                    22.224,
                    21.389,
                    20.592,
                    19.759,
                    19.002,
                    18.241,
                    17.503,
                    16.779,
                    16.047,
                    15.308,
                    14.547,
                    13.821,
                    13.112,
                    12.408,
                    11.654,
                    10.877,
                    10.131,
                    9.368,
                    8.618,
                    7.849,
                    7.048,
                    5.929,
                    4.662,
                    3.831,
                    3.201,
                    2.592,
                    1.977,
                    1.341,
                    0.655,
                    0.003,
                ],
            ),
            # 4.28m dive (21/02/2024 11:05:15)
            (
                "14087156326_ACTIVITY.fit",
                0,
                [
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
                    10.0,
                    11.0,
                    12.0,
                    13.0,
                    14.0,
                    15.0,
                    16.0,
                    17.0,
                    18.0,
                    19.0,
                    20.0,
                    21.0,
                    22.0,
                ],
                [
                    1.201,
                    1.41,
                    1.546,
                    1.707,
                    1.87,
                    2.186,
                    2.492,
                    2.74,
                    2.995,
                    3.173,
                    3.349,
                    3.54,
                    3.745,
                    4.278,
                    4.248,
                    3.717,
                    3.253,
                    2.6,
                    1.907,
                    1.208,
                    0.383,
                    0.165,
                    0.054,
                ],
            ),
            # 7.19m dive (21/02/2024 11:06:59)
            (
                "14087156326_ACTIVITY.fit",
                1,
                [
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
                    10.0,
                    11.0,
                    12.0,
                    13.0,
                    14.0,
                    15.0,
                    16.0,
                    20.0,
                    21.0,
                    22.0,
                    27.0,
                    30.0,
                    31.0,
                    32.0,
                    33.0,
                    34.0,
                    35.0,
                    36.0,
                    37.0,
                    38.0,
                    39.0,
                    40.0,
                    41.0,
                    42.0,
                    43.0,
                    44.0,
                    46.0,
                ],
                [
                    1.192,
                    1.752,
                    2.382,
                    3.11,
                    3.74,
                    4.335,
                    4.813,
                    5.314,
                    5.438,
                    5.332,
                    5.655,
                    5.918,
                    6.121,
                    6.318,
                    6.468,
                    6.741,
                    6.852,
                    6.889,
                    6.941,
                    6.999,
                    7.171,
                    6.935,
                    6.758,
                    6.398,
                    6.079,
                    5.695,
                    5.149,
                    4.71,
                    4.085,
                    3.775,
                    3.231,
                    2.739,
                    2.111,
                    1.559,
                    0.818,
                    0.219,
                    0.023,
                ],
            ),
            # 11.35m dive (21/02/2024 11:08:44)
            (
                "14087156326_ACTIVITY.fit",
                2,
                [
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
                    10.0,
                    11.0,
                    12.0,
                    13.0,
                    14.0,
                    15.0,
                    16.0,
                    17.0,
                    18.0,
                    19.0,
                    20.0,
                    21.0,
                    22.0,
                    23.0,
                    24.0,
                    25.0,
                    26.0,
                    27.0,
                    28.0,
                    29.0,
                    30.0,
                    31.0,
                    32.0,
                    33.0,
                    34.0,
                    35.0,
                    37.0,
                    38.0,
                    39.0,
                    40.0,
                    41.0,
                    42.0,
                    43.0,
                    44.0,
                    45.0,
                    46.0,
                    47.0,
                    48.0,
                    49.0,
                    50.0,
                    51.0,
                    52.0,
                    53.0,
                ],
                [
                    1.696,
                    2.808,
                    3.645,
                    4.451,
                    5.348,
                    6.211,
                    7.005,
                    7.708,
                    8.22,
                    8.627,
                    8.942,
                    9.264,
                    9.515,
                    9.75,
                    9.947,
                    10.189,
                    10.52,
                    10.815,
                    11.056,
                    11.269,
                    11.349,
                    11.306,
                    11.124,
                    10.81,
                    10.648,
                    10.409,
                    10.33,
                    10.224,
                    10.375,
                    10.032,
                    10.24,
                    10.101,
                    10.135,
                    9.817,
                    9.341,
                    9.182,
                    9.049,
                    8.61,
                    8.018,
                    7.427,
                    6.815,
                    6.224,
                    5.744,
                    5.306,
                    4.867,
                    4.363,
                    3.856,
                    3.247,
                    2.593,
                    1.907,
                    1.226,
                    0.55,
                    0,
                ],
            ),
            # 9.68m dive (21/02/2024 11:10:44)
            (
                "14087156326_ACTIVITY.fit",
                3,
                [
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
                    10.0,
                    11.0,
                    12.0,
                    13.0,
                    14.0,
                    15.0,
                    16.0,
                    17.0,
                    18.0,
                    19.0,
                    20.0,
                    21.0,
                    22.0,
                    23.0,
                    24.0,
                    25.0,
                    26.0,
                    27.0,
                    28.0,
                    29.0,
                    30.0,
                    31.0,
                    32.0,
                    33.0,
                    34.0,
                ],
                [
                    0.833,
                    1.232,
                    2.172,
                    2.694,
                    3.225,
                    3.777,
                    4.28,
                    4.739,
                    5.2,
                    5.73,
                    6.19,
                    6.638,
                    7.106,
                    7.557,
                    8.027,
                    8.53,
                    9.01,
                    9.472,
                    9.673,
                    9.882,
                    9.579,
                    9.688,
                    9.472,
                    9.412,
                    8.527,
                    7.677,
                    6.808,
                    6.058,
                    5.105,
                    4.282,
                    3.505,
                    2.456,
                    1.429,
                    0.693,
                    0,
                ],
            ),
            # 12.66m dive (21/02/2024 11:14:27)
            (
                "14087156326_ACTIVITY.fit",
                4,
                [
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
                    10.0,
                    11.0,
                    12.0,
                    13.0,
                    14.0,
                    15.0,
                    16.0,
                    17.0,
                    18.0,
                    19.0,
                    20.0,
                    21.0,
                    22.0,
                    23.0,
                    24.0,
                    25.0,
                    26.0,
                    28.0,
                    29.0,
                    31.0,
                    32.0,
                    33.0,
                    34.0,
                    35.0,
                    37.0,
                    38.0,
                    39.0,
                    40.0,
                    41.0,
                    42.0,
                    43.0,
                    45.0,
                    46.0,
                    47.0,
                    48.0,
                    49.0,
                    50.0,
                    51.0,
                    52.0,
                    53.0,
                    54.0,
                    55.0,
                    56.0,
                    57.0,
                    58.0,
                    59.0,
                    60.0,
                ],
                [
                    0.402,
                    1.447,
                    1.329,
                    2.013,
                    2.709,
                    3.536,
                    4.296,
                    5.078,
                    5.811,
                    6.511,
                    7.261,
                    7.951,
                    8.688,
                    9.306,
                    9.966,
                    10.595,
                    11.221,
                    11.578,
                    11.703,
                    12.078,
                    12.324,
                    12.413,
                    12.548,
                    12.604,
                    12.286,
                    12.265,
                    12.607,
                    12.662,
                    12.621,
                    12.307,
                    12.408,
                    12.348,
                    12.372,
                    12.496,
                    12.395,
                    12.286,
                    12.035,
                    11.789,
                    11.453,
                    11.178,
                    10.865,
                    10.544,
                    10.252,
                    9.913,
                    9.348,
                    8.61,
                    7.883,
                    7.125,
                    6.286,
                    5.369,
                    4.551,
                    3.807,
                    2.937,
                    1.971,
                    1.002,
                    0.244,
                    0,
                ],
            ),
            # 9.55m dive (21/02/2024 11:16:51)
            (
                "14087156326_ACTIVITY.fit",
                5,
                [
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
                    10.0,
                    11.0,
                    12.0,
                    13.0,
                    14.0,
                    16.0,
                    17.0,
                    19.0,
                    20.0,
                    21.0,
                    22.0,
                    23.0,
                    24.0,
                    25.0,
                    26.0,
                    27.0,
                    28.0,
                    29.0,
                    30.0,
                    31.0,
                ],
                [
                    0.686,
                    1.293,
                    1.748,
                    2.637,
                    3.44,
                    4.264,
                    5.038,
                    5.792,
                    6.429,
                    7.086,
                    7.864,
                    8.043,
                    8.575,
                    9.104,
                    9.375,
                    8.997,
                    8.76,
                    8.286,
                    7.711,
                    7.06,
                    6.998,
                    6.3,
                    5.423,
                    4.518,
                    4.009,
                    3.249,
                    2.183,
                    1.169,
                    0.304,
                    0,
                ],
            ),
            # 10.15m dive (21/02/2024 12:07:00)
            (
                "14087156326_ACTIVITY.fit",
                24,
                [
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
                    10.0,
                    11.0,
                    12.0,
                    13.0,
                    14.0,
                    15.0,
                    16.0,
                    17.0,
                    18.0,
                    19.0,
                    22.0,
                    23.0,
                    24.0,
                    25.0,
                    26.0,
                    27.0,
                    29.0,
                    30.0,
                    31.0,
                    32.0,
                    33.0,
                    34.0,
                    35.0,
                    37.0,
                    38.0,
                    39.0,
                    40.0,
                    41.0,
                    42.0,
                    43.0,
                    44.0,
                    45.0,
                    46.0,
                    47.0,
                    49.0,
                    50.0,
                    51.0,
                    52.0,
                    53.0,
                    54.0,
                    55.0,
                    56.0,
                    57.0,
                    58.0,
                    59.0,
                    60.0,
                    61.0,
                    62.0,
                    63.0,
                    64.0,
                    65.0,
                    66.0,
                    67.0,
                    68.0,
                    69.0,
                ],
                [
                    1.322,
                    1.512,
                    2.071,
                    2.644,
                    3.193,
                    3.812,
                    4.411,
                    4.951,
                    5.586,
                    6.111,
                    6.575,
                    6.982,
                    7.447,
                    7.879,
                    8.288,
                    8.585,
                    8.6,
                    9.112,
                    9.207,
                    9.237,
                    9.321,
                    9.529,
                    9.589,
                    9.588,
                    9.726,
                    9.847,
                    10.021,
                    10.099,
                    10.15,
                    10.155,
                    10.085,
                    9.86,
                    9.742,
                    9.474,
                    9.723,
                    9.598,
                    9.423,
                    9.54,
                    9.437,
                    9.211,
                    9.212,
                    9.176,
                    8.977,
                    8.731,
                    8.705,
                    8.523,
                    8.508,
                    8.35,
                    8.068,
                    7.83,
                    7.737,
                    7.543,
                    7.229,
                    6.822,
                    6.378,
                    5.649,
                    5.163,
                    4.793,
                    4.574,
                    3.892,
                    3.071,
                    2.377,
                    1.665,
                    0.893,
                    0,
                ],
            ),
            # 4.95m dive (21/02/2024 12:08:48)
            (
                "14087156326_ACTIVITY.fit",
                25,
                [
                    0.0,
                    1.0,
                    2.0,
                    3.0,
                    5.0,
                    6.0,
                    7.0,
                    8.0,
                    9.0,
                    10.0,
                    11.0,
                    12.0,
                    13.0,
                    14.0,
                    17.0,
                    18.0,
                    19.0,
                    20.0,
                    21.0,
                    22.0,
                    23.0,
                    24.0,
                    25.0,
                    26.0,
                    27.0,
                    28.0,
                    29.0,
                    30.0,
                    31.0,
                    32.0,
                    33.0,
                    34.0,
                    35.0,
                    36.0,
                    37.0,
                ],
                [
                    0.851,
                    1.648,
                    2.444,
                    2.841,
                    3.079,
                    3.296,
                    3.437,
                    3.426,
                    3.304,
                    3.72,
                    4.131,
                    4.288,
                    4.238,
                    4.196,
                    4.255,
                    4.497,
                    4.456,
                    4.586,
                    4.725,
                    4.767,
                    4.805,
                    4.74,
                    4.725,
                    4.619,
                    4.459,
                    4.47,
                    4.4,
                    4.175,
                    3.819,
                    3.341,
                    2.688,
                    1.735,
                    0.904,
                    0.164,
                    0,
                ],
            ),
            # 24.04m dive (09/03/2025 09:49:13)
            (
                "18478819822_ACTIVITY.fit",
                6,
                [
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
                    10.0,
                    11.0,
                    12.0,
                    13.0,
                    14.0,
                    15.0,
                    16.0,
                    17.0,
                    18.0,
                    19.0,
                    20.0,
                    21.0,
                    22.0,
                    23.0,
                    24.0,
                    25.0,
                    26.0,
                    27.0,
                    28.0,
                    29.0,
                    30.0,
                    31.0,
                    32.0,
                    33.0,
                    34.0,
                    35.0,
                    36.0,
                    37.0,
                    38.0,
                    39.0,
                    40.0,
                    41.0,
                    42.0,
                    43.0,
                    44.0,
                    45.0,
                    46.0,
                    47.0,
                    48.0,
                    49.0,
                    50.0,
                    51.0,
                    52.0,
                    53.0,
                    54.0,
                    55.0,
                    56.0,
                    57.0,
                    58.0,
                    59.0,
                    60.0,
                    61.0,
                    62.0,
                    63.0,
                    64.0,
                    65.0,
                    66.0,
                    67.0,
                    68.0,
                    69.0,
                    70.0,
                    # 71.0,
                    # 72.0,
                ],
                [
                    0,
                    0.285,
                    2.167,
                    2.836,
                    3.274,
                    3.58,
                    3.782,
                    3.645,
                    3.735,
                    4.277,
                    5.038,
                    5.799,
                    6.539,
                    7.181,
                    7.787,
                    8.35,
                    8.928,
                    9.483,
                    9.999,
                    10.623,
                    11.229,
                    11.866,
                    12.514,
                    13.17,
                    13.826,
                    14.503,
                    15.193,
                    15.882,
                    16.588,
                    17.326,
                    18.143,
                    18.832,
                    19.61,
                    20.404,
                    21.21,
                    22.028,
                    22.854,
                    23.538,
                    24.04,
                    24.016,
                    24.021,
                    23.99,
                    23.113,
                    21.943,
                    20.706,
                    19.755,
                    19.336,
                    19.485,
                    18.706,
                    17.696,
                    16.609,
                    15.369,
                    14.485,
                    14.174,
                    14.19,
                    13.333,
                    12.33,
                    11.149,
                    9.881,
                    8.977,
                    8.527,
                    8.353,
                    7.364,
                    6.15,
                    5.048,
                    3.783,
                    2.803,
                    2.18,
                    2.104,
                    1.193,
                    0.908,
                    # 0.084,
                    # 0.008,
                ],
            ),
        ],
    )
    def test_parse_valid_fit(
        self,
        request: pytest.FixtureRequest,
        file_path: str,
        selected_dive_idx: int,
        expected_time_data: list[float],
        expected_depth_data: list[float],
    ) -> None:
        """Test parsing a valid FIT file."""
        file_path = str(request.path.parent.joinpath("data", "garmin", file_path))
        fit_parser = GarminFitParser(selected_dive_idx=selected_dive_idx)
        fit_parser.parse(file_path)
        print(fit_parser.get_depth_data())
        assert fit_parser.get_time_data() == expected_time_data
        assert fit_parser.get_depth_data() == expected_depth_data

    def test_parse_invalid_fit(
        self,
        request: pytest.FixtureRequest,
    ) -> None:
        """Test parsing an invalid FIT file."""
        file_path = str(
            request.path.parent.joinpath("data", "garmin", "invalid_file.fit")
        )
        fit_parser = GarminFitParser()

        with pytest.raises(DiveLogFitInvalidFitFileError) as e:
            fit_parser.parse(file_path)
        assert str(e.value) == f"Invalid FIT file: {file_path}"

    def test_parse_invalid_fit_no_file_id_mesgs(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test parsing a FIT file with no file_id_mesgs."""

        def mock_decoder_read(
            *_args: Union[str, bool],
            **_kwargs: Union[str, bool],
        ) -> tuple[dict[str, list[Any]], list[Any]]:
            """A mock function for the Decoder.read method."""
            return {"file_id_mesgs": []}, []

        file_path = "mock"

        fit_parser = GarminFitParser()
        monkeypatch.setattr(Stream, "from_file", self._mock_stream_from_file)
        monkeypatch.setattr(Decoder, "__init__", self._mock_decoder_init)
        monkeypatch.setattr(Decoder, "read", mock_decoder_read)
        with pytest.raises(DiveLogFitInvalidFitFileError) as e:
            fit_parser.parse(file_path)
        assert (
            str(e.value) == f"Invalid FIT file: {file_path}, cannot identify FIT type."
        )

    def test_parse_invalid_fit_wrong_file_type(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test parsing a FIT file with the wrong file type."""

        def mock_decoder_read(
            *_args: Union[str, bool],
            **_kwargs: Union[str, bool],
        ) -> tuple[dict[str, list[Any]], list[Any]]:
            """A mock function for the Decoder.read method."""
            return {"file_id_mesgs": [{"type": "workout"}]}, []

        file_path = "mock"

        fit_parser = GarminFitParser()
        monkeypatch.setattr(Stream, "from_file", self._mock_stream_from_file)
        monkeypatch.setattr(Decoder, "__init__", self._mock_decoder_init)
        monkeypatch.setattr(Decoder, "read", mock_decoder_read)
        with pytest.raises(DiveLogFitInvalidFitFileTypeError) as e:
            fit_parser.parse(file_path)
        assert (
            str(e.value)
            == "Invalid FIT file type: You must import 'activity', not 'workout'"
        )

    def test_no_dive_summary_mesgs(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test parsing a FIT file with no dive_summary_mesgs."""

        def mock_decoder_read(
            *_args: Union[str, bool],
            **_kwargs: Union[str, bool],
        ) -> tuple[dict[str, list[Any]], list[Any]]:
            """A mock function for the Decoder.read method."""
            return {
                "file_id_mesgs": [{"type": "activity"}],
                "dive_summary_mesgs": [],
            }, []

        file_path = "mock"

        fit_parser = GarminFitParser()
        monkeypatch.setattr(Stream, "from_file", self._mock_stream_from_file)
        monkeypatch.setattr(Decoder, "__init__", self._mock_decoder_init)
        monkeypatch.setattr(Decoder, "read", mock_decoder_read)
        with pytest.raises(DiveLogFitDiveNotFoundError) as e:
            fit_parser.parse(file_path)
        assert (
            str(e.value)
            == f"Invalid FIT file: {file_path} does not contain any dive data"
        )

    @patch("builtins.input", return_value="3")
    def test_invalid_dive_idx(
        self, mock_input: Mock, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test parsing a FIT file with an invalid dive index."""

        def mock_decoder_read(
            *_args: Union[str, bool],
            **_kwargs: Union[str, bool],
        ) -> tuple[dict[str, list[Any]], list[Any]]:
            """A mock function for the Decoder.read method."""
            return {
                "file_id_mesgs": [{"type": "activity"}],
                "dive_summary_mesgs": [
                    {
                        "bottom_time": 10,
                        "max_depth": 30.0,
                        "reference_mesg": "lap",
                        "reference_index": 0,
                    },
                    {
                        "bottom_time": 12,
                        "max_depth": 30.0,
                        "reference_mesg": "lap",
                        "reference_index": 1,
                    },
                ],
                "lap_mesgs": [
                    {
                        "start_time": 0,
                    },
                    {
                        "start_time": 55,
                    },
                ],
                "record_mesgs": [],
            }, []

        file_path = "mock"

        fit_parser = GarminFitParser()
        monkeypatch.setattr(Stream, "from_file", self._mock_stream_from_file)
        monkeypatch.setattr(Decoder, "__init__", self._mock_decoder_init)
        monkeypatch.setattr(Decoder, "read", mock_decoder_read)

        with pytest.raises(DiveLogFitDiveNotFoundError) as e:
            fit_parser.parse(file_path)
        assert str(e.value) == "Invalid Dive: Please enter a number between 1 and 2"
        assert mock_input.call_count == 1

    def test_empty_record_mesgs(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test parsing a FIT file with empty record_mesgs."""

        def mock_decoder_read(
            *_args: Union[str, bool],
            **_kwargs: Union[str, bool],
        ) -> tuple[dict[str, list[Any]], list[Any]]:
            """A mock function for the Decoder.read method."""
            return {
                "file_id_mesgs": [{"type": "activity"}],
                "dive_summary_mesgs": [
                    {
                        "bottom_time": 10,
                        "reference_mesg": "lap",
                        "reference_index": 0,
                    }
                ],
                "lap_mesgs": [
                    {
                        "start_time": 0,
                    }
                ],
                "record_mesgs": [],
            }, []

        file_path = "mock"

        fit_parser = GarminFitParser(selected_dive_idx=0)
        monkeypatch.setattr(Stream, "from_file", self._mock_stream_from_file)
        monkeypatch.setattr(Decoder, "__init__", self._mock_decoder_init)
        monkeypatch.setattr(Decoder, "read", mock_decoder_read)
        with pytest.raises(DiveLogFitDiveNotFoundError) as e:
            fit_parser.parse(file_path)
        assert (
            str(e.value)
            == f"Invalid Dive Data: Dive data not found in FIT file: {file_path}"
        )

    def test_file_not_found(self) -> None:
        """Test parsing a FIT file that does not exist."""
        file_path = "invalid_file_path"

        fit_parser = GarminFitParser()
        with pytest.raises(DiveLogFileNotFoundError) as e:
            fit_parser.parse(file_path)
        assert str(e.value) == f"File not found: {file_path}"

    def test_select_dive_single_dive(self) -> None:
        """Test selecting a dive from a FIT file with a single dive."""
        dive_summary = [
            {
                "start_time": 0,
                "end_time": 60,
                "max_depth": 30.0,
                "avg_depth": 20.0,
                "bottom_time": 60,
            }
        ]
        fit_parser = GarminFitParser()
        assert fit_parser.select_dive(dive_summary) == 0

    def test_convert_time(self) -> None:
        """Test converting time from a FIT file to a human-readable format."""
        fit_epoch_time = 1054147458
        fit_parser = GarminFitParser()
        assert (
            fit_parser.convert_fit_epoch_to_datetime(fit_epoch_time)
            == "2023-05-27 18:44:18 (GMT)"
        )

    @patch("builtins.input", return_value="2")
    def test_select_dive_multiple_dives(
        self,
        mock_input: Mock,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Test selecting a dive from a FIT file with multiple dives.

        Note:
            This test uses the mock_input fixture to simulate user input.

        Expected Output:
            Multiple dives found in the FIT file. Please select a dive to import:
            [1]: Dive 1: Start Time: 2023-05-27 19:10:00 (GMT), Max Depth: 30.0m, Bottom Time: 60.0s
            [2]: Dive 2: Start Time: 2023-05-27 19:11:00 (GMT), Max Depth: 20.0m, Bottom Time: 59.0s
        """
        dive_summary = [
            {
                "start_time": 1054149000,
                "end_time": 1054149060,
                "max_depth": 30.0,
                "avg_depth": 20.0,
                "bottom_time": 60,
            },
            {
                "start_time": 1054149060,
                "end_time": 1054149119,
                "max_depth": 20.0,
                "avg_depth": 10.0,
                "bottom_time": 59,
            },
        ]
        fit_parser = GarminFitParser()
        user_select_idx = fit_parser.select_dive(dive_summary)
        expected_idx = int(mock_input.return_value) - 1
        assert user_select_idx == expected_idx

        captured = capsys.readouterr()
        assert "Multiple dives found in the FIT file" in captured.out
        assert (
            "[1]: Dive 1: Start Time: 2023-05-27 19:10:00 (GMT), "
            "Max Depth: 30.0m, Bottom Time: 60.0s" in captured.out
        )
        assert (
            "[2]: Dive 2: Start Time: 2023-05-27 19:11:00 (GMT), "
            "Max Depth: 20.0m, Bottom Time: 59.0s" in captured.out
        )
        assert mock_input.call_count == 1

    @patch("builtins.input", return_value="xxx")
    def test_select_invalid_dive(
        self,
        mock_input: Mock,
    ) -> None:
        """Test selecting an invalid dive index."""
        dive_summary = [
            {
                "start_time": 1054149000,
                "end_time": 1054149060,
                "max_depth": 30.0,
                "avg_depth": 20.0,
                "bottom_time": 60,
            },
            {
                "start_time": 1054149060,
                "end_time": 1054149119,
                "max_depth": 20.0,
                "avg_depth": 10.0,
                "bottom_time": 59,
            },
        ]
        fit_parser = GarminFitParser()
        with pytest.raises(DiveLogFitDiveNotFoundError) as e:
            fit_parser.select_dive(dive_summary)
        assert (
            str(e.value)
            == f"Invalid Dive: Please enter a number between 1 and {len(dive_summary)}"
        )
        assert mock_input.call_count == 1

    @pytest.mark.parametrize("depth_mode", ["raw", "zero-based"])
    @patch("depthviz.parsers.garmin.fit_parser.GarminFitParser.depth_mode_execute")
    def test_parse_valid_fit_depth_mode_exec(
        self,
        mock_depth_mode_execute: Mock,
        depth_mode: str,
        request: pytest.FixtureRequest,
    ) -> None:
        """Test parsing a valid FIT file with depth mode execution."""
        file_path = str(
            request.path.parent.joinpath(
                "data",
                "garmin",
                "11211432883_ACTIVITY.fit",
            )
        )
        parser = GarminFitParser(depth_mode=depth_mode, selected_dive_idx=0)
        parser.parse(file_path)
        mock_depth_mode_execute.assert_called_once()

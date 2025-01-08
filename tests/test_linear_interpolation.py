"""
Unit tests for the linear_interpolation.
"""

import pytest

from depthviz.optimizer.linear_interpolation import (
    LinearInterpolationDepth,
    LinearInterpolationDepthError,
)


class TestLinearInterpolation:
    """
    Test class for the LinearInterpolationDepth class.
    """

    # pylint: disable=too-many-lines
    @pytest.mark.parametrize(
        "times, depths, fps, expected_times, expected_depths",
        [
            (
                [0, 2, 5],
                [10, 20, 40],
                1,
                [0.0, 1.0, 2.0, 3.0, 4.0],
                [10.0, 15.0, 20.0, 26.666666666666668, 33.333333333333336, 40.0],
            ),
            (
                [1, 5, 9],
                [10, 50, 90],
                1,
                [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0],
                [10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0],
            ),
            (
                [0, 10, 20],
                [0, 100, 200],
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
                ],
                [
                    0.0,
                    10.0,
                    20.0,
                    30.0,
                    40.0,
                    50.0,
                    60.0,
                    70.0,
                    80.0,
                    90.0,
                    100.0,
                    110.0,
                    120.0,
                    130.0,
                    140.0,
                    150.0,
                    160.0,
                    170.0,
                    180.0,
                    190.0,
                    200.0,
                ],
            ),
            (
                [0, 1],
                [0, 1],
                5,
                [0.0, 0.2, 0.4, 0.6, 0.8],
                [0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.0, 1.0, 1.0, 1.0],
            ),
            (
                [0, 1, 2, 3],
                [0, 1, 2, 3],
                5,
                [
                    0.0,
                    0.2,
                    0.4,
                    0.6,
                    0.8,
                    1.0,
                    1.2,
                    1.4,
                    1.6,
                    1.8,
                    2.0,
                    2.2,
                    2.4,
                    2.6,
                    2.8,
                ],
                [
                    0.0,
                    0.2,
                    0.4,
                    0.6,
                    0.8,
                    1.0,
                    1.2,
                    1.4,
                    1.6,
                    1.8,
                    2.0,
                    2.2,
                    2.4,
                    2.6,
                    2.8,
                    3.0,
                    3.0,
                    3.0,
                    3.0,
                    3.0,
                ],
            ),
            (
                [0, 1, 2, 3],
                [1, 3, 4, 6],
                25,
                [
                    0.0,
                    0.04,
                    0.08,
                    0.12,
                    0.16,
                    0.2,
                    0.24,
                    0.28,
                    0.32,
                    0.36,
                    0.4,
                    0.44,
                    0.48,
                    0.52,
                    0.56,
                    0.6,
                    0.64,
                    0.68,
                    0.72,
                    0.76,
                    0.8,
                    0.84,
                    0.88,
                    0.92,
                    0.96,
                    1.0,
                    1.04,
                    1.08,
                    1.12,
                    1.16,
                    1.2,
                    1.24,
                    1.28,
                    1.32,
                    1.36,
                    1.4,
                    1.44,
                    1.48,
                    1.52,
                    1.56,
                    1.6,
                    1.64,
                    1.68,
                    1.72,
                    1.76,
                    1.8,
                    1.84,
                    1.88,
                    1.92,
                    1.96,
                    2.0,
                    2.04,
                    2.08,
                    2.12,
                    2.16,
                    2.2,
                    2.24,
                    2.28,
                    2.32,
                    2.36,
                    2.4,
                    2.44,
                    2.48,
                    2.52,
                    2.56,
                    2.6,
                    2.64,
                    2.68,
                    2.72,
                    2.76,
                    2.8,
                    2.84,
                    2.88,
                    2.92,
                    2.96,
                ],
                [
                    1.0,
                    1.08,
                    1.16,
                    1.24,
                    1.32,
                    1.4,
                    1.48,
                    1.56,
                    1.6400000000000001,
                    1.72,
                    1.8,
                    1.88,
                    1.96,
                    2.04,
                    2.12,
                    2.2,
                    2.2800000000000002,
                    2.3600000000000003,
                    2.44,
                    2.52,
                    2.6,
                    2.6799999999999997,
                    2.76,
                    2.84,
                    2.92,
                    3.0,
                    3.04,
                    3.08,
                    3.12,
                    3.16,
                    3.2,
                    3.24,
                    3.2800000000000002,
                    3.3200000000000003,
                    3.3600000000000003,
                    3.4,
                    3.44,
                    3.48,
                    3.52,
                    3.56,
                    3.6,
                    3.6399999999999997,
                    3.6799999999999997,
                    3.7199999999999998,
                    3.76,
                    3.8,
                    3.84,
                    3.88,
                    3.92,
                    3.96,
                    4.0,
                    4.08,
                    4.16,
                    4.24,
                    4.32,
                    4.4,
                    4.48,
                    4.56,
                    4.64,
                    4.72,
                    4.8,
                    4.88,
                    4.96,
                    5.04,
                    5.12,
                    5.2,
                    5.28,
                    5.36,
                    5.44,
                    5.52,
                    5.6,
                    5.68,
                    5.76,
                    5.84,
                    5.92,
                    6.0,
                    6.0,
                    6.0,
                    6.0,
                    6.0,
                    6.0,
                    6.0,
                    6.0,
                    6.0,
                    6.0,
                    6.0,
                    6.0,
                    6.0,
                    6.0,
                    6.0,
                    6.0,
                    6.0,
                    6.0,
                    6.0,
                    6.0,
                    6.0,
                    6.0,
                    6.0,
                    6.0,
                    6.0,
                ],
            ),
            (
                [0, 1],
                [1, 3],
                25,
                [
                    0.0,
                    0.04,
                    0.08,
                    0.12,
                    0.16,
                    0.2,
                    0.24,
                    0.28,
                    0.32,
                    0.36,
                    0.4,
                    0.44,
                    0.48,
                    0.52,
                    0.56,
                    0.6,
                    0.64,
                    0.68,
                    0.72,
                    0.76,
                    0.8,
                    0.84,
                    0.88,
                    0.92,
                    0.96,
                ],
                [
                    1.0,
                    1.08,
                    1.16,
                    1.24,
                    1.32,
                    1.4,
                    1.48,
                    1.56,
                    1.6400000000000001,
                    1.72,
                    1.8,
                    1.88,
                    1.96,
                    2.04,
                    2.12,
                    2.2,
                    2.2800000000000002,
                    2.3600000000000003,
                    2.44,
                    2.52,
                    2.6,
                    2.6799999999999997,
                    2.76,
                    2.84,
                    2.92,
                    3.0,
                    3.0,
                    3.0,
                    3.0,
                    3.0,
                    3.0,
                    3.0,
                    3.0,
                    3.0,
                    3.0,
                    3.0,
                    3.0,
                    3.0,
                    3.0,
                    3.0,
                    3.0,
                    3.0,
                    3.0,
                    3.0,
                    3.0,
                    3.0,
                    3.0,
                    3.0,
                    3.0,
                    3.0,
                ],
            ),
            (
                [0],
                [1],
                25,
                [
                    [
                        0,
                        1,
                        2,
                        3,
                        4,
                        5,
                        6,
                        7,
                        8,
                        9,
                        10,
                        11,
                        12,
                        13,
                        14,
                        15,
                        16,
                        17,
                        18,
                        19,
                        20,
                        21,
                        22,
                        23,
                        24,
                    ]
                ],
                [
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                ],
            ),
            ([0], [1], 5, [[0, 1, 2, 3, 4]], [1, 1, 1, 1, 1]),
            (
                [0, 1, 2],
                [1, 3, 5],
                25,
                [
                    0.0,
                    0.04,
                    0.08,
                    0.12,
                    0.16,
                    0.2,
                    0.24,
                    0.28,
                    0.32,
                    0.36,
                    0.4,
                    0.44,
                    0.48,
                    0.52,
                    0.56,
                    0.6,
                    0.64,
                    0.68,
                    0.72,
                    0.76,
                    0.8,
                    0.84,
                    0.88,
                    0.92,
                    0.96,
                    1.0,
                    1.04,
                    1.08,
                    1.12,
                    1.16,
                    1.2,
                    1.24,
                    1.28,
                    1.32,
                    1.36,
                    1.4,
                    1.44,
                    1.48,
                    1.52,
                    1.56,
                    1.6,
                    1.64,
                    1.68,
                    1.72,
                    1.76,
                    1.8,
                    1.84,
                    1.88,
                    1.92,
                    1.96,
                ],
                [
                    1.0,
                    1.08,
                    1.16,
                    1.24,
                    1.32,
                    1.4,
                    1.48,
                    1.56,
                    1.6400000000000001,
                    1.72,
                    1.8,
                    1.88,
                    1.96,
                    2.04,
                    2.12,
                    2.2,
                    2.2800000000000002,
                    2.3600000000000003,
                    2.44,
                    2.52,
                    2.6,
                    2.6799999999999997,
                    2.76,
                    2.84,
                    2.92,
                    3.0,
                    3.08,
                    3.16,
                    3.24,
                    3.32,
                    3.4,
                    3.48,
                    3.56,
                    3.64,
                    3.72,
                    3.8,
                    3.88,
                    3.96,
                    4.04,
                    4.12,
                    4.2,
                    4.279999999999999,
                    4.359999999999999,
                    4.4399999999999995,
                    4.52,
                    4.6,
                    4.68,
                    4.76,
                    4.84,
                    4.92,
                    5.0,
                    5.0,
                    5.0,
                    5.0,
                    5.0,
                    5.0,
                    5.0,
                    5.0,
                    5.0,
                    5.0,
                    5.0,
                    5.0,
                    5.0,
                    5.0,
                    5.0,
                    5.0,
                    5.0,
                    5.0,
                    5.0,
                    5.0,
                    5.0,
                    5.0,
                    5.0,
                    5.0,
                    5.0,
                ],
            ),
            (
                [0, 2],
                [1, 5],
                25,
                [
                    0.0,
                    0.04,
                    0.08,
                    0.12,
                    0.16,
                    0.2,
                    0.24,
                    0.28,
                    0.32,
                    0.36,
                    0.4,
                    0.44,
                    0.48,
                    0.52,
                    0.56,
                    0.6,
                    0.64,
                    0.68,
                    0.72,
                    0.76,
                    0.8,
                    0.84,
                    0.88,
                    0.92,
                    0.96,
                    1.0,
                    1.04,
                    1.08,
                    1.12,
                    1.16,
                    1.2,
                    1.24,
                    1.28,
                    1.32,
                    1.36,
                    1.4,
                    1.44,
                    1.48,
                    1.52,
                    1.56,
                    1.6,
                    1.64,
                    1.68,
                    1.72,
                    1.76,
                    1.8,
                    1.84,
                    1.88,
                    1.92,
                    1.96,
                ],
                [
                    1.0,
                    1.08,
                    1.16,
                    1.24,
                    1.32,
                    1.4,
                    1.48,
                    1.56,
                    1.6400000000000001,
                    1.72,
                    1.8,
                    1.88,
                    1.96,
                    2.04,
                    2.12,
                    2.2,
                    2.2800000000000002,
                    2.3600000000000003,
                    2.44,
                    2.52,
                    2.6,
                    2.6799999999999997,
                    2.76,
                    2.84,
                    2.92,
                    3.0,
                    3.08,
                    3.16,
                    3.24,
                    3.32,
                    3.4,
                    3.48,
                    3.56,
                    3.64,
                    3.72,
                    3.8,
                    3.88,
                    3.96,
                    4.04,
                    4.12,
                    4.2,
                    4.279999999999999,
                    4.359999999999999,
                    4.4399999999999995,
                    4.52,
                    4.6,
                    4.68,
                    4.76,
                    4.84,
                    4.92,
                    5.0,
                    5.0,
                    5.0,
                    5.0,
                    5.0,
                    5.0,
                    5.0,
                    5.0,
                    5.0,
                    5.0,
                    5.0,
                    5.0,
                    5.0,
                    5.0,
                    5.0,
                    5.0,
                    5.0,
                    5.0,
                    5.0,
                    5.0,
                    5.0,
                    5.0,
                    5.0,
                    5.0,
                    5.0,
                ],
            ),
            (
                [0, 0.5, 1],
                [0, 1, 2],
                5,
                [0.0, 0.2, 0.4, 0.6, 0.8],
                [0.0, 0.4, 0.8, 1.2, 1.6, 2.0, 2.0, 2.0, 2.0, 2.0],
            ),
            (
                [0, 0.5, 1],
                [0, 1, 2],
                25,
                [
                    0.0,
                    0.04,
                    0.08,
                    0.12,
                    0.16,
                    0.2,
                    0.24,
                    0.28,
                    0.32,
                    0.36,
                    0.4,
                    0.44,
                    0.48,
                    0.52,
                    0.56,
                    0.6,
                    0.64,
                    0.68,
                    0.72,
                    0.76,
                    0.8,
                    0.84,
                    0.88,
                    0.92,
                    0.96,
                ],
                [
                    0.0,
                    0.08,
                    0.16,
                    0.24,
                    0.32,
                    0.4,
                    0.48,
                    0.56,
                    0.64,
                    0.72,
                    0.8,
                    0.88,
                    0.96,
                    1.04,
                    1.12,
                    1.2,
                    1.28,
                    1.36,
                    1.44,
                    1.52,
                    1.6,
                    1.68,
                    1.76,
                    1.84,
                    1.92,
                    2.0,
                    2.0,
                    2.0,
                    2.0,
                    2.0,
                    2.0,
                    2.0,
                    2.0,
                    2.0,
                    2.0,
                    2.0,
                    2.0,
                    2.0,
                    2.0,
                    2.0,
                    2.0,
                    2.0,
                    2.0,
                    2.0,
                    2.0,
                    2.0,
                    2.0,
                    2.0,
                    2.0,
                    2.0,
                ],
            ),
            (
                [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                [1, 3, 4, 5, 6, 7, 9, 8, 7, 6],
                25,
                [
                    0.0,
                    0.04,
                    0.08,
                    0.12,
                    0.16,
                    0.2,
                    0.24,
                    0.28,
                    0.32,
                    0.36,
                    0.4,
                    0.44,
                    0.48,
                    0.52,
                    0.56,
                    0.6,
                    0.64,
                    0.68,
                    0.72,
                    0.76,
                    0.8,
                    0.84,
                    0.88,
                    0.92,
                    0.96,
                    1.0,
                    1.04,
                    1.08,
                    1.12,
                    1.16,
                    1.2,
                    1.24,
                    1.28,
                    1.32,
                    1.36,
                    1.4,
                    1.44,
                    1.48,
                    1.52,
                    1.56,
                    1.6,
                    1.64,
                    1.68,
                    1.72,
                    1.76,
                    1.8,
                    1.84,
                    1.88,
                    1.92,
                    1.96,
                    2.0,
                    2.04,
                    2.08,
                    2.12,
                    2.16,
                    2.2,
                    2.24,
                    2.28,
                    2.32,
                    2.36,
                    2.4,
                    2.44,
                    2.48,
                    2.52,
                    2.56,
                    2.6,
                    2.64,
                    2.68,
                    2.72,
                    2.76,
                    2.8,
                    2.84,
                    2.88,
                    2.92,
                    2.96,
                    3.0,
                    3.04,
                    3.08,
                    3.12,
                    3.16,
                    3.2,
                    3.24,
                    3.28,
                    3.32,
                    3.36,
                    3.4,
                    3.44,
                    3.48,
                    3.52,
                    3.56,
                    3.6,
                    3.64,
                    3.68,
                    3.72,
                    3.76,
                    3.8,
                    3.84,
                    3.88,
                    3.92,
                    3.96,
                    4.0,
                    4.04,
                    4.08,
                    4.12,
                    4.16,
                    4.2,
                    4.24,
                    4.28,
                    4.32,
                    4.36,
                    4.4,
                    4.44,
                    4.48,
                    4.52,
                    4.56,
                    4.6,
                    4.64,
                    4.68,
                    4.72,
                    4.76,
                    4.8,
                    4.84,
                    4.88,
                    4.92,
                    4.96,
                    5.0,
                    5.04,
                    5.08,
                    5.12,
                    5.16,
                    5.2,
                    5.24,
                    5.28,
                    5.32,
                    5.36,
                    5.4,
                    5.44,
                    5.48,
                    5.52,
                    5.56,
                    5.6,
                    5.64,
                    5.68,
                    5.72,
                    5.76,
                    5.8,
                    5.84,
                    5.88,
                    5.92,
                    5.96,
                    6.0,
                    6.04,
                    6.08,
                    6.12,
                    6.16,
                    6.2,
                    6.24,
                    6.28,
                    6.32,
                    6.36,
                    6.4,
                    6.44,
                    6.48,
                    6.52,
                    6.56,
                    6.6,
                    6.64,
                    6.68,
                    6.72,
                    6.76,
                    6.8,
                    6.84,
                    6.88,
                    6.92,
                    6.96,
                    7.0,
                    7.04,
                    7.08,
                    7.12,
                    7.16,
                    7.2,
                    7.24,
                    7.28,
                    7.32,
                    7.36,
                    7.4,
                    7.44,
                    7.48,
                    7.52,
                    7.56,
                    7.6,
                    7.64,
                    7.68,
                    7.72,
                    7.76,
                    7.8,
                    7.84,
                    7.88,
                    7.92,
                    7.96,
                    8.0,
                    8.04,
                    8.08,
                    8.12,
                    8.16,
                    8.2,
                    8.24,
                    8.28,
                    8.32,
                    8.36,
                    8.4,
                    8.44,
                    8.48,
                    8.52,
                    8.56,
                    8.6,
                    8.64,
                    8.68,
                    8.72,
                    8.76,
                    8.8,
                    8.84,
                    8.88,
                    8.92,
                    8.96,
                ],
                [
                    1.0,
                    1.08,
                    1.16,
                    1.24,
                    1.32,
                    1.4,
                    1.48,
                    1.56,
                    1.6400000000000001,
                    1.72,
                    1.8,
                    1.88,
                    1.96,
                    2.04,
                    2.12,
                    2.2,
                    2.2800000000000002,
                    2.3600000000000003,
                    2.44,
                    2.52,
                    2.6,
                    2.6799999999999997,
                    2.76,
                    2.84,
                    2.92,
                    3.0,
                    3.04,
                    3.08,
                    3.12,
                    3.16,
                    3.2,
                    3.24,
                    3.2800000000000002,
                    3.3200000000000003,
                    3.3600000000000003,
                    3.4,
                    3.44,
                    3.48,
                    3.52,
                    3.56,
                    3.6,
                    3.6399999999999997,
                    3.6799999999999997,
                    3.7199999999999998,
                    3.76,
                    3.8,
                    3.84,
                    3.88,
                    3.92,
                    3.96,
                    4.0,
                    4.04,
                    4.08,
                    4.12,
                    4.16,
                    4.2,
                    4.24,
                    4.279999999999999,
                    4.32,
                    4.359999999999999,
                    4.4,
                    4.4399999999999995,
                    4.48,
                    4.52,
                    4.5600000000000005,
                    4.6,
                    4.640000000000001,
                    4.68,
                    4.720000000000001,
                    4.76,
                    4.8,
                    4.84,
                    4.88,
                    4.92,
                    4.96,
                    5.0,
                    5.04,
                    5.08,
                    5.12,
                    5.16,
                    5.2,
                    5.24,
                    5.279999999999999,
                    5.32,
                    5.359999999999999,
                    5.4,
                    5.4399999999999995,
                    5.48,
                    5.52,
                    5.5600000000000005,
                    5.6,
                    5.640000000000001,
                    5.68,
                    5.720000000000001,
                    5.76,
                    5.8,
                    5.84,
                    5.88,
                    5.92,
                    5.96,
                    6.0,
                    6.04,
                    6.08,
                    6.12,
                    6.16,
                    6.2,
                    6.24,
                    6.28,
                    6.32,
                    6.36,
                    6.4,
                    6.44,
                    6.48,
                    6.52,
                    6.56,
                    6.6,
                    6.64,
                    6.68,
                    6.72,
                    6.76,
                    6.8,
                    6.84,
                    6.88,
                    6.92,
                    6.96,
                    7.0,
                    7.08,
                    7.16,
                    7.24,
                    7.32,
                    7.4,
                    7.48,
                    7.5600000000000005,
                    7.640000000000001,
                    7.720000000000001,
                    7.800000000000001,
                    7.880000000000001,
                    7.960000000000001,
                    8.04,
                    8.12,
                    8.2,
                    8.28,
                    8.36,
                    8.44,
                    8.52,
                    8.6,
                    8.68,
                    8.76,
                    8.84,
                    8.92,
                    9.0,
                    8.96,
                    8.92,
                    8.879999999999999,
                    8.84,
                    8.8,
                    8.76,
                    8.719999999999999,
                    8.68,
                    8.64,
                    8.6,
                    8.559999999999999,
                    8.52,
                    8.48,
                    8.440000000000001,
                    8.4,
                    8.36,
                    8.32,
                    8.280000000000001,
                    8.24,
                    8.2,
                    8.16,
                    8.120000000000001,
                    8.08,
                    8.04,
                    8.0,
                    7.96,
                    7.92,
                    7.88,
                    7.84,
                    7.8,
                    7.76,
                    7.72,
                    7.68,
                    7.64,
                    7.6,
                    7.56,
                    7.52,
                    7.48,
                    7.44,
                    7.4,
                    7.36,
                    7.32,
                    7.28,
                    7.24,
                    7.2,
                    7.16,
                    7.12,
                    7.08,
                    7.04,
                    7.0,
                    6.960000000000001,
                    6.92,
                    6.880000000000001,
                    6.84,
                    6.800000000000001,
                    6.76,
                    6.720000000000001,
                    6.68,
                    6.640000000000001,
                    6.6,
                    6.5600000000000005,
                    6.52,
                    6.48,
                    6.4399999999999995,
                    6.4,
                    6.359999999999999,
                    6.32,
                    6.279999999999999,
                    6.24,
                    6.199999999999999,
                    6.16,
                    6.119999999999999,
                    6.08,
                    6.039999999999999,
                    6.0,
                    6.0,
                    6.0,
                    6.0,
                    6.0,
                    6.0,
                    6.0,
                    6.0,
                    6.0,
                    6.0,
                    6.0,
                    6.0,
                    6.0,
                    6.0,
                    6.0,
                    6.0,
                    6.0,
                    6.0,
                    6.0,
                    6.0,
                    6.0,
                    6.0,
                    6.0,
                    6.0,
                    6.0,
                ],
            ),
            (
                [0, 0.1, 0.2],
                [1, 2, 3],
                25,
                [0.0, 0.04, 0.08, 0.12, 0.16],
                [
                    1.0,
                    1.4,
                    1.7999999999999998,
                    2.1999999999999997,
                    2.6,
                    3.0,
                    3.0,
                    3.0,
                    3.0,
                    3.0,
                ],
            ),
            ([0, 0.04], [1, 2], 25, [0.0], [1.0, 2.0]),
            ([0, 0.08], [1, 2], 25, [0.0, 0.04], [1.0, 1.5, 2.0, 2.0]),
        ],
    )
    # pylint: disable=too-many-arguments
    def test_linear_interpolation(
        self,
        times: list[float],
        depths: list[float],
        fps: int,
        expected_times: list[float],
        expected_depths: list[float],
    ) -> None:  # pylint: enable=too-many-arguments
        """
        Test the linear_interpolation function.
        """
        handler = LinearInterpolationDepth(times, depths, fps)
        assert handler.get_interpolated_times() == expected_times
        assert handler.get_interpolated_depths() == expected_depths

    @pytest.mark.parametrize(
        "times, depths, fps",
        [
            (
                [
                    0,
                    1,
                    2,
                    3,
                ],
                [
                    1,
                    3,
                    4,
                    5,
                ],
                -2,
            ),
        ],
    )
    def test_invalid_fps(
        self,
        times: list[float],
        depths: list[float],
        fps: int,
    ) -> None:
        """
        Test the linear_interpolation function with invalid fps.
        """
        with pytest.raises(LinearInterpolationDepthError) as e:
            LinearInterpolationDepth(times, depths, fps)
        assert str(e.value) == "Error: FPS must be positive."

    @pytest.mark.parametrize("times, depths, fps", [([0, 1, 2], [1, 3], 25)])
    def test_unequal_time_depth_list_length(
        self,
        times: list[float],
        depths: list[float],
        fps: int,
    ) -> None:
        """
        Test the linear_interpolation function with invalid input.
        """
        with pytest.raises(LinearInterpolationDepthError) as e:
            LinearInterpolationDepth(times, depths, fps)
        assert (
            str(e.value) == "Error: Times and depths lists must have the same length."
        )

    @pytest.mark.parametrize("times, depths, fps", [(None, "XYZ", 25)])
    def test_invalid_input(
        self,
        times: list[float],
        depths: list[float],
        fps: int,
    ) -> None:
        """
        Test the linear_interpolation function with invalid input.
        """
        with pytest.raises(LinearInterpolationDepthError) as e:
            LinearInterpolationDepth(times, depths, fps)
        assert str(e.value) == "Error: Input times and depths must be lists."

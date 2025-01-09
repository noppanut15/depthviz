"""
This module provides a class to perform linear interpolation on depth data.
"""

import math


class LinearInterpolationDepthError(Exception):
    """Base class for exceptions in this module."""


class LinearInterpolationDepth:
    """
    A class to perform linear interpolation on depth data.

    Args:
        times: A list of time points (in seconds).
        depths: A list of corresponding depth values (in meters).
        fps: The target frame rate (frames per second).
    """

    def __init__(self, times: list[float], depths: list[float], fps: int) -> None:
        self.__current_pos = 0
        self.times = times
        self.depths = depths
        self.fps = fps
        self.__new_times: list[float] = []
        self.__interpolated_depths = self.__interpolate_depth()

    def __linear_interpolation(self, x: float, current_pos: int = 0) -> float:
        """
        A helper function to perform linear interpolation between two points.
        """
        i = current_pos
        t1, d1 = self.times[i], self.depths[i]
        t2, d2 = self.times[i + 1], self.depths[i + 1]
        return float(d1 + (x - t1) * (d2 - d1) / (t2 - t1))

    def __interpolate_depth(self) -> list[float]:
        """
        Interpolates depth data to a given frame rate using linear interpolation.
        Original data points are retained at their correct times.
        """

        if not (isinstance(self.times, list) and isinstance(self.depths, list)):
            raise LinearInterpolationDepthError(
                "Error: Input times and depths must be lists."
            )

        if len(self.times) != len(self.depths):
            raise LinearInterpolationDepthError(
                "Error: Times and depths lists must have the same length."
            )

        if self.fps <= 0:
            raise LinearInterpolationDepthError("Error: FPS must be positive.")

        if len(self.times) == 1:
            # If there is only one data point, return a constant depth for a second
            # (according to the fps)
            self.__new_times = [float(t) for t in range(self.fps)]
            return [self.depths[0] for _ in range(self.fps)]

        interpolated_depths = []
        # Calculate the total number of frames
        total_frames = math.ceil((self.times[-1] - self.times[0]) * self.fps)
        # Generate a list of new time points for the interpolated depth data
        self.__new_times = [self.times[0] + (i / self.fps) for i in range(total_frames)]

        # Interpolate the depth values at the new time points
        for i, t in enumerate(self.__new_times):
            # If the time point is the same as the original time point, use the original depth
            if t == self.times[self.__current_pos]:
                interpolated_depths.append(float(self.depths[self.__current_pos]))
            elif t > self.times[self.__current_pos + 1]:
                # If the time point is greater than the next original time point,
                # move the pointer to the next point (of the original time)
                self.__current_pos += 1
                interpolated_depths.append(
                    self.__linear_interpolation(t, self.__current_pos)
                )
            else:
                # Otherwise, interpolate between the current and next original time point
                interpolated_depths.append(
                    self.__linear_interpolation(t, self.__current_pos)
                )

        # If the total time is less than 1 second, double the length of the interpolated depth
        if self.times[-1] - self.times[0] <= 1:
            expected_len = math.ceil(self.fps * (self.times[-1] - self.times[0])) * 2
        else:
            # Otherwise, add one more frame to the length of the interpolated depth
            expected_len = (
                math.ceil(self.fps * (self.times[-1] - self.times[0])) + self.fps
            )
        # If the length of the interpolated depth is less than the expected length,
        # repeat the last depth value and time point
        for i in range(total_frames, expected_len):
            self.__new_times.append(self.__new_times[-1] + (1 / self.fps))
            interpolated_depths.append(float(self.depths[-1]))
        return interpolated_depths

    def get_interpolated_depths(self) -> list[float]:
        """
        Returns the interpolated depth data.
        Returns:
            The interpolated depth data.
        """
        return self.__interpolated_depths

    def get_interpolated_times(self) -> list[float]:
        """
        Returns the interpolated time data.
        Returns:
            The interpolated time data.
        """
        return self.__new_times


# Test cases
# For future reference
# ==============================================================================

# test_cases = [
#     ([0, 2, 5], [10, 20, 40], 1, 6),  # x falls between non-consecutive points
#     ([1, 5, 9], [10, 50, 90], 1, 9),  # another example with bigger gap
#     ([0, 10, 20], [0, 100, 200], 1, 21),
#     ([0, 1], [0, 1], 5, 10),
#     ([0, 1, 2, 3], [0, 1, 2, 3], 5, 20),
#     ([0, 1, 2, 3], [1, 3, 4, 6], 25, 100),  # Standard case
#     ([0, 1], [1, 3], 25, 50),  # Two points
#     ([0], [1], 25, 25),  # One point
#     ([0], [1], 5, 5),  # One point
#     ([0, 1, 2], [1, 3, 5], 25, 75),  # another standard case
#     ([0, 2], [1, 5], 25, 75),  # non-consecutive time
#     ([0, 0.5, 1], [0, 1, 2], 5, 10),  # non-integer time
#     ([0, 0.5, 1], [0, 1, 2], 25, 50),  # non-integer time
#     (
#         [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
#         [
#             1,
#             3,
#             4,
#             5,
#             6,
#             7,
#             9,
#             8,
#             7,
#             6,
#         ],
#         25,
#         250,
#     ),  # 10 seconds
#     ([0, 0.1, 0.2], [1, 2, 3], 25, 10),  # Time difference less than 1 second
#     ([0, 0.04], [1, 2], 25, 2),  # Time difference is exactly 2 frame
#     ([0, 0.08], [1, 2], 25, 4),  # Time difference is 4 frame
#     (
#         [
#             0.25,
#             0.5,
#             0.75,
#             1.0,
#             1.25,
#             1.5,
#             1.75,
#             2.0,
#             2.25,
#             2.5,
#             2.75,
#             3.0,
#         ],
#         [0.1, 0.2, 0.3, 0.4, 0.5, 0.9, 1.3, 1.7, 2.1, 2.5, 2.9, 3.3],
#         25,
#         94,
#     ),  # Standard case
#     # ([0, 30, 60], [0, 30, 0], 25, 1525),
# ]

# if __name__ == "__main__":
#     for time, depth, fps, expected_len in test_cases:
#         handler = LinearInterpolationDepth(times=time, depths=depth, fps=fps)
#         new_times = handler.get_interpolated_times()
#         interpolated_depths = handler.get_interpolated_depths()
#         assert (
#             len(interpolated_depths) == expected_len
#         ), f"Expected {expected_len} but got {len(interpolated_depths)}"
#         assert (
#             len(new_times) == expected_len
#         ), f"Expected {expected_len} but got {len(new_times)}"
#         print(f"({time}, {depth}, {fps}, {new_times}, {interpolated_depths}),")

# Copyright (c) 2024 - 2025 Noppanut Ploywong (@noppanut15) <noppanut.connect@gmail.com>
# Apache License 2.0 (see LICENSE file or http://www.apache.org/licenses/LICENSE-2.0)


"""
Unit tests for the depth module.
"""

import pytest
from depthviz.video.time import TimeReportVideoCreator, TimeReportVideoCreatorError


class TestTimeReportVideoCreator:
    """
    Test the TimeReportVideoCreator class.
    """

    @pytest.mark.parametrize(
        "time_data, expected_duration, expected_num_clips, expected_clip_texts",
        [
            (
                [
                    0.0,
                    0.25,
                    0.5,
                    0.75,
                    1.0,
                    1.25,
                    1.5,
                    1.75,
                    2.0,
                    2.25,
                    2.5,
                    2.75,
                    3.0,
                ],
                4,
                16,
                [
                    "00:00",
                    "00:00",
                    "00:00",
                    "00:00",
                    "00:01",
                    "00:01",
                    "00:01",
                    "00:01",
                    "00:02",
                    "00:02",
                    "00:02",
                    "00:02",
                    "00:03",
                    "00:03",
                    "00:03",
                    "00:03",
                ],
            ),
            ([0.0], 1, 4, ["00:00", "00:00", "00:00", "00:00"]),
            (
                [0.0, 1.0],
                2,
                8,
                [
                    "00:00",
                    "00:00",
                    "00:00",
                    "00:00",
                    "00:01",
                    "00:01",
                    "00:01",
                    "00:01",
                ],
            ),
            (
                [123123412, 123123413, 123123414],
                3,
                12,
                [
                    "00:00",
                    "00:00",
                    "00:00",
                    "00:00",
                    "00:01",
                    "00:01",
                    "00:01",
                    "00:01",
                    "00:02",
                    "00:02",
                    "00:02",
                    "00:02",
                ],
            ),
            (
                [1.0, 2.0, 3.0, 4.0],
                4,
                16,
                [
                    "00:00",
                    "00:00",
                    "00:00",
                    "00:00",
                    "00:01",
                    "00:01",
                    "00:01",
                    "00:01",
                    "00:02",
                    "00:02",
                    "00:02",
                    "00:02",
                    "00:03",
                    "00:03",
                    "00:03",
                    "00:03",
                ],
            ),
            (
                [0.25, 0.5, 0.75, 1.0, 1.25, 1.5],
                3,
                12,
                [
                    "00:00",
                    "00:00",
                    "00:00",
                    "00:00",
                    "00:01",
                    "00:01",
                    "00:01",
                    "00:01",
                    "00:02",
                    "00:02",
                    "00:02",
                    "00:02",
                ],
            ),
        ],
    )
    def test_render_time_report_video(
        self,
        time_data: list[float],
        expected_duration: float,
        expected_num_clips: int,
        expected_clip_texts: list[str],
    ) -> None:
        """
        Test the render_time_report_video method.
        """
        # Create a TimeReportVideoCreator instance
        time_report_video_creator = TimeReportVideoCreator()

        # Create a video with the time data
        video = time_report_video_creator.render_time_report_video(time_data=time_data)

        # Check the video is not None
        assert video is not None

        # Check the duration of the video (seconds)
        assert video.duration == pytest.approx(expected_duration)

        # Check the number of clips in the video
        assert len(video.clips) == expected_num_clips

        # Check the text of all clips in the video
        clip_texts = [clip.text for clip in video.clips]
        assert clip_texts == expected_clip_texts

    @pytest.mark.parametrize(
        "time_data, expected_error_message",
        [
            ([], "The time data is empty."),
            ([-1.0], "The time data contains negative values."),
            ([0.0, -1.0], "The time data contains negative values."),
            ([-1.0, -2.0], "The time data contains negative values."),
        ],
    )
    def test_render_time_report_video_error(
        self, time_data: list[float], expected_error_message: str
    ) -> None:
        """
        Test the render_time_report_video method with error cases.
        """
        # Create a TimeReportVideoCreator instance
        time_report_video_creator = TimeReportVideoCreator()

        # Check the expected error message is raised
        with pytest.raises(TimeReportVideoCreatorError) as e:
            time_report_video_creator.render_time_report_video(time_data=time_data)

        assert str(e.value) == expected_error_message

"""
Unit tests for the core module.
"""

import os.path
import pathlib
import pytest
from depthviz.core import (
    DepthReportVideoCreator,
    VideoNotRenderError,
    VideoFormatError,
    DepthReportVideoCreatorError,
)


class TestDepthReportVideoCreator:
    """
    Test the DepthReportVideoCreator class.
    """

    def test_render_depth_report_video(self) -> None:
        """
        Test the render_depth_report_video method.
        """
        # Create a DepthReportVideoCreator instance
        depth_report_video_creator = DepthReportVideoCreator()

        # Create a depth report video
        time_data = [
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
        ]
        depth_data = [0.1, 0.2, 0.3, 0.4, 0.5, 0.9, 1.3, 1.7, 2.1, 2.5, 2.9, 3.3]
        depth_report_video_creator.render_depth_report_video(
            time_data=time_data, depth_data=depth_data
        )
        video = depth_report_video_creator.get_video()

        # Check the video is not None
        assert video is not None

        # Check the duration of the video (seconds)
        assert video.duration == pytest.approx(3.76)

        # Check the number of clips in the video
        assert len(video.clips) == 94

    def test_save_specific_dir(self, tmp_path: pathlib.Path) -> None:
        """
        Test the save method in a specific directory.
        """
        # Create a DepthReportVideoCreator instance
        depth_report_video_creator = DepthReportVideoCreator(fps=1)

        # Create a depth report video
        time_data = [1.0, 2.0, 3.0]
        depth_data = [0.1, 0.2, 0.3]
        depth_report_video_creator.render_depth_report_video(
            time_data=time_data, depth_data=depth_data
        )

        # Save the video to a file in directory tmp_path
        path = tmp_path / "test_depth_report_video.mp4"
        depth_report_video_creator.save(path=path.as_posix())

        assert path.exists()
        assert path.stat().st_size > 0
        assert path.suffix == ".mp4"

    def test_save_current_dir(self) -> None:
        """
        Test the save method in the current directory.
        """
        # Create a DepthReportVideoCreator instance
        depth_report_video_creator = DepthReportVideoCreator(fps=4)

        # Create a depth report video
        time_data = [0.25, 0.5, 0.75, 1.0]
        depth_data = [0.0, 1.0, 2.0, 3.0]
        depth_report_video_creator.render_depth_report_video(
            time_data=time_data, depth_data=depth_data
        )

        # Save the video to a file in the current directory
        path = ".depth_overlay.mp4"
        depth_report_video_creator.save(path=path)

        assert os.path.exists(".depth_overlay.mp4")

    def test_save_to_nonexistent_path(self, tmp_path: pathlib.Path) -> None:
        """
        Test the save method with a nonexistent path.
        """
        # Create a DepthReportVideoCreator instance
        depth_report_video_creator = DepthReportVideoCreator(fps=1)

        # Create a depth report video
        time_data = [1.0, 2.0, 3.0]
        depth_data = [0.1, 0.2, 0.3]
        depth_report_video_creator.render_depth_report_video(
            time_data=time_data, depth_data=depth_data
        )

        # Save the video to a nonexistent path
        wrong_path = tmp_path / "non_existent_dir" / "test_depth_report_video.mp4"
        with pytest.raises(FileNotFoundError) as e:
            depth_report_video_creator.save(wrong_path.as_posix())
        assert str(e.value) == f"Parent directory does not exist: {wrong_path.parent}"

    def test_save_without_file_name(self, tmp_path: pathlib.Path) -> None:
        """
        Test the save method without a file name.
        """
        # Create a DepthReportVideoCreator instance
        depth_report_video_creator = DepthReportVideoCreator(fps=1)

        # Create a depth report video
        time_data = [1.0, 2.0, 3.0]
        depth_data = [0.1, 0.2, 0.3]
        depth_report_video_creator.render_depth_report_video(
            time_data=time_data, depth_data=depth_data
        )

        # Save the video to a file without a file name
        wrong_path = tmp_path
        with pytest.raises(NameError) as e:
            depth_report_video_creator.save(wrong_path.as_posix())
        assert (
            str(e.value)
            == f"{wrong_path} is a directory, please add a file name to the path. \
                        (e.g., path/to/mydepth_video.mp4)"
        )

    def test_save_video_not_rendered(self, tmp_path: pathlib.Path) -> None:
        """
        Test the save method with a video not rendered.
        """
        # Create a DepthReportVideoCreator instance
        depth_report_video_creator = DepthReportVideoCreator(fps=1)

        # Save the video to a file without rendering it
        path = tmp_path / "test_depth_report_video.mp4"
        with pytest.raises(VideoNotRenderError) as e:
            depth_report_video_creator.save(path=path.as_posix())
        assert str(e.value) == "Cannot save video because it has not been rendered yet."

    def test_save_video_wrong_format(self, tmp_path: pathlib.Path) -> None:
        """
        Test the save method with a wrong file format.
        """
        # Create a DepthReportVideoCreator instance
        depth_report_video_creator = DepthReportVideoCreator(fps=1)

        # Create a depth report video
        time_data = [1.0, 2.0, 3.0]
        depth_data = [0.1, 0.2, 0.3]
        depth_report_video_creator.render_depth_report_video(
            time_data=time_data, depth_data=depth_data
        )

        # Save the video to a file with a wrong file format
        wrong_path = tmp_path / "test_depth_report_video.avi"
        with pytest.raises(VideoFormatError) as e:
            depth_report_video_creator.save(wrong_path.as_posix())
        assert str(e.value) == "Invalid file format: The file format must be .mp4"

    def test_render_depth_video_with_invalid_input(self) -> None:
        """
        Test the render_depth_report_video method with invalid input.
        (different length between time and depth data)
        """
        # Create a DepthReportVideoCreator instance
        depth_report_video_creator = DepthReportVideoCreator(fps=1)

        # Create a depth report video with invalid input
        time_data = [0.1, 0.2, 0.3]
        depth_data = [0.1, 0.2]
        with pytest.raises(DepthReportVideoCreatorError) as e:
            depth_report_video_creator.render_depth_report_video(
                time_data=time_data, depth_data=depth_data
            )
        assert (
            str(e.value)
            == "Interpolation Error; (Error: Times and depths lists must have the same length.)"
        )

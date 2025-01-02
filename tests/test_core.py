"""
Unit tests for the core module.
"""

import os.path
import pathlib
import pytest
from depthviz.core import DepthReportVideoCreator, VideoNotRenderError


class TestDepthReportVideoCreator:
    """
    Test the DepthReportVideoCreator class.
    """

    def test_render_depth_report_video(self) -> None:
        """
        Test the render_depth_report_video method.
        """
        # Create a DepthReportVideoCreator instance
        depth_report_video_creator = DepthReportVideoCreator(sample_rate=0.25)

        # Create a depth report video
        depth_data = [0.1, 0.2, 0.3, 0.4, 0.5, 0.9, 1.3, 1.7, 2.1, 2.5, 2.9, 3.3]
        depth_report_video_creator.render_depth_report_video(depth_data)
        video = depth_report_video_creator.get_video()

        # Check the video is not None
        assert video is not None

        # Check the duration of the video (seconds)
        assert video.duration == 3

        # Check the number of clips in the video
        assert len(video.clips) == 12

    def test_save_specific_dir(self, tmp_path: pathlib.Path) -> None:
        """
        Test the save method in a specific directory.
        """
        # Create a DepthReportVideoCreator instance
        depth_report_video_creator = DepthReportVideoCreator()

        # Create a depth report video
        depth_data = [0.1, 0.2, 0.3]
        depth_report_video_creator.render_depth_report_video(depth_data)

        # Save the video to a file in directory tmp_path
        path = tmp_path / "test_depth_report_video.mp4"
        depth_report_video_creator.save(path=path.as_posix(), fps=1)

        assert path.exists()
        assert path.stat().st_size > 0
        assert path.suffix == ".mp4"

    def test_save_current_dir(self) -> None:
        """
        Test the save method in the current directory.
        """
        # Create a DepthReportVideoCreator instance
        depth_report_video_creator = DepthReportVideoCreator(sample_rate=0.25)

        # Create a depth report video
        depth_data = [0.0, 1.0, 2.0, 3.0]
        depth_report_video_creator.render_depth_report_video(depth_data)

        # Save the video to a file in the current directory
        path = ".depth_overlay.mp4"
        depth_report_video_creator.save(path=path, fps=4)

        assert os.path.exists(".depth_overlay.mp4")

    def test_save_to_nonexistent_path(self, tmp_path: pathlib.Path) -> None:
        """
        Test the save method with a nonexistent path.
        """
        # Create a DepthReportVideoCreator instance
        depth_report_video_creator = DepthReportVideoCreator()

        # Create a depth report video
        depth_data = [0.1, 0.2, 0.3]
        depth_report_video_creator.render_depth_report_video(depth_data)

        # Save the video to a nonexistent path
        wrong_path = tmp_path / "non_existent_dir" / "test_depth_report_video.mp4"
        with pytest.raises(FileNotFoundError) as e:
            depth_report_video_creator.save(wrong_path.as_posix(), fps=1)
        assert str(e.value) == f"Parent directory does not exist: {wrong_path.parent}"

    def test_save_without_file_name(self, tmp_path: pathlib.Path) -> None:
        """
        Test the save method without a file name.
        """
        # Create a DepthReportVideoCreator instance
        depth_report_video_creator = DepthReportVideoCreator()

        # Create a depth report video
        depth_data = [0.1, 0.2, 0.3]
        depth_report_video_creator.render_depth_report_video(depth_data)

        # Save the video to a file without a file name
        wrong_path = tmp_path
        with pytest.raises(NameError) as e:
            depth_report_video_creator.save(wrong_path.as_posix(), fps=1)
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
        depth_report_video_creator = DepthReportVideoCreator()

        # Save the video to a file without rendering it
        path = tmp_path / "test_depth_report_video.mp4"
        with pytest.raises(VideoNotRenderError) as e:
            depth_report_video_creator.save(path=path.as_posix(), fps=1)
        assert str(e.value) == "Cannot save video because it has not been rendered yet."

# Copyright (c) 2024 - 2025 Noppanut Ploywong (@noppanut15) <noppanut.connect@gmail.com>
# Apache License 2.0 (see LICENSE file or http://www.apache.org/licenses/LICENSE-2.0)


"""Unit tests for the progress bar logger class."""

import pytest
from depthviz.video.logger import DepthVizProgessBarLogger


def test_depthviz_progress_bar_logger(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test the DepthVizProgessBarLogger class for the closing tqdm bar function."""

    def mock_close_tqdm_bar(bar_mock: str) -> None:
        """Mock the close_tqdm_bar function to not actually close the bar."""
        print(f"Closing bar: {bar_mock}")
        raise SystemExit()

    progress_bar_logger = DepthVizProgessBarLogger(
        description="Rendering", unit="f", color="#3982d8"
    )
    monkeypatch.setattr(progress_bar_logger, "close_tqdm_bar", mock_close_tqdm_bar)
    monkeypatch.setattr(progress_bar_logger, "tqdm_bars", {"frame_index": "xxx"})

    with pytest.raises(SystemExit):
        progress_bar_logger.new_tqdm_bar(bar="frame_index")

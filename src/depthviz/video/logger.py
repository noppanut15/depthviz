# Copyright (c) 2024 - 2025 Noppanut Ploywong (@noppanut15) <noppanut.connect@gmail.com>
# Apache License 2.0 (see LICENSE file or http://www.apache.org/licenses/LICENSE-2.0)


"""This module contains the progress bar logger class for the DepthViz application."""

from proglog import TqdmProgressBarLogger


class DepthVizProgessBarLogger(TqdmProgressBarLogger):  # type: ignore
    """Class to handle the progress bar logger for the DepthViz application."""

    def __init__(
        self, description: str, unit: str, color: str, ncols: int = 80
    ) -> None:
        """Initialize the progress bar logger."""
        super().__init__(
            init_state=None,
            bars=None,
            leave_bars=False,
            ignored_bars=None,
            logged_bars="all",
            notebook="default",
            print_messages=False,
            min_time_interval=0,
            ignore_bars_under=0,
        )
        self.__description = description
        self.__unit = unit
        self.__color = color
        self.__ncols = ncols

    def new_tqdm_bar(self, bar: str) -> None:
        """Create a new tqdm bar, possibly replacing an existing one."""
        if (bar in self.tqdm_bars) and (self.tqdm_bars[bar] is not None):
            self.close_tqdm_bar(bar)
        infos = self.bars[bar]
        self.tqdm_bars[bar] = self.tqdm(
            total=infos["total"],
            desc=self.__description,
            unit=self.__unit,
            colour=self.__color,
            ncols=self.__ncols,
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} ({remaining} remaining)",
            leave=self.leave_bars,
        )

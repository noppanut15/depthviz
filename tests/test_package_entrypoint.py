# Copyright (c) 2024 - 2025 Noppanut Ploywong (@noppanut15) <noppanut.connect@gmail.com>
# Apache License 2.0 (see LICENSE file or http://www.apache.org/licenses/LICENSE-2.0)


"""
Unit tests for the main entrypoint of the package.
"""

import sys


def test_main_entrypoint() -> None:
    """
    Test the main entrypoint to ensure that it is callable and
    its dependencies are able to be imported.
    """
    # pylint: disable=import-outside-toplevel
    from depthviz.__main__ import run  # type: ignore

    # pylint: enable=import-outside-toplevel
    sys.argv = ["depthviz"]
    ret_code = run()
    assert ret_code == 1

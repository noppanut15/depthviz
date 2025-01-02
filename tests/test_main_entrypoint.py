"""
Unit tests for the main entrypoint of the package.
"""


def test_main_entrypoint():
    """
    Test the main entrypoint to ensure that it is callable and
    its dependencies are able to be imported.
    """
    from depthviz.__main__ import main  # pylint: disable=import-outside-toplevel

    ret_code = main()
    assert ret_code == 1

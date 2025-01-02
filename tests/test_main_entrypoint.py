"""
Unit tests for the main entrypoint of the package.
"""


def test_main_entrypoint() -> None:
    """
    Test the main entrypoint to ensure that it is callable and
    its dependencies are able to be imported.
    """
    # pylint: disable=import-outside-toplevel
    from depthviz.__main__ import main  # type: ignore

    # pylint: enable=import-outside-toplevel
    ret_code = main()
    assert ret_code == 1

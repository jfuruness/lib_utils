import pytest


@pytest.fixture(scope="function", autouse=True)
def reset_logger():
    """Resets logger after every pytest function call

    In this way it can be configured multiple times with no issues
    This is only needed during pytest
    """

    from .. import print_funcs
    print_funcs.logging_set = False

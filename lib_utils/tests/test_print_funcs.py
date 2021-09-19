import logging

import pytest

from .. import print_funcs


@pytest.mark.print_funcs
class TestPrintFuncs:
    """Tests all funcs in file_funcs"""

    def test_config_logging(self):
        """Tests that the loggin occurs and goes to a file"""

        section = "test"
        path = print_funcs.config_logging(section=section)
        log_str = "logging test"
        logging.error(log_str)
        
        with open(path, "r") as f:
            lines = f.read()
            assert log_str in lines

    @pytest.mark.skip(reason="New hires")
    def test_config_logging_duplication(self):
        """Tests calling config_logging twice

        Shouldn't overwrite other files
        Shouldn't create a new file
        Shouldn't add more handlers
        Should still log to the old file
        """

        raise NotImplementedError

    @pytest.mark.skip(reason="New hires")
    def test_config_logging_levels(self):
        """Tests the setting of all log levels"""

        raise NotImplementedError

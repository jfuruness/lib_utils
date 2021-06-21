import logging
import os
from subprocess import TimeoutExpired

import pytest

from .. import file_funcs, helper_funcs, print_funcs


@pytest.mark.helper_funcs
class TestHelperFuncs:
    """Tests all funcs in helper_funcs"""

    @pytest.mark.parametrize("log_level,timeout", [[logging.INFO, None],
                                                   [logging.INFO, True],
                                                   [logging.INFO, False],
                                                   [logging.DEBUG, None],
                                                   [logging.DEBUG, True],
                                                   [logging.DEBUG, False]])
    def test_run_cmds(self, log_level, timeout):
        """Tests the run cmds function with all possible inputs"""

        print_funcs.config_logging(level=log_level, section="test")
        path = "/tmp/run_cmds_test.txt"
        file_funcs.delete_paths(path)
        for cmd in [f"sleep 2 && echo 'test' > {path}",
                    ["sleep 2", f"echo 'test' > {path}"]]:
            # Timeout should be exceeded
            if timeout is True:
                timeout = 1
                with pytest.raises(TimeoutExpired):
                    helper_funcs.run_cmds(cmd, timeout=1)
                assert not os.path.exists(path)
            # timeout should not be exceeded
            elif timeout is False:
                helper_funcs.run_cmds(cmd, timeout=5)
                assert os.path.exists(path)
            # No timeout
            else:
                helper_funcs.run_cmds(cmd)
                assert os.path.exists(path)

import logging
from subprocess import TimeoutExpired

import pytest

from .. import file_funcs, helper_funcs, print_funcs


@pytest.mark.helper_funcs
class TestHelperFuncs:
    """Tests all funcs in helper_funcs"""

    @pytest.mark.skip(reason="New hire work")
    def test_retry(self):
        pass

    @pytest.mark.skip(reason="New hire work")
    def test_pool(self):
        """Tests Pathos ProcessingPool

        Pathos doesn't close pools, so if you create two pools in a row
        with the same params it will error. So this ensures the context
        manager closes it correctly
        """

        def f(x):
            return x * x

        for _ in range(2):
            with helper_funcs.Pool(cpus=2) as p:
                assert p.map(f, [1, 2, 3]) == [1, 4, 9]

    @pytest.mark.skip(reason="New hire work")
    def test_mp_call(self):
        pass

    @pytest.mark.parametrize("log_level,timeout", [[logging.INFO, None],
                                                   [logging.INFO, True],
                                                   [logging.INFO, False],
                                                   [logging.DEBUG, None],
                                                   [logging.DEBUG, True],
                                                   [logging.DEBUG, False]])
    def test_run_cmds(self, log_level, timeout, tmp_path):
        """Tests the run cmds function with all possible inputs"""

        print_funcs.config_logging(level=log_level, section="test")
        path = tmp_path / "run_cmds_test.txt"
        file_funcs.delete_paths([path])
        for cmd in [[f"sleep 2 && echo 'test' > {path}"],
                    ["sleep 2", f"echo 'test' > {path}"]]:
            # Timeout should be exceeded
            if timeout is True:
                timeout = 1
                with pytest.raises(TimeoutExpired):
                    helper_funcs.run_cmds(cmd, timeout=1)
                assert not path.exists()
            # timeout should not be exceeded
            elif timeout is False:
                helper_funcs.run_cmds(cmd, timeout=5)
                assert path.exists()
            # No timeout
            else:
                helper_funcs.run_cmds(cmd)
                assert path.exists()

    @pytest.mark.skip(reason="New hire work")
    def test_get_tags(self):
        pass

    @pytest.mark.skip(reason="New hire work")
    def test_get_hrefs(self):
        pass

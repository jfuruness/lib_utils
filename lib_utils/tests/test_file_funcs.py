import os

import pytest

from .. import file_funcs


@pytest.mark.file_funcs
class TestFileFuncs:
    """Tests all funcs in file_funcs"""

    def test_delete_files(self):
        """Tests the delete files decorator

        Files should be removed both at the start and end of the func
        """

        file_path = "/tmp/delete_files_test.txt"

        @file_funcs.delete_files(files=[file_path])
        def func():
            assert not os.path.exists(file_path)
            with open(file_path, "w+") as f:
                f.write("test")

        with open(file_path, "w+") as f:
            f.write("test")

        func()
        assert not os.path.exists(file_path)

    @pytest.mark.skip
    def test_makedirs(self):
        pass

    @pytest.mark.parametrize("paths", [["/tmp/test_file_utils.txt",
                                        "/tmp/test_file_utils2.txt"],
                                       "/tmp/test_file_utils3.txt",
                                       "/tmp/test_dir",
                                       ["/tmp/test_dir_2",
                                        "/tmp/test_dir_3"]])
    def test_delete_paths(self, paths):
        """Tests that files are deleted properly"""

        # Create files or dirs
        if not isinstance(paths, list):
            _temp_paths = [paths]
        else:
            _temp_paths = paths

        # for each path
        for path in _temp_paths:
            # If it's a file
            if ".txt" in path:
                with open(path, "w+") as f:
                    f.write("test")
            # If it's a dir
            else:
                os.makedirs(path)

        file_funcs.delete_paths(paths)

        for path in _temp_paths:
            assert not os.path.exists(path)

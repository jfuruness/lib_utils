import os
from pathlib import Path

import pytest

from .. import file_funcs


@pytest.mark.file_funcs
class TestFileFuncs:
    """Tests all funcs in file_funcs"""

    def test_delete_files(self, tmpdir: Path):
        """Tests the delete files decorator

        Files should be removed both at the start and end of the func
        """

        file_path = tmpdir / "delete_files_test.txt"

        @file_funcs.delete_files([file_path])
        def func():
            assert not file_path.exists()
            with file_path.open(mode="w+") as f:
                f.write("test")

        with file_path.open(mode="w+") as f:
            f.write("test")

        func()
        assert not file_path.exists()

    @pytest.mark.parametrize("paths", [["test_file_utils.txt",
                                        "test_file_utils2.txt"],
                                       ["test_file_utils3.txt"],
                                       ["test_dir"],
                                       ["test_dir_2",
                                        "test_dir_3"]])
    def test_delete_paths(self, paths: list, tmpdir: Path):
        """Tests that files are deleted properly"""

        paths = [tmpdir / x for x in paths]

        # for each path
        for path in paths:
            # If it's a file
            if ".txt" in path:
                with path.open(mode="w+") as f:
                    f.write("test")
            # If it's a dir
            else:
                path.mkdir()

        file_funcs.delete_paths(paths)

        for path in paths:
            assert not path.exists()

    @pytest.mark.skip(reason="New hires work")
    def test_delete_paths_asserts(self):
        """Tests that assert statements correct typing"""

        pass

    @pytest.mark.skip(reason="New hires work")
    def test_delete_paths_sudo(self):
        """Tests that sudo rm -rf is called when needed"""

        pass

    @pytest.mark.skip(reason="New hires work")
    def test_delete_paths_not_exists(self):
        """Ensures delete_paths succeeds with nonexistant paths"""

        pass

    def test_clean_paths(self, tmpdir: Path):
        """Ensures clean_paths removes and recreates dirs"""

        # Directories
        dir_paths = [tmpdir / "test1", tmpdir / "test2" / "test3"]
        # Files that exist within those directories
        file_paths = [x / "test.txt" for x in paths]

        # Write a temporary file that should get removed
        for path in file_paths:
            with path.open(mode="w+") as f:
                f.write("test")
            assert path.exists()

        clean_paths(dir_paths)

        # Make sure directories still exist
        for path in dir_paths:
            assert path.exists()
        # Make sure directories are empty
        for path in file_paths:
            assert not path.exists()

    @pytest.mark.skip(reason="New hires")
    def test_write_dicts_to_tsv(self):
        pass

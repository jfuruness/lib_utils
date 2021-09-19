"""Contains useful functions relating to files"""

from contextlib import contextmanager
import csv
import functools
import logging
from pathlib import Path
import shutil
from typing import List

import requests

from .helper_funcs import run_cmds, retry


@contextmanager
def temp_path(path_str=None, path_append=None):
    if path_str is None:
        path_str = f"/tmp/{datetime.now()}".replace(" ", "_")
    if path_append:
        path_str += path_append
    delete_paths([Path(path_str)])
    yield Path(path_str)
    delete_paths([Path(path_str)])


# This decorator deletes paths before and after func is called
def delete_files(paths: List[Path]):
    """This decorator deletes files before and after a function.
    This is very useful for installation procedures.
    """
    def my_decorator(func):
        @functools.wraps(func)
        def function_that_runs_func(*args, **kwargs):
            # Inside the decorator
            # Delete the files - prob don't exist yet
            delete_paths(paths)
            # Run the function
            stuff = func(*args, **kwargs)
            # Delete the files if they do exist
            delete_paths(paths)
            return stuff
        return function_that_runs_func
    return my_decorator


@retry(Exception, tries=2, msg="Failed download")
def download_file(url: str, path: Path, timeout=60, verify=False, err=False):
    """Downloads a file from a url into a path."""

    # https://stackoverflow.com/a/39217788/8903959
    # This works best for specifically long files
    # Urlretrieve is deprecated:
    # https://docs.python.org/3.5/library/urllib.request.html#legacy-interface
    # Send a get request to URL
    with requests.get(url, stream=True, verify=verify, timeout=timeout) as r:
        if r.status_code == 200:
            # open the file and copy to it
            with path.open(mode='wb') as f:
                shutil.copyfileobj(r.raw, f)
        else:
            logging.warning(f"{url} returned {r.status_code}")
            if err:
                r.raise_for_status()


def delete_paths(paths: List[Path]):
    """Removes directory if directory, or removes path if path"""

    assert isinstance(paths, list), "delete_paths needs a list of Path objects"

    for path in paths:
        assert isinstance(path, Path), "Must be a path object"
        if path.exists():
            if path.is_file():
                path.unlink()
            else:
                try:
                    shutil.rmtree(str(path))
                except PermissionError:
                    run_cmds(f"sudo rm -rf {str(path)}")


def clean_paths(paths: List[Path]):
    """If path exists remove it, else create it"""

    # delete_paths verifies the typing
    delete_paths(paths)
    for path in paths:
        path.mkdir(parents=True)


def write_dicts_to_tsv(list_of_dicts: List[dict], path: Path):
    """Writes a list of dicts to TSV

    Note - column ordering = column ordering in the first dict
    """

    logging.debug(f"Writing rows to {path}")
    with path.open(mode="w+") as f:
        cols = list(list_of_dicts[0].keys())
        writer = csv.DictWriter(f, fieldnames=cols, delimiter="\t")
        writer.writeheader()
        writer.writerows(list_of_dicts)

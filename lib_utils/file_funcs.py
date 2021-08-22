"""Contains useful functions relating to files"""

from contextlib import contextmanager
import csv
from datetime import datetime
import functools
import logging
import os
import shutil
import subprocess

import requests


from .helper_funcs import run_cmds, retry


# This decorator deletes paths before and after func is called
def delete_files(files=[]):
    """This decorator deletes files before and after a function.
    This is very useful for installation procedures.
    """
    def my_decorator(func):
        @functools.wraps(func)
        def function_that_runs_func(*args, **kwargs):
            # Inside the decorator
            # Delete the files - prob don't exist yet
            delete_paths(files)
            # Run the function
            stuff = func(*args, **kwargs)
            # Delete the files if they do exist
            delete_paths(files)
            return stuff
        return function_that_runs_func
    return my_decorator

@contextmanager
def temp_path(path=None, path_append=None):

    if path is None:
        path = f"/tmp/{datetime.now()}".replace(" ", "_")
    if path_append:
        path += path_append
    delete_paths(path)
    yield path
    delete_paths(path)

def makedirs(path, remake=False):
    # Get all subpaths
    all_paths = []
    for i in range(len(path.split("/"))):
        subpath = "/".join(path.split("/")[:i + 1])
        if subpath not in ["/", "", " "]:
            all_paths.append(subpath)

    # Make all subpaths if they do not exist
    for path in all_paths[:-1]:
        makedir(path)
    # Make final path, and remake if desired
    makedir(all_paths[-1], remake=remake)

def makedir(path, remake=False):
    try:
        os.makedirs(path)
    except PermissionError as e:
        # We don't always want to attempt sudo. Ex: Pytest
        # https://stackoverflow.com/a/58866220
        if "PYTEST_CURRENT_TEST" in os.environ:
            raise e
        else:
            logging.warning(f"PermissionError when creating {path}. "
                            "Attempting with sudo")
            # -p creates parent dirs. Thanks Tony!
            cmd = f"sudo mkdir -p {path} && sudo chown -R $USER:$USER {path}"
 
            try:
                run_cmds(cmd)
            # Sudo must have failed, needs permissions
            except subprocess.CalledProcessError as subprocess_exc:
                logging.error("Command {cmd} failed with {subprocess_exc}")
                raise e
    except FileExistsError:
        logging.debug(f"Path already exists: {path}")
        if remake:
            logging.debug(f"Recreating path: {path}")
            try:
                shutil.rmtree(path)
            except PermissionError:
                run_cmds("sudo rm -rf {path}")
            makedir(path, remake=False)


@retry(Exception, tries=2, msg="Failed download")
def download_file(url: str, path: str, timeout=60, verify=False, err=False):
    """Downloads a file from a url into a path."""

    # NOTE: NO LOGGING!!! really slows down multiprocessing
    
    # https://stackoverflow.com/a/39217788/8903959
    # This works best for specifically long files
    # Urlretrieve is deprecated:
    # https://docs.python.org/3.5/library/urllib.request.html#legacy-interface
    # Send a get request to URL
    with requests.get(url, stream=True, verify=verify, timeout=timeout) as r:
        if r.status_code == 200:
            # open the file and copy to it
            with open(path, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
        else:
            logging.warning(f"{url} returned {r.status_code}")
            if err:
                r.raise_for_status()


def delete_paths(paths):
    """Removes directory if directory, or removes path if path"""

    # If a single path is passed in, convert it to a list
    if not isinstance(paths, list):
        paths = [paths]

    for path in paths:
        try:
            remove_func = os.remove if os.path.isfile(path) else shutil.rmtree
            remove_func(path)
        # Just in case we always delete everything at the end of a run
        # So some files may not exist anymore
        except AttributeError:
            logging.debug(f"Attribute error when deleting {path}")
        except FileNotFoundError:
            logging.debug(f"File not found when deleting {path}")
        except PermissionError:
            logging.warning(f"Permission error when deleting {path}, retrying")
            run_cmds(f"sudo rm -rf {path}")


def clean_paths(paths):
    """If path exists remove it, else create it"""

    # If a single path is passed in, convert it to a list
    if not isinstance(paths, list):
        paths = [paths]
    delete_paths(paths)
    for path in paths:
        makedirs(path)

def write_dicts_to_tsv(list_of_dicts, path):
    """Writes a list of dicts to TSV

    Note - column ordering = column ordering in the first dict
    """

    logging.debug(f"Writing rows to {path}")
    with open(path, mode="w+") as f:
        cols = list(list_of_dicts[0].keys())
        writer = csv.DictWriter(f, fieldnames=cols, delimiter="\t")
        writer.writeheader()
        writer.writerows(list_of_dicts)

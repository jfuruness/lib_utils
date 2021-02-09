"""Contains useful functions relating to files"""

import functools
import logging
import os

import urllib
import shutil

from .helper_funcs import run_cmds, retry


# This decorator deletes paths before and after func is called
def delete_files(files=[]):
    """This decorator deletes files before and after a function.
    This is very useful for installation procedures.
    """
    def my_decorator(func):
        @functools.wraps(func)
        def function_that_runs_func(self, *args, **kwargs):
            # Inside the decorator
            # Delete the files - prob don't exist yet
            delete_paths(files)
            # Run the function
            stuff = func(self, *args, **kwargs)
            # Delete the files if they do exist
            delete_paths(files)
            return stuff
        return function_that_runs_func
    return my_decorator


def makedirs(path, remake=False):
    try:
        os.makedirs(path)
    except PermissionError:
        run_cmds([f"sudo mkdir {path}", f"sudo chmod -R 777 {path}"])
    except FileExistsError:
        if remake:
            shutil.rmtree(path)
            makedirs(path)


@retry(Exception, tries=2, msg="Failed download")
def download_file(url: str, path: str):
    """Downloads a file from a url into a path."""

    logging.info(f"Downloading\n\tPath:{path}\n\tLink:{url}\n")
    # Code for downloading files off of the internet
    # long since forgetten the link sorry
    with urllib.request.urlopen(url, timeout=60)\
            as response, open(path, 'wb') as out_file:
        # Copy the file into the specified file_path
        shutil.copyfileobj(response, out_file)


def delete_paths(paths):
    """Removes directory if directory, or removes path if path"""

    if not paths:
        paths = []
    # If a single path is passed in, convert it to a list
    if not isinstance(paths, list):
        paths = [paths]
    for path in paths:
        try:
            remove_func = os.remove if os.path.isfile(path) else shutil.rmtree
            remove_func(path)
            # If the path is a file
            if os.path.isfile(path):
                # Delete the file
                os.remove(path)
            # If the path is a directory
            if os.path.isdir(path):
                # rm -rf the directory
                shutil.rmtree(path)
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

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
    except PermissionError as e:
        # We don't always want to attempt sudo. Ex: Pytest
        # https://stackoverflow.com/a/58866220
        if "PYTEST_CURRENT_TEST" in os.environ:
            raise e
        else:
            logging.debug(f"PermissionError when creating {path}. "
                          "Attempting with sudo")
            cmd = f"sudo mkdir {path} && sudo chmown -R $USER:$USER {path}"
 
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
            shutil.rmtree(path)
            makedirs(path)


@retry(Exception, tries=2, msg="Failed download")
def download_file(url: str, path: str, timeout=60):
    """Downloads a file from a url into a path."""

    logging.info(f"Downloading\n\tPath:{path}\n\tLink:{url}\n")
    # Code for downloading files off of the internet
    # long since forgetten the link sorry
    with urllib.request.urlopen(url, timeout=timeout)\
            as response, open(path, 'wb') as out_file:
        # Copy the file into the specified file_path
        shutil.copyfileobj(response, out_file)


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

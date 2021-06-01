"""Contains useful functions relating to printing"""

from datetime import datetime
import functools
import logging
import os
import sys

import multiprocessing_logging

from .file_funcs import makedirs


def config_logging(level=logging.INFO, section="main"):
    """Configures logging to log to a file and screen"""

    if len(logging.root.handlers) == 0:

        path = _get_log_path(section)

        logging.root.handlers = []
        logging.basicConfig(level=level,
                            format='%(asctime)s-%(levelname)s: %(message)s',
                            handlers=[logging.StreamHandler(),
                                      logging.FileHandler(path)])

        logging.captureWarnings(True)
        multiprocessing_logging.install_mp_handler()
        logging.debug("initialized logger")


def _get_log_path(section):
    """Returns path to log file"""

    fname = f"{section}_{datetime.now().strftime('%Y_%m_%d_%M_%S.%f')}.log"
    log_dir = f"/var/log/{section}/"

    makedirs(log_dir)

    return os.path.join(log_dir, fname)


def write_to_stdout(msg: str):
    sys.stdout.write(f"{msg}\n")
    sys.stdout.flush()


# This decorator prints exception upon err
def print_err(err, msg="{}"):
    """This decorator deletes files before and after a function.
    This is very useful for installation procedures.
    """
    def my_decorator(func):
        @functools.wraps(func)
        def function_that_runs_func(*args, **kwargs):
            try:
                # Run the function
                return func(*args, **kwargs)
            except err as e:
                logging.error(msg.format(e))
        return function_that_runs_func
    return my_decorator

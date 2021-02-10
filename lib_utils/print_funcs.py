"""Contains useful functions relating to printing"""

import logging
import sys

import multiprocessing_logging


def config_logging(level=logging.INFO):
    """Configures logging to log to a file and screen"""

    if len(logging.root.handlers) != 1:
        logging.root.handlers = []
        logging.basicConfig(level=level,
                            format='%(asctime)s-%(levelname)s: %(message)s',
                            handlers=[logging.StreamHandler()])

        logging.captureWarnings(True)
        multiprocessing_logging.install_mp_handler()
        logging.debug("initialized logger")


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

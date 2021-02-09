"""This package contains functions useful functions"""

from contextlib import contextmanager
import functools
import logging
from multiprocessing import cpu_count
from subprocess import check_call, DEVNULL
import time

from pathos.multiprocessing import ProcessingPool


# This decorator retries func if it fails
def retry(err, tries=5, msg="", sleep=.1):
    """This decorator deletes files before and after a function.
    This is very useful for installation procedures.
    """
    def my_decorator(func):
        @functools.wraps(func)
        def function_that_runs_func(*args, **kwargs):
            # Inside the decorator
            e = None
            # Number of tries
            for i in range(tries):
                try:
                    # Run the function
                    return func(*args, **kwargs)
                except err as f:
                    time.sleep(sleep)
                    e = f
                # Delete the files if they do exist
            logging.error(msg)
            raise e
            assert False, "Should never reach here, in retry decorator"
        return function_that_runs_func
    return my_decorator


@contextmanager
def Pool(threads=None, multiplier=1):
    """Context manager for pathos ProcessingPool"""

    # Creates a pool with threads else cpu_count * multiplier
    p = ProcessingPool(threads if threads else cpu_count() * multiplier)
    yield p
    # Need to clear due to:
    # https://github.com/uqfoundation/pathos/issues/111
    p.close()
    p.join()
    p.clear()


def run_cmds(cmds, timeout=None, stdout=False):

    cmd = " && ".join(cmds) if isinstance(cmds, list) else cmds

    kwargs = {"shell": True}

    # If logging is greater than or equal to info
    if logging.root.level >= 20 and stdout is False:
        kwargs.update({"stdout": DEVNULL, "stderr": DEVNULL})
    if timeout is not None:
        kwargs["timeout"] = timeout

    logging.debug(f"Running: {cmd}")
    check_call(cmd, **kwargs)

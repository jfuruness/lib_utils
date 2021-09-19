"""This package contains functions useful functions"""

from contextlib import contextmanager
import functools
import logging
from multiprocessing import cpu_count
from subprocess import check_call, DEVNULL
import time

from bs4 import BeautifulSoup as Soup
from pathos.multiprocessing import ProcessingPool
import requests
from tqdm import tqdm

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def retry(err, tries=5, msg="", fail_func=lambda: time.sleep(.1)):
    """This decorator retries a func with the added fail func"""

    def my_decorator(func):
        @functools.wraps(func)
        def function_that_runs_func(*args, **kwargs):
            # Inside the decorator
            e = None
            # Number of tries
            for _ in range(tries):
                try:
                    # Run the function
                    return func(*args, **kwargs)
                except err as exc:
                    fail_func()
                    e = exc
            logging.error(msg)
            raise e
        return function_that_runs_func
    return my_decorator


@contextmanager
def Pool(cpus=cpu_count()) -> ProcessingPool:
    """Context manager for pathos ProcessingPool"""

    # Creates a pool with processes
    p = ProcessingPool(cpus)
    yield p
    # Need to clear due to:
    # https://github.com/uqfoundation/pathos/issues/111
    p.close()
    p.join()
    p.clear()


def mp_call(func, args: list, desc: str, cpus=cpu_count()):
    """Makes a multiprocess call to a function with a progress bar"""

    
    with Pool(cpus=cpus) as p:
        # Imap is an ordered map that returns an iterator
        list(tqdm(p.imap(func, *args), total=len(args[0]), desc=desc))


def run_cmds(cmds: list, timeout=None, stdout=False):

    assert isinstance(cmds, list)

    cmd = " && ".join(cmds)

    kwargs = {"shell": True}

    # If logging is greater than or equal to info
    if logging.root.level >= 20 and stdout is False:
        kwargs.update({"stdout": DEVNULL, "stderr": DEVNULL})
    if timeout is not None:
        kwargs["timeout"] = timeout

    logging.debug(f"Running: {cmd}")
    check_call(cmd, **kwargs)

def get_tags(url: str, tag: str, timeout=30, verify=False) -> list:
    """Gets the html of given url and returns a list of tags"""

    # Verify verifies the SSL. Most website I scrape from have outdated certs
    response = requests.get(url, timeout=timeout, verify=verify)
    # Raises an exception if there was an error
    response.raise_for_status()
    # Get all tags within the beautiful soup from the html and return them
    tags = [x for x in Soup(response.text, 'html.parser').select(tag)]
    response.close()

    return tags

def get_hrefs(url: str, tag="a", timeout=30, verify=False) -> list[str]:
    """Returns all hrefs that have an a tag at a given url"""

    hrefs = []
    for x in get_tags(url, tag, timeout=timeout, verify=verify):
        # Get doesn't work normally
        if x.get("href") is not None:
            hrefs.append(x["href"])
    return hrefs

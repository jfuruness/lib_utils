"""Contains useful functions relating to printing"""

from datetime import datetime
import functools
import logging
import os
from pathlib import Path
import sys

import multiprocessing_logging

from .file_funcs import makedirs

logging_set = False

def config_logging(level=logging.INFO, section="main", mp=False) -> Path:
    """Configures logging to log to a file and screen

    mp stands for multiprocessing, didn't want to override that package
    """

    # NOTE: it turns out that subprocess calls, pytest, etc
    # Seems to automatically add handlers, even if they are not set
    # The only real way to check if we have handlers set
    # Is to check if we have specific handlers that are set, or a global
    global logging_set
    if not logging_set:

        path = _get_log_path(section)

        # without this it doesn't work
        logging.root.handlers = []
        logging.basicConfig(level=level,
                            format='%(asctime)s-%(levelname)s: %(message)s',
                            handlers=[logging.StreamHandler(),
                                      logging.FileHandler(path)])

        logging.captureWarnings(True)

        # If you need multiprocessing install this
        # Otherwise it slows it down, and additionally doesn't flush
        # after every call, which ruins logging unit tests
        # . See: https://github.com/jruere/
        # multiprocessing-logging/issues/51#issue-925800880
        if mp:
            multiprocessing_logging.install_mp_handler()
        logging.debug("initialized logger")
        logging_set = True
        return path


def _get_log_path(section: str) -> Path:
    """Returns path to log file"""

    fname = f"{section}_{datetime.now().strftime('%Y_%m_%d_%M_%S.%f')}.log"
    log_dir = f"/var/log/{section}/"

    path = Path(log_dir)
    path.mkdir(parents=True)
    return path / fname

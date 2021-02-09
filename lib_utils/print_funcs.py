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

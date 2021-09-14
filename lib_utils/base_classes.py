"""Contains useful base classes"""

from datetime import datetime, timedelta
from multiprocessing import cpu_count
import os

from .file_funcs import makedirs
from .helper_funcs import mp_call


class Base:
    """Base collector for classes that perform ETL"""

    def __init__(self, **kwargs):
        # Save kwargs in case you need to initialize other Base Classes
        self.kwargs = kwargs
        # Gets default download time if not otherwise set
        self.dl_time = kwargs.get("dl_time", self._default_dl_time())
        # Sets directory to download files to and write parsed files
        self._dir = os.path.join(kwargs.get("_dir", "/tmp/"),
                                 self.__class__.__name__,
                                 self.dl_time.strftime("%Y.%m.%d.%H.%M.%S"))
        # Make self._dir
        makedirs(self._dir)#, remake=True)
        # Path to output file
        self.tsv_path = os.path.join(self._dir,
                                     f"{self.__class__.__name__}.tsv")
        # CPUs for downloading files (I/O bound)
        self.dl_cpus = kwargs.get("dl_cpus", cpu_count() * 4)
        # CPUs for processing.
        # Some funcs go haywire if you use every core. cores-1 seems fine
        self.parse_cpus = kwargs.get("parse_cpus", cpu_count() - 1)
        # Store in the db or not
        self.db = kwargs.get("db", False)
        # Debug info
        self.debug = kwargs.get("debug", False)
        assert hasattr(self, "run"), "Needs a run function"

    def parse_mp(self, func, args: list, desc=None, parse_cpus=None):
        """Calls a parsing function using multiprocessing

        parse cpus is by default equal to cpu_count() - 1
        """

        self._mp(func, args, desc, "parsing", parse_cpus, self.parse_cpus)

    def download_mp(self, func, args: list, desc=None, dl_cpus=None):
        """Calls a download function using multiprocessing

        Download cpus is by default equal to cpu_count() * 4
        This should be an I/O bound process
        """

        self._mp(func, args, desc, "downloading", dl_cpus, self.dl_cpus)

    def _mp(self, func, args: list, desc, default_action, cpus, default_cpus):
        """Call a function with multiprocessing"""

        if cpus is None:
            cpus = default_cpus
        if desc is None:
            desc = f"{self.__class__.__name__} is {default_action}"

        mp_call(func, args, desc, cpus=cpus)

    def _default_dl_time(self):
        """Returns default DL time.

        For most things, we download from 4 days ago
        And for collectors, time must be divisible by 4/8
        """

        # 7 days because sometimes caida takes a while to upload
        dl_time = datetime.utcnow() - timedelta(days=7)
        return dl_time.replace(hour=0, minute=0, second=0, microsecond=0)


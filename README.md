
# lib\_utils
This package contains helper functions. Originally [this](https://github.com/jfuruness/lib_bgp_data/blob/master/lib_bgp_data/utils/utils.py)

* [lib\_utils](#lib_utils)
* [Description](#package-description)
* [Usage](#usage)
* [Installation](#installation)
* [Testing](#testing)
* [Development/Contributing](#developmentcontributing)
* [History](#history)
* [Credits](#credits)
* [Licence](#license)

## Package Description
* [lib\_utils](#lib_utils)

This package contains helper functions. Originally [this](https://github.com/jfuruness/lib_bgp_data/blob/master/lib_bgp_data/utils/utils.py)


## Usage
* [lib\_utils](#lib_utils)

Functions:
* file functions:
    * delete_files: (decorator) deletes a list of files or dirs before and after func
    * make_dirs: makes a directory
    * download_file: downloads a file, tries twice
    * delete_paths: deletes paths
    * clean_paths: deletes paths and then remakes dirs
* print functions:
    * config_logging: configures logging for printing
    * write_to_stdout: writes to standard out w/\n and flushes buffer
* helper functions
    * retry: (decorator) retries a function if it errors with error X Y times, sleeping z seconds inbetween each time
    * Pool: (context manager) creates a pathos processing pool that closes automatically
    * run_cmds: Runs bash commands properly. Can suppress stdout.

```python
from lib_utils import file_funcs, helper_funcs, print_funcs
# An example of a function
helper_funcs.run_cmds("ls", stdout=True)
```

## Installation
* [lib\_utils](#lib_utils)

Many helper functions rely on linux

Install python3 and pip if you have not already. Then run:

```bash
pip3 install wheel
pip3 install lib_utils
```
This will install the package and all of it's python dependencies.

If you want to install the project for development:
```bash
git clone https://github.com/jfuruness/lib_utils.git
cd lib_utils
pip3 install wheel
pip3 install -e .
```

To test the development package: [Testing](#testing)


## Testing
* [lib\_utils](#lib_utils)

You can test the package if in development by moving/cd into the directory where setup.py is located and running:
(Note that you must have all dependencies installed first)
```python3 setup.py test```

To test from pip install:
```bash
pip3 install wheel
# janky but whatever. Done to install deps
pip3 install lib_utils
pip3 uninstall lib_utils
pip3 install lib_utils --install-option test
```

## Development/Contributing
* [lib\_utils](#lib_utils)

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request
6. Email me at jfuruness@gmail.com because idk how to even check those messages

## History
* [lib\_utils](#lib_utils)
* 0.1.0 First production release

## Credits
* [lib\_utils](#lib_utils)

Credits to Drew Monroe and the UITS team for inspiring this library. Credits to Matt Jaccino, Sam Kasbawala, and Tony Zheng for their help in the [original utils](https://github.com/jfuruness/lib_bgp_data/blob/master/lib_bgp_data/utils/utils.py).

## License
* [lib\_utils](#lib_utils)

BSD License (see license file)

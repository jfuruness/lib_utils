
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
* [To do](#todo)


## Package Description
* [lib\_utils](#lib_utils)

This package contains helper functions. Originally [this](https://github.com/jfuruness/lib_bgp_data/blob/master/lib_bgp_data/utils/utils.py)


## Usage
* [lib\_utils](#lib_utils)

Functions:
* file functions:
    * delete_files: (decorator) deletes a list of files or dirs before and after func
    * download_file: downloads a file, tries twice
    * delete_paths: deletes paths
    * clean_paths: deletes paths and then remakes dirs
    * write_dicts_to_tsv: Writes a list of dictionaries to a TSV file with a header
* print functions:
    * config_logging: configures logging for printing
* helper functions
    * retry: (decorator) retries a function if it errors with error X Y times, sleeping z seconds inbetween each time
    * Pool: (context manager) creates a pathos processing pool that closes automatically
    * mp_call: Multiprocess call to a function that also updates tqdm
    * run_cmds: Runs bash commands properly. Can suppress stdout.
    * get_tags: Gets all tags of a given URL
    * get_hrefs: Gets all hrefs of a given URL
 * base_classes
   * Base: Contains useful functions for classes that deal with simulations

```python
from lib_utils import file_funcs, helper_funcs, print_funcs
# An example of a function
helper_funcs.run_cmds("ls", stdout=True)
```

There are very few helper functions, and I don't want to take the time to document them extensively. Just view the source code, the functions are well documented there. I know that is not great practice, but most likely I am the only one who will use this repo.

## Installation
* [lib\_utils](#lib_utils)

Many helper functions rely on linux

To create the default logging directories:
```bash
# Section for default logging
sudo mkdir /var/log/main
sudo chown -R $USER:$USER /var/log/main
# Section for test logging
sudo mkdir /var/log/test
sudo chown -R $USER:$USER /var/log/test
```

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
python3 setup.py develop
```

To test the development package: [Testing](#testing)


## Testing
* [lib\_utils](#lib_utils)

You can test the package if in development by moving/cd into the directory where setup.py is located and running:
(Note that you must have all dependencies installed first)
```python3 setup.py test```

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
* 0.2.0 Moved over to Path from pathlib. Removed useless functions. Added more tests. Added more functions. Added Base class
* 0.1.7 Added more unit tests, fixed multiprocess logging
* 0.1.6 Added get_tags, added
* 0.1.5 fixed an error in the print_err func
* 0.1.4 Added print_err func
* 0.1.2 Minor edits to readme and files
* 0.1.0 First production release

## Credits
* [lib\_utils](#lib_utils)

Credits to Drew Monroe and the UITS team for inspiring this library. Credits to Matt Jaccino, Sam Kasbawala, and Tony Zheng for their help in the [original utils](https://github.com/jfuruness/lib_bgp_data/blob/master/lib_bgp_data/utils/utils.py).

## License
* [lib\_utils](#lib_utils)

BSD License (see license file)

## Todo
* [lib\_utils](#lib_utils)

Better unit tests. Oof.



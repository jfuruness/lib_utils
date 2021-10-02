from setuptools import setup, find_packages
import sys

setup(
    name='lib_utils',
    packages=find_packages(),
    version='0.2.1',
    author='Justin Furuness, Tony Zheng',
    author_email='jfuruness@gmail.com',
    url='https://github.com/jfuruness/lib_utils.git',
    download_url='https://github.com/jfuruness/lib_utils.git',
    keywords=['Furuness', 'Utils', 'Wrapper', 'ETL', 'Helper Functions'],
    install_requires=[
            "bs4",
            "multiprocessing_logging",
            "pathos",
            "pytest",
            "requests",
            "tqdm",
        ],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3'],
    python_requires=">=3.7",
    entry_points={},
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)

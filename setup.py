from setuptools import setup, find_packages
import sys

setup(
    name='lib_utils',
    packages=find_packages(),
    version='0.1.5',
    author='Justin Furuness',
    author_email='jfuruness@gmail.com',
    url='https://github.com/jfuruness/lib_utils.git',
    download_url='https://github.com/jfuruness/lib_utils.git',
    keywords=['Furuness', 'Utils', 'Wrapper', 'ETL', 'Helper Functions'],
    install_requires=[
            "multiprocessing_logging",
            "pathos",
        ],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3'],
    entry_points={},
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)

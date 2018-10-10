#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name="pyMeSHSim",
    version='0.0.1',
    description="tools for MeSH system operation",
    author="luozhihui",
    author_email='luozhihui1123@163.com',
    # url="https://github.com/username/reponame",
    # download_url='https://github.com/username/reponame/archive/0.1.tar.gz',
    keywords=['MeSH', 'Metamap', 'similarity'],
    packages=find_packages(),
    include_package_data=True,

    classifiers=[
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: POSIX',
        'Development Status :: 1 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Bio-Meidecine'
        ],
    install_requires=['bcolz>=1.2.1',
                        'pandas']
)

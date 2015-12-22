#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

import agd_tools

setup(
    name="agd_tools",
    version=agd_tools.__version__,
    author="AGD Team",
    description="Useful functions for datascience.",
    include_package_data=True,
    long_description=open('README.md').read(),
    packages=find_packages(),
    url="https://github.com/SGMAP-AGD/Tools",
    package_data={'agd_tools': ['config.ini']},
    classifiers=['Development Status :: 2 - Pre-Alpha',
                 'Programming Language :: Python :: 3'],
    install_requires=['numpy',
                      'scipy',
                      'SQLAlchemy',
                      'psycopg2',
                      'pandas',
                      'paramiko',
                      'scikit-learn >= 0.17',
                      'geographiclib',
                      ]
)

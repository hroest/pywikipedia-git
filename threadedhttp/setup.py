#!/usr/bin/env python
# -*- coding: utf-8  -*-

#
# (C) Merlijn van Deen, 2007
#
# Distributed under the terms of the MIT license
#

from setuptools import setup, find_packages
setup(
    name = "threadedhttp",
    version = "0.1",
    packages = find_packages(exclude=['ez_setup']),
    install_requires = ["httplib2"],
    platforms=['any'],
    author = "Merlijn van Deen",
    author_email = "valhallasw@arctus.nl",
    description = "httplib2-based HTTP library supporting cookies and threads",
    classifiers = filter(None, map(str.strip,
"""                 
Intended Audience :: Developers
License :: OSI Approved :: MIT License
Programming Language :: Python
Topic :: Software Development :: Libraries :: Python Modules
""".splitlines())),
    license = "MIT License",
    keywords = "thread cookie httplib2",
    url = "http://pywikipediabot.sourceforge.net",
)
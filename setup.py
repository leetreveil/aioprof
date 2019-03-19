#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re

from setuptools import setup


setup(
    name="aioprof",
    version="0.0.1",
    py_modules=['aioprof'],
    python_requires='>=3.6',
    url="https://github.com/leetreveil/aioprof",
    license="MIT",
    author="Lee Treveil",
    author_email="leetreveil@gmail.com",
    install_requires=["pyinstrument"]
)

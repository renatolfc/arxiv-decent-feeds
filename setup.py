#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

import arxivdf

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='arxiv-decent-feeds',
    version=arxivdf.__version__,
    description='Feed converer for arxiv feeds',
    long_description=long_description,
    url='https://github.com/trovao/arxiv-decent-feeds',
    author='Renato Cunha',
    author_email='erangb@erangbphaun.pbz',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 2',
    ],
    keywords='arxiv feed aggregator',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'arxivdf=arxivdf.adf:main',
        ],
    },
    install_requires=['requests', 'feedparser', 'python-dateutil', 'lxml'],
)


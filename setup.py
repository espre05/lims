#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand


# This is a plug-in for setuptools that will invoke py.test
# when you run python setup.py test
class PyTest(TestCommand):

    """Set up the py.test test runner."""

    def finalize_options(self):
        """Set options for the command line."""
        TestCommand.finalize_options(self)
        self.test_args = ['-v']
        self.test_suite = True

    def run_tests(self):
        """Execute the test runner command."""
        # Import here, because outside the required eggs aren't loaded yet
        import pytest
        sys.exit(pytest.main(self.test_args))

setup(
    name='cghq-lims',
    version='0.0.1',
    description='Microservice to interface with LIMS',
    author='Robin Andeer',
    author_email='robin.andeer@scilifelab.se',
    packages=find_packages(exclude=('tests*', 'docs', 'examples')),
    include_package_data=True,
    install_requires=[
        'Flask>=0.10',
        'Flask-Script',
        'Flask-Restful',
        'genologics',
        'requests'
    ],
    cmdclass=dict(test=PyTest),
    zip_safe=False,
    keywords='pytest flask',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
    platforms='any',
    license='BSD License',
    entry_points={
        'console_scripts': ['lims-ws = lims.cli:main']
    },
)

# coding: utf-8
import sys as _sys
import setuptools as _setup
from setuptools.command.test import test as _TestCommand


class PyTest(_TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]
    pytest_args = None
    test_args = None
    test_suite = None

    def initialize_options(self):
        _TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        _TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        _sys.exit(errno)


_setup.setup(
    name="py_vnu",
    version="0.1",
    scripts=[
        "scripts/vnu",
    ],
    py_modules=[
        "vnu",
    ],
    install_requires=[
        "requests",
    ],
    tests_require=[
        "mock",
        "pytest",
        "pytest-cov",
    ],
    cmdclass={
        "test": PyTest,
    },
    author="Roland Sommer",
    author_email="rol@ndsommer.de",
    description="Simple client for http://validator.nu/",
    license="Apache 2.0",
)

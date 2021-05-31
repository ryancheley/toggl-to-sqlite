from setuptools import setup
import os

VERSION = "0.3.0"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="toggl-to-sqlite",
    description="Create a SQLite database containing data from your Toggl account",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Ryan Cheley",
    url="https://github.com/ryancheley/toggle-to-sqlite",
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=["toggl_to_sqlite"],
    entry_points="""
        [console_scripts]
        toggl-to-sqlite=toggl_to_sqlite.cli:cli
    """,
    install_requires=["sqlite-utils>=2.4.4", "click", "requests", "requests_mock"],
    extras_require={"test": ["pytest"]},
    tests_require=["toggl-to-sqlite[test]"],
)

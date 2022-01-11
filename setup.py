import os

from setuptools import setup

VERSION = "0.6.0"


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
    project_urls={
        "Issues": "https://github.com/ryancheley/toggl-to-sqlite/issues",
        "CI": "https://github.com/ryancheley/toggl-to-sqlite/actions",
        "Changelog": "https://github.com/ryancheley/toggl-to-sqlite/releases",
        "Documentation": "https://github.com/ryancheley/toggl-to-sqlite/blob/main/README.md",
    },
    url="https://github.com/ryancheley/toggle-to-sqlite",
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=["toggl_to_sqlite"],
    package_dir={"": "src"},
    entry_points="""
        [console_scripts]
        toggl-to-sqlite=toggl_to_sqlite.cli:cli
    """,
    install_requires=["sqlite-utils>=2.4.4", "click", "requests", "requests_mock", "toml"],
    extras_require={"test": ["pytest", "black", "isort", "coverage", "mypy", "cogapp", "pre-commit"]},
    tests_require=["toggl-to-sqlite[test]"],
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Utilities",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)

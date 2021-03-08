# toggl-to-sqlite

[![PyPI](https://img.shields.io/pypi/v/toggl-to-sqlite.svg)](https://pypi.org/project/toggl-to-sqlite/)
[![GitHub changelog](https://img.shields.io/github/v/release/ryancheley/toggl-to-sqlite?include_prereleases&label=changelog)](https://github.com/ryancheley/toggl-to-sqlite/releases)
[![Tests](https://github.com/ryancheley/toggl-to-sqlite/workflows/Test/badge.svg)](https://github.com/ryancheley/toggl-to-sqlite/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/ryancheley/toggl-to-sqlite/blob/main/LICENSE)


Create a SQLite database containing data from your [Toggl](https://toggl.com/) account.

## How to install

    $ pip install toggl-to-sqlite

## Usage

You will need to first obtain a valid OAuth token for your toggl account. You can do this by running the `auth` command and following the prompts:

    $ toggl-to-sqlite auth
    You will need to get your API Token from this page

    https://track.toggl.com/profile

    Once you have your API Token enter it at the command line. 
    
    Authentication tokens written to auth.json

Now you can fetch all of your items from toggl like this:

    $ toggl-to-sqlite fetch toggl.db


## Using with Datasette

The SQLite database produced by this tool is designed to be browsed using [Datasette](https://datasette.readthedocs.io/). Use the [datasette-render-timestamps](https://github.com/simonw/datasette-render-timestamps) plugin to improve the display of the timestamp values.
# toggl-to-sqlite

[![PyPI](https://img.shields.io/pypi/v/toggl-to-sqlite.svg)](https://pypi.org/project/toggl-to-sqlite/)
[![GitHub changelog](https://img.shields.io/github/v/release/ryancheley/toggl-to-sqlite?include_prereleases&label=changelog)](https://github.com/ryancheley/toggl-to-sqlite/releases)
[![Tests](https://github.com/ryancheley/toggl-to-sqlite/workflows/Test/badge.svg)](https://github.com/ryancheley/toggl-to-sqlite/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/ryancheley/toggl-to-sqlite/blob/main/LICENSE)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/ryancheley/toggl-to-sqlite/main.svg)](https://results.pre-commit.ci/latest/github/ryancheley/toggl-to-sqlite/main)



Create a SQLite database containing data from your [Toggl](https://toggl.com/) account.

## How to install

    $ pip install toggl-to-sqlite

## Usage

You will need to first obtain a valid API token for your toggl account. You can do this by running the `auth` command and following the prompts:

    $ toggl-to-sqlite auth
    You will need to get your API Token from this page

    https://track.toggl.com/profile

    Once you have your API Token enter it at the command line.

    Authentication tokens written to auth.json

Now you can fetch all of your items from toggl like this:

    $ toggl-to-sqlite fetch toggl.db

**NB!** By default `toggl-to-sqlite` only fetches data from the 25 previous days. As an alternative you can specify to get time_entries since a specific date. You do this by specifying the `since` option:

    $ toggl-to-sqlite fetch -s 2021-03-13

You can choose to get only `time_entries`, `projects`, or `workspaces` by speciying a type in the argument like this.

To get ONLY your workspaces:

    $ toggl-to-sqlite fetch -t workspaces toggl.db

To get your workspaces and projects:

    $ toggl-to-sqlite fetch -t workspaces -t projects toggl.db

The default is to get all three of `time_entries`, `projects`, and `workspaces`

## toggl-to-sqlite --help

<!-- [[[cog
import cog
from toggl_to_sqlite import cli
from click.testing import CliRunner
runner = CliRunner()
result = runner.invoke(cli.cli, ["--help"])
help = result.output.replace("Usage: cli", "Usage: toggl-to-sqlite")
cog.out(
    "```\n{}\n```".format(help)
)
]]] -->
```
Usage: toggl-to-sqlite [OPTIONS] COMMAND [ARGS]...

  Save Toggl data to a SQLite database

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  auth   Save authentication credentials to a JSON file
  fetch  Save Toggl data to a SQLite database

```
<!-- [[[end]]] -->

## Using with Datasette

The SQLite database produced by this tool is designed to be browsed using [Datasette](https://datasette.readthedocs.io/). Use the [datasette-render-timestamps](https://github.com/simonw/datasette-render-timestamps) plugin to improve the display of the timestamp values.

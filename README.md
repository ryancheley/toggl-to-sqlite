# toggl-to-sqlite

[![PyPI](https://img.shields.io/pypi/v/toggl-to-sqlite.svg)](https://pypi.org/project/toggl-to-sqlite/)
[![GitHub changelog](https://img.shields.io/github/v/release/ryancheley/toggl-to-sqlite?include_prereleases&label=changelog)](https://github.com/ryancheley/toggl-to-sqlite/releases)
[![Tests](https://github.com/ryancheley/toggl-to-sqlite/workflows/Test/badge.svg)](https://github.com/ryancheley/toggl-to-sqlite/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/ryancheley/toggl-to-sqlite/blob/main/LICENSE)
[![Python](https://img.shields.io/badge/python-3.9+-blue)](https://pypi.org/project/toggl-to-sqlite/)
[![Code style: ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/ryancheley/toggl-to-sqlite/main.svg)](https://results.pre-commit.ci/latest/github/ryancheley/toggl-to-sqlite/main)

Save data from [Toggl](https://toggl.com/) to a SQLite database using the modern **Toggl API v9**.

## Features

- ✅ **Toggl API v9** - Uses the latest Toggl API for maximum compatibility
- ✅ **Complete Data Export** - Time entries, workspaces, and projects
- ✅ **Flexible Date Ranges** - Fetch all data or specify custom date ranges
- ✅ **SQLite Storage** - Portable, queryable database format
- ✅ **100% Test Coverage** - Reliable and well-tested codebase
- ✅ **Modern Python** - Supports Python 3.9+
- ✅ **Modern Tooling** - Built with uv, ruff, and automated versioning

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

## Development

This project uses modern Python tooling for development.

### Prerequisites

- Python 3.9+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

### Setup with uv (recommended)

```bash
git clone https://github.com/ryancheley/toggl-to-sqlite
cd toggl-to-sqlite
uv sync --extra test
```

### Setup with pip

```bash
git clone https://github.com/ryancheley/toggl-to-sqlite
cd toggl-to-sqlite
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e ".[test]"
```

### Running tests

```bash
# With uv
uv run pytest

# With pip
pytest
```

### Code quality

This project uses [ruff](https://github.com/astral-sh/ruff) for linting and formatting:

```bash
# With uv
uv run ruff check .          # Linting
uv run ruff format .         # Formatting

# With pip
ruff check .
ruff format .
```

### Version management

Versions are automatically managed using git tags:

```bash
# Create a new version
git tag v0.9.0
git push origin v0.9.0

# Or use the bump script
python bump-version.py patch  # 0.8.2 -> 0.8.3
python bump-version.py minor  # 0.8.2 -> 0.9.0
python bump-version.py major  # 0.8.2 -> 1.0.0
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for more information on contributing to this project.

## Requirements

- Python 3.9 or higher
- Valid Toggl account with API access

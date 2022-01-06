import json

import click
import sqlite_utils

from . import utils


@click.group()
@click.version_option()
def cli():
    "Save Toggl data to a SQLite database"


@cli.command()
@click.option(
    "-a",
    "--auth",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=False),
    default="auth.json",
    help="Path to save tokens to, defaults to auth.json",
)
def auth(auth):
    "Save authentication credentials to a JSON file"
    click.echo("Visit this page and sign in with your Toggl account:\n")
    click.echo("https://track.toggl.com/profile")
    api_token = input(
        "Once you have signed in there, copy your API Token at the bottom of the page, paste it here, and press <enter>: "
    )
    # Now exchange the request_token for an access_token

    open(auth, "w").write(
        json.dumps(
            {
                "api_token": api_token,
            },
            indent=4,
        )
        + "\n"
    )
    click.echo("Authentication tokens written to {}".format(auth))


@cli.command()
@click.argument(
    "db_path",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=False),
    required=True,
)
@click.option(
    "-a",
    "--auth",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=False),
    default="auth.json",
    help="Path to auth tokens, defaults to auth.json",
)
@click.option("-d", "--days", required=True, type=int, default=25)
@click.option("-s", "--since", type=click.DateTime())
@click.option(
    "-t",
    "--type",
    default=["time_entries", "workspaces", "projects"],
    required=True,
    multiple=True,
)
def fetch(db_path, auth, days, since, type):
    "Save Toggl data to a SQLite database"
    auth = json.load(open(auth))
    db = sqlite_utils.Database(db_path)
    days = days
    since = since
    if "time_entries" in type:
        time_entries = utils.get_time_entries(api_token=auth["api_token"], days=days, since=since)
        utils.save_items(time_entries, "time_entries", db)
    if "workspaces" in type:
        workspaces = utils.get_workspaces(api_token=auth["api_token"])
        utils.save_items(workspaces, "workspaces", db)
    if "projects" in type:
        projects = utils.get_projects(api_token=auth["api_token"])
        utils.save_items(projects, "projects", db)

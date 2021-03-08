import click
import json
import urllib.parse
import requests
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
    click.echo(
            "https://track.toggl.com/profile"
        )
    api_token = input(
        "Once you have signed in there, copy your API Toekn at the bottom of the page, paste it here, and press <enter>: "
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
@click.option("-a", "--all", is_flag=True, help="Fetch all items (not just new ones)")
@click.option("-s", "--silent", is_flag=True, help="Don't show progress bar")
def fetch(db_path, auth, all, silent):
    "Save Toggl data to a SQLite database"
    auth = json.load(open(auth))
    db = sqlite_utils.Database(db_path)
    fetch = utils.get_data()
    utils.save_items(fetch, db)
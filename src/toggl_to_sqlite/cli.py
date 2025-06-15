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
@click.option(
    "-d", "--days", type=int, default=25, help="Number of days to fetch (only used if no automatic since date is available)"
)
@click.option("-s", "--since", type=click.DateTime(), help="Fetch data since this date (overrides automatic since detection)")
@click.option("--force-full", is_flag=True, help="Force a full sync, ignoring previous sync times")
@click.option(
    "-t", "--type", default=["time_entries", "workspaces", "projects"], required=True, multiple=True, help="Data types to fetch"
)
def fetch(db_path, auth, days, since, force_full, type):
    "Save Toggl data to a SQLite database"
    import datetime

    auth = json.load(open(auth))
    db = sqlite_utils.Database(db_path)

    # Get current time for updating sync timestamps
    sync_time = datetime.datetime.now(datetime.timezone.utc)

    if "time_entries" in type:
        # Use automatic since detection for time entries (unless force_full is specified)
        if force_full:
            click.echo("Force full sync requested - fetching all time entries")
            effective_since = None
        else:
            effective_since = utils.get_effective_since_date(
                api_token=auth["api_token"], table_name="time_entries", db=db, user_since=since
            )

        # Only use automatic since if no explicit since date is provided
        if effective_since and not since and not force_full:
            # Convert to date for comparison if it's a datetime
            effective_date = effective_since.date() if hasattr(effective_since, "date") else effective_since
            days_since_effective = (datetime.datetime.now().date() - effective_date).days + 1  # Add 1 to ensure overlap
            click.echo(f"📅 Fetching time entries since {effective_date} ({days_since_effective} days)")
            time_entries = utils.get_time_entries(api_token=auth["api_token"], days=days_since_effective, since=effective_since)
        else:
            if since:
                since_date = since.date() if hasattr(since, "date") else since
                click.echo(f"📅 Fetching time entries since user-specified date: {since_date}")
            else:
                click.echo(f"📅 Fetching time entries for the last {days} days")
            time_entries = utils.get_time_entries(api_token=auth["api_token"], days=days, since=since)

        utils.save_items(time_entries, "time_entries", db)
        utils.update_sync_time(db, "time_entries", sync_time)

    if "workspaces" in type:
        workspaces = utils.get_workspaces(api_token=auth["api_token"])
        utils.save_items(workspaces, "workspaces", db)
        utils.update_sync_time(db, "workspaces", sync_time)

    if "projects" in type:
        projects = utils.get_projects(api_token=auth["api_token"])
        utils.save_items(projects, "projects", db)
        utils.update_sync_time(db, "projects", sync_time)

import datetime
import math

import requests
import sqlite_utils


def get_start_datetime(api_token: str, since: datetime.datetime = None) -> datetime.date:
    toggl = requests.get("https://api.track.toggl.com/api/v9/workspaces", auth=(api_token, "api_token"))
    if toggl.status_code == 200:
        data = toggl.json()
        if not since:
            start_time = data[0]["at"]
            start_time = datetime.datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S+00:00")
        else:
            start_time = since
        return start_time.date()
    else:
        return datetime.date.today()


def get_workspaces(api_token: str) -> list:
    workspaces = []
    response = requests.get("https://api.track.toggl.com/api/v9/workspaces", auth=(api_token, "api_token"))
    if response.status_code == 200:
        workspaces.append(response.json())
        for workspace in workspaces[0]:
            workspace.pop("api_token", None)
    return workspaces


def get_projects(api_token: str) -> list:
    projects = []
    workspaces = get_workspaces(api_token)
    if len(workspaces) > 0:
        for workspace in workspaces[0]:
            response = requests.get(
                f"https://api.track.toggl.com/api/v9/workspaces/{workspace['id']}/projects",
                params={"active": "both"},
                auth=(api_token, "api_token"),
            )
            project = response.json()
            if project:
                projects.append(project)
    return projects


def get_time_entries(api_token: str, days: int, since: datetime.datetime = None) -> list:
    start_date = get_start_datetime(api_token, since)
    today = datetime.date.today()
    data = []
    if days > 0:
        cycles = math.ceil((today - start_date).days / days)
        for cycle in range(cycles):
            _start_date = (start_date + datetime.timedelta(days=days) * cycle).strftime("%Y-%m-%dT00:00:00-00:00")
            _end_date = (start_date + datetime.timedelta(days=days) * (cycle + 1)).strftime("%Y-%m-%dT00:00:00-00:00")
            params = (
                ("start_date", _start_date),
                ("end_date", _end_date),
            )
            response = requests.get(
                "https://api.track.toggl.com/api/v9/me/time_entries",
                params=params,
                auth=(api_token, "api_token"),
            )
            data.append(response.json())

    return data


def save_items(items: list, table: str, db: sqlite_utils.Database) -> None:
    for item in items:
        data = item
        try:
            db[table].insert_all(data, pk="id", alter=True, replace=True)
        except AttributeError:
            print(item)


def get_last_sync_time(db: sqlite_utils.Database, table_name: str) -> datetime.datetime:
    """Get the last sync time for a specific table."""
    since_table = f"{table_name}_since"

    if since_table not in db.table_names():
        return None

    try:
        # Explicitly query for row with id=1
        rows = list(db[since_table].rows_where("id = ?", [1]))
        if not rows:
            return None
        row = rows[0]
        return datetime.datetime.fromisoformat(row["since"])
    except (sqlite_utils.db.NotFoundError, KeyError, IndexError, ValueError):
        return None


def update_sync_time(db: sqlite_utils.Database, table_name: str, sync_time: datetime.datetime) -> None:
    """Update the last sync time for a specific table."""
    since_table = f"{table_name}_since"

    db[since_table].insert({"id": 1, "since": sync_time.isoformat()}, pk="id", replace=True, alter=True)


def get_effective_since_date(
    api_token: str, table_name: str, db: sqlite_utils.Database, user_since: datetime.datetime = None
) -> datetime.datetime:
    """Get the effective 'since' date to use for fetching data.

    Priority:
    1. User-provided since parameter
    2. Last sync time from database
    3. Workspace creation date (fallback)
    """
    if user_since:
        return user_since

    # Check for last sync time
    last_sync = get_last_sync_time(db, table_name)
    if last_sync:
        return last_sync

    # Fallback to workspace creation date
    return get_start_datetime(api_token)

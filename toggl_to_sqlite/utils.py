import requests
import json
import datetime
import math


def get_start_datetime(api_token, since: datetime = None):
    toggl = requests.get(
        "https://api.track.toggl.com/api/v8/me", auth=(api_token, "api_token")
    )
    if toggl.status_code == 200:
        data = json.loads(toggl.text)
        if not since:
            start_time = data["data"]["workspaces"][0]["at"]
            start_time = datetime.datetime.strptime(
                start_time, "%Y-%m-%dT%H:%M:%S+00:00"
            )
        else:
            start_time = since
        return start_time.date()
    else:
        return datetime.date.today()


def get_workspaces(api_token):
    workspaces = []
    response = requests.get(
        "https://api.track.toggl.com/api/v8/workspaces", auth=(api_token, "api_token")
    )
    if response.status_code == 200:
        workspaces.append(json.loads(response.text))
    return workspaces


def get_projects(api_token):
    projects = []
    workspaces = get_workspaces(api_token)
    if len(workspaces) > 0:
        for workspace in workspaces[0]:
            response = requests.get(
                f'https://api.track.toggl.com/api/v8/workspaces/{workspace["id"]}/projects',
                auth=(api_token, "api_token"),
            )
            project = json.loads(response.text)
            if project:
                projects.append(project)
    return projects


def get_time_entries(api_token, days, since: datetime = None):
    start_date = get_start_datetime(api_token, since)
    today = datetime.date.today()
    data = []
    if days > 0:
        cycles = math.ceil((today - start_date).days / days)
        for cycle in range(cycles):
            _start_date = (start_date + datetime.timedelta(days=days) * cycle).strftime(
                "%Y-%m-%dT00:00:00-00:00"
            )
            _end_date = (
                start_date + datetime.timedelta(days=days) * (cycle + 1)
            ).strftime("%Y-%m-%dT00:00:00-00:00")
            params = (
                ("start_date", _start_date),
                ("end_date", _end_date),
            )
            response = requests.get(
                "https://api.track.toggl.com/api/v8/time_entries",
                params=params,
                auth=(api_token, "api_token"),
            )
            data.append(json.loads(response.text))

    return data


def save_items(items, table, db):
    for item in items:
        data = item
        db[table].insert_all(data, pk="id", alter=True, replace=True)

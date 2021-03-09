import requests
import json
import datetime
import math


try:
    with open("auth.json", "r") as f:
        auth = json.load(f)

    API_TOKEN = auth["api_token"]
except FileNotFoundError:
    pass


def get_start_datetime():
    toggl = requests.get(
        "https://api.track.toggl.com/api/v8/me", auth=(API_TOKEN, "api_token")
    )
    data = json.loads(toggl.text)
    start_time = data["data"]["workspaces"][0]["at"]
    start_time = datetime.datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S+00:00")
    return start_time.date()


def get_workspaces():
    workspaces = []
    response = requests.get('https://api.track.toggl.com/api/v8/workspaces', auth=(API_TOKEN, 'api_token'))
    workspaces.append(json.loads(response.text))
    return workspaces
    

def get_projects():
    projects = []
    workspaces = get_workspaces()
    for workspace in workspaces[0]:
        response = requests.get(f'https://api.track.toggl.com/api/v8/workspaces/{workspace["id"]}/projects', auth=(API_TOKEN, 'api_token'))
        project = json.loads(response.text)
        if project:
            projects.append(project)
    return projects


def get_time_entries(days=100):
    start_date = get_start_datetime()
    today = datetime.date.today()
    cycles = math.ceil((today - start_date).days / days)

    data = []

    for cycle in range(cycles):
        _start_date = (start_date + datetime.timedelta(days=days) * cycle).strftime(
            "%Y-%m-%dT00:00:00-00:00"
        )
        _end_date = (start_date + datetime.timedelta(days=days) * (cycle + 1)).strftime(
            "%Y-%m-%dT00:00:00-00:00"
        )
        params = (
            ("start_date", _start_date),
            ("end_date", _end_date),
        )
        response = requests.get(
            "https://api.track.toggl.com/api/v8/time_entries",
            params=params,
            auth=(API_TOKEN, "api_token"),
        )
        data.append(json.loads(response.text))
    return data


def save_items(items, table, db):
    for item in items:
        data = item
        db[table].insert_all(data, pk="id", alter=True, replace=True)


def transform(item):
    for key in (
        "id",
        "pid",
        "tid",
        "uid",
        "dur",
        "billable",
    ):
        if key in item:
            item[key] = int(item[key])

import datetime
import json
import pathlib

import pytest
import requests
import sqlite_utils
from test_classes import (
    MockResponseGetStartDateTime,
    MockResponseWorkspaces,
    MockTimeEntryResponse,
)

from toggl_to_sqlite.utils import (
    get_projects,
    get_start_datetime,
    get_time_entries,
    get_workspaces,
    save_items,
)


def load():
    json_path = pathlib.Path(__file__).parent / "toggl.json"
    return json.load(open(json_path, "r"))


@pytest.fixture(scope="session")
def converted():
    db = sqlite_utils.Database(":memory:")
    save_items(load(), "time_entries", db)
    return db


def test_tables(converted):
    assert {"time_entries"} == set(converted.table_names())


def test_item(converted):
    item = list(converted["time_entries"].rows)[0]
    print(item)
    assert {
        "id": 436691234,
        "wid": 777,
        "pid": 123,
        "billable": 1,
        "start": "2013-03-11T11:36:00+00:00",
        "stop": "2013-03-11T15:36:00+00:00",
        "duration": 14400,
        "description": "Meeting with the client",
        "tags": '["tag1, tag2"]',
        "at": "2013-03-11T15:36:58+00:00",
    } == item


def test_get_time_entries(monkeypatch):
    api_token = "fake_api"
    days = 10

    def mock_get(*args, **kwargs):
        return MockTimeEntryResponse(200)

    def mock_get_start_datetime(api_token=api_token, days=days):
        return datetime.date(2022, 1, 1)

    monkeypatch.setattr(requests, "get", mock_get)
    monkeypatch.setattr("toggl_to_sqlite.utils.get_start_datetime", mock_get_start_datetime)
    actual = get_time_entries(api_token=api_token, days=days)
    expected = [
        [
            {
                "id": 2306806385,
                "guid": "e13d9d8b6aee8c8363c80608a93d9bfd",
                "wid": 3829545,
                "pid": 157777117,
                "billable": False,
                "start": "2022-01-03T16:00:00+00:00",
                "stop": "2022-01-04T00:00:00+00:00",
                "duration": 28800,
                "description": "PTO",
                "duronly": False,
                "at": "2021-12-28T22:58:14+00:00",
                "uid": 2611584,
            },
            {
                "id": 2311598789,
                "guid": "58ea59f21eb26166195bd887dc2f2270",
                "wid": 3829545,
                "pid": 155736600,
                "billable": False,
                "start": "2022-01-04T15:57:15+00:00",
                "stop": "2022-01-04T16:01:07+00:00",
                "duration": 232,
                "description": "Email",
                "duronly": False,
                "at": "2022-01-04T16:01:07+00:00",
                "uid": 2611584,
            },
            {
                "id": 2311606757,
                "guid": "d50f74fb306ba0d9a79b68975e1fe5d0",
                "wid": 3829545,
                "pid": 155736600,
                "billable": False,
                "start": "2022-01-04T16:01:07+00:00",
                "stop": "2022-01-04T16:28:16+00:00",
                "duration": 1629,
                "description": "Computer Restart",
                "duronly": False,
                "at": "2022-01-04T16:28:16+00:00",
                "uid": 2611584,
            },
        ]
    ]
    assert actual[0] == expected[0]


def test_get_projects(monkeypatch):
    api_token = "fake_api"

    def mock_get(*args, **kwargs):
        return MockResponseWorkspaces(200)

    def mock_get_workspaces(api_token=api_token):
        return [[{"id": 1806100}]]

    monkeypatch.setattr(requests, "get", mock_get)
    monkeypatch.setattr("toggl_to_sqlite.utils.get_workspaces", mock_get_workspaces)
    expected = [
        [
            {
                "id": 1,
                "name": "TEST workspace",
                "profile": 0,
                "premium": False,
                "admin": True,
                "default_hourly_rate": 0,
                "default_currency": "USD",
                "only_admins_may_create_projects": False,
                "only_admins_see_billable_rates": False,
                "only_admins_see_team_dashboard": False,
                "projects_billable_by_default": True,
                "rounding": 1,
                "rounding_minutes": 0,
                "api_token": "fake_api",
                "at": "2016-12-15T06:53:39+00:00",
                "ical_enabled": True,
            }
        ]
    ]
    actual = get_projects(api_token=api_token)
    assert actual == expected


def test_get_workspaces(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockResponseWorkspaces(200)

    api_token = "fake_api"
    monkeypatch.setattr(requests, "get", mock_get)
    actual = get_workspaces(api_token=api_token)
    assert "api_token" not in actual[0][0].keys()


def test_get_start_datetime_no_since_passed_with_response(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockResponseGetStartDateTime(200)

    api_token = "fake_api"
    monkeypatch.setattr(requests, "get", mock_get)
    expected = datetime.date(2019, 12, 4)
    actual = get_start_datetime(api_token=api_token)
    assert actual == expected


def test_get_start_datetime_no_since_passed_with_no_response(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockResponseGetStartDateTime(404)

    api_token = "fake_api"
    monkeypatch.setattr(requests, "get", mock_get)
    expected = datetime.date.today()
    actual = get_start_datetime(api_token=api_token)
    assert actual == expected


def test_get_start_datetime_since_passed_with_response(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockResponseGetStartDateTime(200)

    api_token = "fake_api"
    since = datetime.datetime(2020, 3, 13)
    monkeypatch.setattr(requests, "get", mock_get)
    expected = datetime.date(2020, 3, 13)
    actual = get_start_datetime(api_token=api_token, since=since)
    assert actual == expected


def test_get_start_datetime_since_passed_with_no_response(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockResponseGetStartDateTime(404)

    api_token = "fake_api"
    since = datetime.datetime.now()
    monkeypatch.setattr(requests, "get", mock_get)
    expected = datetime.date.today()
    actual = get_start_datetime(api_token=api_token, since=since)
    assert actual == expected

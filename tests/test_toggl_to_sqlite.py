import datetime
import json
import pathlib

import pytest
import requests_mock
import sqlite_utils

from toggl_to_sqlite import utils


def load():
    json_path = pathlib.Path(__file__).parent / "toggl.json"
    return json.load(open(json_path, "r"))


@pytest.fixture(scope="session")
def converted():
    db = sqlite_utils.Database(":memory:")
    utils.save_items(load(), "time_entries", db)
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


def test_get_start_datetime_bad_api_token():
    api_token = "api_token"
    start_date = utils.get_start_datetime(api_token=api_token)
    assert start_date == datetime.date.today()


def test_get_workspaces_bad_api_token():
    api_token = "api_token"
    workspaces = utils.get_workspaces(api_token=api_token)
    assert workspaces == []


def test_get_projects_bad_api():
    api_token = "api_token"
    actual = utils.get_projects(api_token=api_token)
    expected = []
    assert actual == expected


def test_get_projects_good_api(monkeypatch):
    execpted_projects = [{"id": 1}]

    def mock_get_workspaces(api_token):
        return [[{"id": 1}]]

    monkeypatch.setattr(utils, "get_workspaces", mock_get_workspaces)

    with requests_mock.Mocker() as rm:
        return_value = {"id": 1}
        rm.get(
            "https://api.track.toggl.com/api/v8/workspaces/1/projects",
            status_code=200,
            json=return_value,
        )
        response = utils.get_projects("api_token")

    assert execpted_projects == response


def test_get_time_entries_bad_api():
    api_token = "api_token"
    actual = utils.get_time_entries(api_token=api_token, days=25)
    expected = []
    assert actual == expected


def test_get_get_workspaces():
    expected_workspaces = [
        {
            "data": [
                {
                    "id": 3134975,
                    "name": "John's personal ws",
                    "default_hourly_rate": 50,
                    "default_currency": "USD",
                    "rounding": 1,
                    "rounding_minutes": 15,
                    "at": "2013-08-28T16:22:21+00:00",
                    "logo_url": "my_logo.png",
                },
                {
                    "id": 777,
                    "name": "My Company Inc",
                    "default_hourly_rate": 40,
                    "default_currency": "EUR",
                    "rounding": 1,
                    "rounding_minutes": 15,
                    "at": "2013-08-28T16:22:21+00:00",
                },
            ]
        }
    ]
    with requests_mock.Mocker() as rm:
        return_value = {
            "data": [
                {
                    "id": 3134975,
                    "name": "John's personal ws",
                    "default_hourly_rate": 50,
                    "default_currency": "USD",
                    "rounding": 1,
                    "rounding_minutes": 15,
                    "at": "2013-08-28T16:22:21+00:00",
                    "logo_url": "my_logo.png",
                },
                {
                    "id": 777,
                    "name": "My Company Inc",
                    "default_hourly_rate": 40,
                    "default_currency": "EUR",
                    "rounding": 1,
                    "rounding_minutes": 15,
                    "at": "2013-08-28T16:22:21+00:00",
                },
            ]
        }
        rm.get(
            "https://api.track.toggl.com/api/v8/workspaces",
            status_code=200,
            json=return_value,
        )
        response = utils.get_workspaces("api_token")
    assert response == expected_workspaces


def test_get_start_datetime_with_good_api_token_and_since():
    expected_start_time = datetime.datetime(2021, 4, 1, 0, 0)
    with requests_mock.Mocker() as rm:
        return_value = {
            "data": {
                "description": "New time entry",
                "start": "2013-02-12T15:35:47+02:00",
                "wid": 31366,
                "pid": 9012,
                "duration": 1200,
                "stop": "2013-02-12T15:35:57+02:00",
                "tags": ["billed"],
                "id": 4269795,
                "workspaces": [{"at": "2021-01-01T15:35:47+00:00"}],
            }
        }
        rm.get("https://api.track.toggl.com/api/v8/me", status_code=200, json=return_value)

        response = utils.get_start_datetime("api_token", expected_start_time)
        assert response == expected_start_time.date()


def test_get_start_datetime_with_good_api_token_and_blank_since():
    expected_start_time = datetime.date(2021, 1, 1)
    with requests_mock.Mocker() as rm:
        return_value = {
            "data": {
                "description": "New time entry",
                "start": "2013-02-12T15:35:47+02:00",
                "wid": 31366,
                "pid": 9012,
                "duration": 1200,
                "stop": "2013-02-12T15:35:57+02:00",
                "tags": ["billed"],
                "id": 4269795,
                "workspaces": [{"at": "2021-01-01T15:35:47+00:00"}],
            }
        }
        rm.get("https://api.track.toggl.com/api/v8/me", status_code=200, json=return_value)

        response = utils.get_start_datetime("api_token")
    print(response)

    assert response == expected_start_time

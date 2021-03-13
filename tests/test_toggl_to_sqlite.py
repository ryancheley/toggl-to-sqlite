from toggl_to_sqlite import utils
import pytest
import json
import sqlite_utils
from sqlite_utils.db import ForeignKey
import pathlib
import requests
import datetime
import random


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
    # assert 1 == 0
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


def test_get_time_entries_bad_api():
    api_token = "api_token"
    actual = utils.get_time_entries(api_token=api_token, days=25)
    expepected = []
    assert actual == expepected


def test_get_time_entries_bad_days():
    """
        This will work with either a valid or invalid token
    """
    days = random.randrange(-100, 0)
    print(days)
    api_token = "api_token"
    actual = utils.get_time_entries(api_token=api_token, days=days)
    expepected = []
    assert actual == expepected
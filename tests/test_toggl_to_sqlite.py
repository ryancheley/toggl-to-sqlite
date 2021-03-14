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


def test_get_start_datetime_good_api_token_blank_since(monkeypatch):
    def mockreturn(api_token):
        return datetime.date(2019, 12, 4)

    monkeypatch.setattr(utils, "get_start_datetime", mockreturn)    

    x = datetime.date(2019, 12, 4)
    assert x == utils.get_start_datetime("api_token")


def test_get_start_datetime_good_api_token_non_blank_since(monkeypatch):
    def mockreturn(api_token, since):
        return datetime.date(2020, 12, 4)

    monkeypatch.setattr(utils, "get_start_datetime", mockreturn)    

    since = datetime.date(2020, 12, 4)
    assert since == utils.get_start_datetime("api_token", "since")


def test_get_workspaces_good_api_token(monkeypatch):
    def mockreturn(api_token):
        workspace = [
                        [
                            {
                                'id': 0, 
                                'name': "My workspace", 
                                'profile': 0, 
                                'premium': False, 
                                'admin': True, 
                                'default_hourly_rate': 0, 
                                'default_currency': 'USD', 
                                'only_admins_may_create_projects': False, 
                                'only_admins_see_billable_rates': False, 
                                'only_admins_see_team_dashboard': False, 
                                'projects_billable_by_default': True, 
                                'rounding': 1, 
                                'rounding_minutes': 0, 
                                'api_token': 'api_token', 
                                'at': '2016-12-15T06:53:39+00:00', 
                                'ical_enabled': True
                            },
                        ]
        ]
        return workspace

    monkeypatch.setattr(utils, "get_workspaces", mockreturn)    

    expected_workspace =         workspace = [
                        [
                            {
                                'id': 0, 
                                'name': "My workspace", 
                                'profile': 0, 
                                'premium': False, 
                                'admin': True, 
                                'default_hourly_rate': 0, 
                                'default_currency': 'USD', 
                                'only_admins_may_create_projects': False, 
                                'only_admins_see_billable_rates': False, 
                                'only_admins_see_team_dashboard': False, 
                                'projects_billable_by_default': True, 
                                'rounding': 1, 
                                'rounding_minutes': 0, 
                                'api_token': 'api_token', 
                                'at': '2016-12-15T06:53:39+00:00', 
                                'ical_enabled': True
                            },
                        ]
        ]

    assert utils.get_workspaces("api_token") == expected_workspace


def test_get_projects_good_api(monkeypatch):
    def mockreturn(api_token):
        return [
            [
                {
                    'id': 1, 
                    'wid': 2, 
                    'name': 'Project', 
                    'billable': False, 
                    'is_private': True, 
                    'active': True, 
                    'template': False, 
                    'at': '2020-06-09T04:02:21+00:00', 
                    'created_at': '2019-12-04T05:02:20+00:00', 
                    'color': '0', 
                    'auto_estimates': False, 
                    'actual_hours': 42, 
                    'hex_color': '#0b83d9'
                }
            ]
        ]

    monkeypatch.setattr(utils, "get_projects", mockreturn)    

    expected_projects = [
            [
                {
                    'id': 1, 
                    'wid': 2, 
                    'name': 'Project', 
                    'billable': False, 
                    'is_private': True, 
                    'active': True, 
                    'template': False, 
                    'at': '2020-06-09T04:02:21+00:00', 
                    'created_at': '2019-12-04T05:02:20+00:00', 
                    'color': '0', 
                    'auto_estimates': False, 
                    'actual_hours': 42, 
                    'hex_color': '#0b83d9'
                }
            ]
        ]
    assert expected_projects == utils.get_projects("api_token")


def test_get_time_entries_since_in_the_future(monkeypatch):
    def mockreturn(api_token, days, since):
        return []

    monkeypatch.setattr(utils, "get_time_entries", mockreturn)    

    x = []
    assert x == utils.get_time_entries("api_token", "days", "since")

def test_get_time_entries_good_api(monkeypatch):
    def mockreturn(api_token, days):
        return [
            [
                {
                    'id': 1, 
                    'guid': 'itsameemailadminsitration', 
                    'wid': 1, 
                    'pid': 1, 
                    'billable': False, 
                    'start': '2019-12-04T15:18:28+00:00', 
                    'stop': '2019-12-04T15:28:37+00:00', 
                    'duration': 42, 
                    'description': 'Email', 
                    'tags': ['Email'], 
                    'duronly': False, 
                    'at': '2019-12-05T03:04:29+00:00', 
                    'uid': 1
                }
            ]
        ]

    monkeypatch.setattr(utils, "get_time_entries", mockreturn)    

    x = [
            [
                {
                    'id': 1, 
                    'guid': 'itsameemailadminsitration', 
                    'wid': 1, 
                    'pid': 1, 
                    'billable': False, 
                    'start': '2019-12-04T15:18:28+00:00', 
                    'stop': '2019-12-04T15:28:37+00:00', 
                    'duration': 42, 
                    'description': 'Email', 
                    'tags': ['Email'], 
                    'duronly': False, 
                    'at': '2019-12-05T03:04:29+00:00', 
                    'uid': 1
                }
            ]
        ]
    assert x == utils.get_time_entries("api_token", "days")
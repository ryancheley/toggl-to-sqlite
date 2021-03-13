from toggl_to_sqlite import utils
import pytest
import json
import sqlite_utils
from sqlite_utils.db import ForeignKey
import pathlib
import requests
import datetime
import random


def load_auth():
    json_path = pathlib.Path(__file__).parents[1] / "auth.json"
    return json.load(open(json_path, "r"))

API_TOKEN = load_auth()['api_token']

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

def test_get_start_datetime_good_api_token_blank_since():
    """
        Need to figure out how to mock this
    """
    api_token = API_TOKEN
    start_date = utils.get_start_datetime(api_token=api_token)
    assert start_date == datetime.date(2019, 12, 4)


def test_get_start_datetime_good_api_token_non_blank_since():
    """
        Need to figure out how to mock this
    """
    api_token = API_TOKEN
    since = datetime.datetime(2020,12,4)
    start_date = utils.get_start_datetime(api_token=api_token, since=since)
    assert start_date == since.date()


def test_get_workspaces_bad_api_token():
    api_token = "api_token"
    workspaces = utils.get_workspaces(api_token=api_token)
    assert workspaces == []

def test_get_workspaces_good_api_token():
    """
        Need to figure out how to mock this
    """
    api_token = API_TOKEN
    actual = utils.get_workspaces(api_token=api_token)
    expected = [[{'id': 1806100, 'name': "Rcheley's workspace", 'profile': 0, 'premium': False, 'admin': True, 'default_hourly_rate': 0, 'default_currency': 'USD', 'only_admins_may_create_projects': False, 'only_admins_see_billable_rates': False, 'only_admins_see_team_dashboard': False, 'projects_billable_by_default': True, 'rounding': 1, 'rounding_minutes': 0, 'api_token': '775c077edcdd0935c38cbfff99bbca96', 'at': '2016-12-15T06:53:39+00:00', 'ical_enabled': True}, {'id': 3829545, 'name': 'DOHC Business Informatics', 'profile': 101, 'premium': True, 'admin': True, 'default_hourly_rate': 0, 'default_currency': 'USD', 'only_admins_may_create_projects': False, 'only_admins_see_billable_rates': False, 'only_admins_see_team_dashboard': False, 'projects_billable_by_default': True, 'rounding': 1, 'rounding_minutes': 0, 'api_token': 'efb896083b906202d81d1fb78b69c313', 'at': '2019-12-04T05:14:38+00:00', 'logo_url': 'https://assets.toggl.com/images/workspace.jpg', 'ical_url': '/ical/workspace_user/df8d9fa987994f84f4f770d799c72e01', 'ical_enabled': True}]]
    assert expected == actual


def test_get_projects_bad_api():
    api_token = "api_token"
    actual = utils.get_projects(api_token=api_token)
    expected = []
    assert actual == expected


def test_get_projects_good_api():
    """
        Need to figure out how to mock this
    """
    api_token = API_TOKEN
    actual = utils.get_projects(api_token=api_token)
    expected = [[{'id': 155736600, 'wid': 3829545, 'name': 'Administration', 'billable': False, 'is_private': True, 'active': True, 'template': False, 'at': '2020-06-09T04:02:21+00:00', 'created_at': '2019-12-04T05:02:20+00:00', 'color': '0', 'auto_estimates': False, 'actual_hours': 1113, 'hex_color': '#0b83d9'}, {'id': 157266743, 'wid': 3829545, 'name': 'Commuting', 'billable': False, 'is_private': True, 'active': True, 'template': False, 'at': '2020-06-09T04:07:28+00:00', 'created_at': '2020-02-15T16:58:36+00:00', 'color': '14', 'auto_estimates': False, 'actual_hours': 2, 'hex_color': '#525266'}, {'id': 155771467, 'wid': 3829545, 'name': 'Exercise', 'billable': False, 'is_private': True, 'active': True, 'template': False, 'at': '2020-06-09T04:02:33+00:00', 'created_at': '2019-12-05T13:55:29+00:00', 'color': '11', 'auto_estimates': False, 'actual_hours': 9, 'hex_color': '#566614'}, {'id': 157105935, 'wid': 3829545, 'name': 'Family Time', 'billable': False, 'is_private': True, 'active': True, 'template': False, 'at': '2020-06-09T04:07:18+00:00', 'created_at': '2020-02-10T00:59:21+00:00', 'color': '6', 'auto_estimates': False, 'currency': 'USD', 'hex_color': '#06a893'}, {'id': 155736594, 'wid': 3829545, 'name': 'Issue work', 'billable': False, 'is_private': True, 'active': True, 'template': False, 'at': '2020-06-09T04:02:21+00:00', 'created_at': '2019-12-04T05:02:02+00:00', 'color': '12', 'auto_estimates': False, 'actual_hours': 462, 'hex_color': '#991102'}, {'id': 155736597, 'wid': 3829545, 'name': 'Meeting Prep', 'billable': False, 'is_private': True, 'active': True, 'template': False, 'at': '2020-06-09T04:02:21+00:00', 'created_at': '2019-12-04T05:02:09+00:00', 'color': '6', 'auto_estimates': False, 'actual_hours': 60, 'hex_color': '#06a893'}, {'id': 155736591, 'wid': 3829545, 'name': 'Meetings', 'billable': False, 'is_private': True, 'active': True, 'template': False, 'at': '2020-06-09T04:02:21+00:00', 'created_at': '2019-12-04T05:01:50+00:00', 'color': '8', 'auto_estimates': False, 'actual_hours': 1049, 'hex_color': '#465bb3'}, {'id': 155980477, 'wid': 3829545, 'name': 'Personal', 'billable': False, 'is_private': True, 'active': True, 'template': False, 'at': '2020-06-09T04:03:35+00:00', 'created_at': '2019-12-17T14:47:48+00:00', 'color': '13', 'auto_estimates': False, 'actual_hours': 232, 'hex_color': '#d92b2b'}, {'id': 157777117, 'wid': 3829545, 'name': 'PTO', 'billable': False, 'is_private': True, 'active': True, 'template': False, 'at': '2020-06-09T04:09:52+00:00', 'created_at': '2020-03-06T13:50:25+00:00', 'color': '14', 'auto_estimates': False, 'actual_hours': 27, 'hex_color': '#525266'}, {'id': 157105842, 'wid': 3829545, 'name': 'Reading', 'billable': False, 'is_private': True, 'active': True, 'template': False, 'at': '2020-06-09T04:07:18+00:00', 'created_at': '2020-02-10T00:48:16+00:00', 'color': '7', 'auto_estimates': False, 'currency': 'USD', 'hex_color': '#c9806b'}, {'id': 155736593, 'wid': 3829545, 'name': 'Team Development', 'billable': False, 'is_private': True, 'active': True, 'template': False, 'at': '2020-06-09T04:02:21+00:00', 'created_at': '2019-12-04T05:01:57+00:00', 'color': '10', 'auto_estimates': False, 'actual_hours': 16, 'hex_color': '#c7af14'}, {'id': 155932445, 'wid': 3829545, 'name': 'Watching Videos', 'billable': False, 'is_private': True, 'active': True, 'template': False, 'at': '2020-06-09T04:03:32+00:00', 'created_at': '2019-12-15T02:31:58+00:00', 'color': '14', 'auto_estimates': False, 'hex_color': '#525266'}, {'id': 157105845, 'wid': 3829545, 'name': 'Writing Code', 'billable': False, 'is_private': True, 'active': True, 'template': False, 'at': '2020-06-09T04:07:18+00:00', 'created_at': '2020-02-10T00:48:25+00:00', 'color': '13', 'auto_estimates': False, 'currency': 'USD', 'hex_color': '#d92b2b'}]]
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



def test_get_time_entries_good_api():
    """
        Need to figure out how to mock this
    """
    api_token = API_TOKEN
    actual = utils.get_time_entries(api_token=api_token, days=25)
    assert len(actual) == 19


def test_get_time_entries_since_in_the_future():
    since = since = datetime.datetime.today() + datetime.timedelta(days=1)
    api_token = API_TOKEN
    actual = utils.get_time_entries(api_token=api_token, days=25, since=since)
    assert len(actual) == 0

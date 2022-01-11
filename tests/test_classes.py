class MockResponseGetStartDateTime:
    def __init__(self, status_code) -> None:
        self.status_code = status_code

    @staticmethod
    def json():
        return {"data": {"workspaces": [{"at": "2019-12-04T05:14:38+00:00"}]}}


class MockResponseWorkspaces:
    def __init__(self, status_code) -> None:
        self.status_code = status_code

    @staticmethod
    def json():
        return [
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


class MockTimeEntryResponse:
    def __init__(self, status_code) -> None:
        self.status_code = status_code

    @staticmethod
    def json():
        return [
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

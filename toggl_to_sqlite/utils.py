import requests
import json
import datetime
import math


try: 
    with open('auth.json', 'r') as f:
        auth = json.load(f)

    API_TOKEN = auth['api_token']
except FileNotFoundError:
    pass


def get_start_datetime():
    toggl = requests.get('https://api.track.toggl.com/api/v8/me', auth=(API_TOKEN, 'api_token'))
    data = json.loads(toggl.text)
    start_time = data['data']['workspaces'][0]['at']
    start_time = datetime.datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S+00:00')
    return start_time.date()

def get_workspace_ids():
    toggl = requests.get('https://api.track.toggl.com/api/v8/me', auth=(API_TOKEN, 'api_token'))
    data = json.loads(toggl.text)
    workspace_id = data['data']['workspaces'][0]['id']
    return workspace_id

def get_data(days=100):
    workspace_id = get_workspace_ids()
    start_date = get_start_datetime()
    end_date = start_date + datetime.timedelta(days=100)
    today = datetime.date.today()
    cycles = math.ceil((today - start_date ).days / days)
    
    data = []

    for cycle in range(cycles):
        params = (
            ('workspace_id', workspace_id),
            ('since', start_date + datetime.timedelta(days=100)*cycle),
            ('until', start_date + datetime.timedelta(days=100)*(cycle+1)),
            ('user_agent', 'api_test'),
        )
        response = requests.get('https://api.track.toggl.com/reports/api/v2/details', params=params, auth=(API_TOKEN, 'api_token'))
        data.append(json.loads(response.text))
    return data


def save_items(items, db):
    for item in items:
        transform(item)
        db["items"].insert(item, pk="item_id", alter=True, replace=True)


def transform(item):
    for key in (
        'id', 
        'pid', 
        'tid', 
        'uid', 
        'dur', 
        'billable', 
    ):
        if key in item:
            item[key] = int(item[key])


class FetchItems:
    def __init__(self, auth, since=None, page_size=500, sleep=2, retry_sleep=3, record_since=None):
        self.auth = auth
        self.since = since
        self.page_size = page_size
        self.sleep = sleep
        self.retry_sleep = retry_sleep
        self.record_since = record_since

    def __iter__(self):
        offset = 0
        retries = 0
        while True:
            args = {
                "consumer_key": self.auth["pocket_consumer_key"],
                "access_token": self.auth["pocket_access_token"],
                "sort": "oldest",
                "state": "all",
                "detailType": "complete",
                "count": self.page_size,
                "offset": offset,
            }
            if self.since is not None:
                args["since"] = self.since
            response = requests.get("https://getpocket.com/v3/get", args)
            if response.status_code == 503 and retries < 5:
                print("Got a 503, retrying...")
                retries += 1
                time.sleep(retries * self.retry_sleep)
                continue
            else:
                retries = 0
            response.raise_for_status()
            page = response.json()
            items = list((page["list"] or {}).values())
            next_since = page["since"]
            if self.record_since and next_since:
                self.record_since(next_since)
            if not items:
                break
            yield from items
            offset += self.page_size
            if self.sleep:
                time.sleep(self.sleep)
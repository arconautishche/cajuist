import json
import os
from datetime import date, datetime, time, timedelta, timezone

import requests
from dotenv import load_dotenv

from model.worked_day import Task

load_dotenv()
api_token = os.getenv('TOGGL_TOKEN')

print(date.today().isoformat())

def load_time_entries(entries_day: date):
    start_of_day = datetime.combine(entries_day, time(), tzinfo=timezone.utc)
    end_of_day = start_of_day + timedelta(hours=23)

    dates = {
        'start_date': start_of_day.isoformat(),
        'end_date' : end_of_day.isoformat()
        }

    r = requests.get(
        'https://www.toggl.com/api/v8/time_entries',
        auth=(api_token, 'api_token'),
        params=dates
        )

    if r.status_code == 200:
        return __grouped(r.json())

    return None

def __grouped(toggl_time_entries_json):
    tasks = []
    for toggl_entry in toggl_time_entries_json:
        workorder = __extract_workorder(toggl_entry)
        activity = __extract_activity(toggl_entry)
        description = __extract_description(toggl_entry)
        duration = __extract_duration(toggl_entry)

        task = Task(workorder, activity, description, duration)
        tasks.append(task)

def __extract_description(toggle_entry):
    pass

def __extract_workorder(toggle_entry):
    pass

def __extract_activity(toggle_entry):
    pass

def __extract_duration(toggle_entry):
    pass

if __name__ == '__main__':
    time_entries = load_time_entries(date(year=2020, month=4, day=30))
    with open('toggl_export.json', 'w') as f:
        json.dump(time_entries, f, indent=4)

import json
import os
from datetime import date, datetime, time, timedelta, timezone

import requests
from dotenv import load_dotenv

load_dotenv()
api_token = os.getenv('TOGGL_TOKEN')

projects = {}

def load_time_entries(entries_day: date):
    print('-- ⏲ IMPORTING FROM TOGGL ⏲ --')
    start_of_day = datetime.combine(entries_day, time(), tzinfo=timezone.utc)
    end_of_day = start_of_day + timedelta(hours=23)

    dates = {
        'start_date': start_of_day.isoformat(),
        'end_date' : end_of_day.isoformat()
        }

    r = requests.get(
        'https://api.toggl.com/api/v8/time_entries',
        auth=(api_token, 'api_token'),
        params=dates
        )

    if r.status_code == 200:
        return __tasks_from_toggl_entries(r.json())

    return []

def __load_projects():
    workspace_id = 3405699 # TODO: safe for personal use, but not really nice
    r = requests.get(
        f'https://api.toggl.com/api/v8/workspaces/{workspace_id}/projects',
        auth=(api_token, 'api_token')
        )

    for proj in r.json():
        projects[proj['id']] = proj['name']

def __tasks_from_toggl_entries(toggl_time_entries_json):
    tasks = []
    for toggl_entry in toggl_time_entries_json:
        new_task = dict(
            workorder = __extract_workorder(toggl_entry),
            activity = __extract_activity(toggl_entry),
            description = __extract_description(toggl_entry),
            hours = __extract_duration(toggl_entry)
        )

        if new_task['hours'] < 0:
            raise Exception(f'Toggle task "{new_task["description"]}" has negative hours, still running?')

        matching_task = next((t for t in tasks if __matching_task(t, new_task)), None)
        if matching_task:
            matching_task['hours'] += new_task['hours']
        else:
            tasks.append(new_task)

    return tasks

def __extract_description(toggle_entry):
    return toggle_entry['description']

def __extract_workorder(toggle_entry):
    return projects[toggle_entry['pid']]

def __extract_activity(toggle_entry):
    if 'tags' in toggle_entry:
        return toggle_entry['tags'][0]

    return None

def __extract_duration(toggle_entry):
    return toggle_entry['duration'] / 3600

def __matching_task(task1, task2):
    if task1['workorder'] == task2['workorder']:
        if task1['activity'] == task2['activity']:
            if task1['description'] == task2['description']:
                return True

    return False

__load_projects()

if __name__ == '__main__':
    time_entries = load_time_entries(date(year=2020, month=4, day=30))
    with open('toggl_export.json', 'w') as f:
        json.dump(time_entries, f, indent=4)

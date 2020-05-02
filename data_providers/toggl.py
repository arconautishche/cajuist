import json
import os
import re
from datetime import date, datetime, time, timedelta, timezone

import requests
from dotenv import load_dotenv

from model.worked_day import Task

load_dotenv()
api_token = os.getenv('TOGGL_TOKEN')

projects = {}

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
        return __tasks_from_toggl_entries(r.json())

    return []

def __load_projects():
    workspace_id = 3405699 # TODO: safe for personal use, but not really nice
    r = requests.get(
        f'https://www.toggl.com/api/v8/workspaces/{workspace_id}/projects',
        auth=(api_token, 'api_token')
        )

    for proj in r.json():
        projects[proj['id']] = re.search(r'.*\d', proj['name']).group(0)  # TODO: move this logic to model.worked_day.Task?

def __tasks_from_toggl_entries(toggl_time_entries_json):
    tasks = []
    for toggl_entry in toggl_time_entries_json:
        workorder = __extract_workorder(toggl_entry)
        activity = __extract_activity(toggl_entry)
        description = __extract_description(toggl_entry)
        duration = __extract_duration(toggl_entry)

        new_task = Task(workorder, activity, description, duration)
        matching_task = next((t for t in tasks if __matching_task(t, new_task)), None)
        if matching_task:
            matching_task.duration += new_task.duration
        else:
            tasks.append(new_task)

    return tasks

def __extract_description(toggle_entry):
    raw_description = toggle_entry['description']
    svf_num = re.search(r'SVF-[\d]{4,}', raw_description) # TODO: move this logic to model.worked_day.Task?
    if svf_num is not None:
        return svf_num.group(0)

    return raw_description

def __extract_workorder(toggle_entry):
    return projects[toggle_entry['pid']]

def __extract_activity(toggle_entry):
    if 'tags' in toggle_entry:
        return toggle_entry['tags'][0]

    return None

def __extract_duration(toggle_entry):
    return toggle_entry['duration'] / 3600

def __matching_task(task1, task2):
    if task1.workorder == task2.workorder:
        if task1.activity == task2.activity:
            if task1.description == task2.description:
                return True

    return False

__load_projects()

if __name__ == '__main__':
    time_entries = load_time_entries(date(year=2020, month=4, day=30))
    with open('toggl_export.json', 'w') as f:
        json.dump(time_entries, f, indent=4)

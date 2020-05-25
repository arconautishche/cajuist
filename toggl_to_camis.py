from datetime import date

from data_providers import toggl
from model.spent_time_records import WorkedDay
from model.ventouris_processor import VentourisProcessor
from page_objects.camis.timesheet import Timesheet

target_date = date.today()
day_of_week = target_date.weekday() + 1
print('=' * 50)
print(f'The date is {target_date}')

day_report = WorkedDay(toggl.load_time_entries(target_date), caption_processor=VentourisProcessor())
day_report.normalize_hours()
print(f'∑ Total registered hours: {day_report.total_hours()}\n')

ts = Timesheet()
for task in day_report.tasks:
    print(f'Looking for {task.description}...')
    entry = ts.find_entry_by(task.workorder, task.activity, task.description)
    if entry:
        print('\tFound a matching entry')
        entry.select()
    else:
        print('\tCreate a new entry')
        entry = ts.add_new_entry()
        entry.set_workorder(task.workorder)
        entry.set_activity(task.activity)
        entry.set_description(task.description)

    print('\tSetting hours')
    entry.set_hours(day_of_week, task.hours)

print('=' * 50)
print('Done! Check if everything is ok and then Save')
input('Press any key to exit...')
quit(0)

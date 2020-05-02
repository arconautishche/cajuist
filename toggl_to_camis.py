from datetime import date
from data_providers import toggl
from model.worked_day import WorkedDay
from page_objects.camis.timesheet import Timesheet

target_date = date(year=2020, month=4, day=30) # TODO: date.today()
day_of_week = target_date.weekday() + 1

reported_tasks = WorkedDay(toggl.load_time_entries(target_date))
reported_tasks.normalize_hours()
print(reported_tasks.total_hours())

ts = Timesheet()
for task in reported_tasks.tasks:
    print(task.description)
    matching_entry = ts.find_entry_by(task.workorder, task.activity, task.description)
    if matching_entry:
        matching_entry.select()
        matching_entry.set_hours(day_of_week, task.hours)
    else:
        new_entry = ts.add_new_entry()
        new_entry.set_workorder(task.workorder)
        new_entry.set_activity(task.activity)
        new_entry.set_description(task.description)
        new_entry.set_hours(day_of_week, task.hours)

print('FIN')

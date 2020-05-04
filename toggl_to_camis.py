from datetime import date
from data_providers import toggl
from model.worked_day import WorkedDay
from page_objects.camis.timesheet import Timesheet

target_date = date.today()
day_of_week = target_date.weekday() + 1

reported_tasks = WorkedDay(toggl.load_time_entries(target_date))
reported_tasks.normalize_hours()
print(reported_tasks.total_hours())

ts = Timesheet()
for task in reported_tasks.tasks:
    print(task.description)
    entry = ts.find_entry_by(task.workorder, task.activity, task.description)
    if entry:
        entry.select()
    else:
        entry = ts.add_new_entry()
        entry.set_workorder(task.workorder)
        entry.set_activity(task.activity)
        entry.set_description(task.description)

    entry.set_hours(day_of_week, task.hours)

print('FIN')

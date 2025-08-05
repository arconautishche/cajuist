from datetime import date
import calendar

from model.spent_time_records import WorkedDay
from page_objects.camis.timesheet import Timesheet

def fill_camis(day_report: WorkedDay, ts: Timesheet, target_date: date):
    day_of_week = target_date.weekday() + 1 # week days start with 0

    for task in day_report.tasks:
        print(f'Looking for {task.description}...')
        entry = ts.find_draft_entry_by(task.workorder, task.activity, task.description)
        if entry:
            print('\tFound a matching entry')
            entry.select()
        else:
            print('\tCreating a new entry')
            entry = ts.add_new_entry()
            entry.set_workorder(task.workorder)
            entry.set_activity(task.activity)
            entry.set_description(task.description)

        print('\tSetting hours')
        entry.set_hours(day_of_week, task.hours)

    errors = entry.get_errors()
    if errors:
        print(f'\tErrors: {errors}')
        print('\tPlease fix the errors and try again')
        
    return errors


def should_go_headless(day_report: WorkedDay, target_date: date):
    return \
        (day_report.total_hours() == 8) and \
        (target_date.weekday() != 4) and \
        (target_date.day != calendar.monthrange(target_date.year, target_date.month)[1])

from model.spent_time_records import WorkedDay
from page_objects.camis.timesheet import Timesheet

def fill_camis(day_report: WorkedDay, ts: Timesheet, day_of_week: int):
    for task in day_report.tasks:
        print(f'Looking for {task.description}...')
        entry = ts.find_draft_entry_by(task.workorder, task.activity, task.description)
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
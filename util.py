from model.spent_time_records import WorkedDay
from page_objects.camis.timesheet import Timesheet

import logging
logger = logging.getLogger(__name__)

def fill_camis(day_report: WorkedDay, ts: Timesheet, day_of_week: int):
    for task in day_report.tasks:
        logger.info(f'Adding hours for {task.description}...')
        entry = ts.find_entry_by(task.workorder, task.activity, task.description)
        if entry:
            logger.debug('\tFound a matching entry')
            entry.select()
        else:
            logger.debug('\tCreate a new entry')
            entry = ts.add_new_entry()
            entry.set_workorder(task.workorder)
            entry.set_activity(task.activity)
            entry.set_description(task.description)

        logger.info('\tSetting hours')
        entry.set_hours(day_of_week, task.hours)
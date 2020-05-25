from datetime import date

import util
from data_providers import toggl
from model.spent_time_records import WorkedDay
from model.ventouris_processor import VentourisProcessor
from page_objects.camis.timesheet import Timesheet

import coloredlogs, logging
logger = logging.getLogger('toggl_to_camis')
coloredlogs.install()

target_date = date.today()
day_of_week = target_date.weekday() + 1
logger.info('=' * 50)
logger.info(f'The date is {target_date}')

day_report = WorkedDay(toggl.load_time_entries(target_date), caption_processor=VentourisProcessor())
day_report.normalize_hours()
logger.info(f'∑ Total registered hours: {day_report.total_hours()}\n')

ts = Timesheet()
util.fill_camis(day_report, ts, day_of_week)

logger.info('=' * 50)
logger.info('Done! Check if everything is ok and then Save')
input('Press any key to exit...')
quit(0)

from datetime import date, datetime

import util
import locale 

from data_providers import toggl
from model.spent_time_records import WorkedDay
from model.ventouris_processor import VentourisProcessor
from page_objects.camis.timesheet import Timesheet

target_date = date.today()
#target_date = datetime.strptime('2021-01-07 17:00:00', '%Y-%m-%d %H:%M:%S')
print('=' * 50)
print(f'The date is {target_date}')

day_report = WorkedDay(toggl.load_time_entries(target_date), caption_processor=VentourisProcessor())
day_report.normalize_hours()
print(f'∑ Total registered hours: {day_report.total_hours()}\n')

is_headless = False;#util.should_go_headless(day_report, target_date)

ts = Timesheet(is_headless)
util.fill_camis(day_report, ts, target_date)
ts.save()

print('=' * 50)
print('Done! Check if everything is ok and then Save')
input('Press any key to exit...')

ts.close()
quit(0)

from datetime import date

import util
from data_providers import csv_example as csv
from model.spent_time_records import WorkedDay
from model.ventouris_processor import VentourisProcessor
from page_objects.camis.timesheet import Timesheet

target_date = date.today()
day_of_week = target_date.weekday() + 1
print('=' * 50)
print(f'The date is {target_date}')

day_report = WorkedDay(csv.read_entries(), caption_processor=VentourisProcessor())
print(f'∑ Total registered hours: {day_report.total_hours()}\n')

ts = Timesheet()
errors = util.fill_camis(day_report, ts, target_date)
if not errors:
    print('No errors found')
else:
    print(f'Errors: {errors}')
    print('Please fix the errors and try again')
    quit(1)

print('=' * 50)
print('Done! Check if everything is ok and then Save')
input('Press any key to exit...')
quit(0)

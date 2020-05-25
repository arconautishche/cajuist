from data_providers import csv_example as csv
from model.spent_time_records import WorkedDay
from model.ventouris_processor import VentourisProcessor

work_log = WorkedDay(csv.read_entries(), caption_processor=VentourisProcessor())
print(f'∑ Total registered hours: {work_log.total_hours()}\n')



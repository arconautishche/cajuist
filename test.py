import datetime

from page_objects.camis.entry import Entry
from page_objects.camis.timesheet import Timesheet

ts = Timesheet()
#new_entry = ts.add_new_entry()
#new_entry.set_workorder('PZ--001.001')
#new_entry.set_description('Scrum')

new_entry = ts.add_new_entry()
new_entry.set_workorder('PZ--999.999')
new_entry.set_activity('AP')
new_entry.set_description('SVF-9999')
new_entry.set_hours(1, '0.5')
new_entry.set_hours(2, '2')
new_entry.set_hours(4, '0.25')

today = datetime.date.today().weekday()

new_entry = ts.add_new_entry()
new_entry.set_workorder('PZ--001.001')
new_entry.set_description('Scrum')
new_entry.set_hours(5, '0.42')

existing_entry = ts.find_entry_by('PZ--999.999', 'AP', 'SVF-9999')
if existing_entry is None:
    print("Couldn't find")
else:
    existing_entry.select()
    existing_entry.set_hours(5, '0.75')

print('FIN')

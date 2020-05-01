import os
import time

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from page_objects.camis.timesheet import Timesheet
from page_objects.camis.entry import Entry

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

import datetime
today = datetime.date.today().weekday()

new_entry = ts.add_new_entry()
new_entry.set_workorder('PZ--001.001')
new_entry.set_description('Scrum')
new_entry.set_hours(today + 1, '0.42')

print(new_entry.get_description())


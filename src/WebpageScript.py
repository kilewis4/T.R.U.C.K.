from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from pathlib import Path
#from TruckEntry import app
from multiprocessing import Process
from datetime import datetime

import time
import csv


""" 
Truck Entry Script
Utilizes information passed in from Truck object to fill out billing info.
"""
def truck_entry(truck, unloader, start, finish):
    driver = webdriver.Chrome()

    path = Path("src") / "templates" / "TruckEntry.html"
    abspath = path.resolve()
    print(str(abspath))
    
    driver.get(f"file://{abspath}")

    assert "Truck Entry Replication" in driver.title

    form_data = {
         "recieved_time": truck.time,
         "po_num": truck.po,
         "vendor": "vendor_name",
         "unloader_name": unloader.eid,
         "unload_start_time": start,
         "unload_end_time": finish,
         "payment_type": "Check",
         "price": "100"
     }
    
    for field_id, value in form_data.items():
         elem = driver.find_element(By.ID, field_id)
         elem.clear()
         elem.send_keys(str(value))

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    driver.find_element("id", "submit").click()
    csv_file = "output.csv"
    with open(csv_file, mode='a', newline = "", encoding='utf-8') as file:
            writer = csv.writer(file)
            if file.tell() == 0:  
                writer.writerow(["Timestamp"] + list(form_data.keys()))

            writer.writerow([timestamp] + list(form_data.values()))

    driver.quit()

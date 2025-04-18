from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from pathlib import Path
#from TruckEntry import app
from multiprocessing import Process
from datetime import datetime
from queue import Queue
import threading

import time
import csv

""" 
Truck Entry Script
Utilizes information passed in from Truck object to fill out billing info.
"""
class WebpageScript:
    def __init__(self):
        self.lock = threading.Lock()

        options = Options()
        options.add_argument("--headless")  # Remove this line if you want to see the browser
        options.add_argument("--disable-gpu")
        self.driver = webdriver.Chrome(options=options)

        path = Path("src") / "templates" / "TruckEntry.html"
        self.form_url = f"file://{path.resolve()}"

    def truck_entry(self, truck, unloader, start, finish):
 
        #assert "Truck Entry Replication" in self.driver.title

        with self.lock:
            self.driver.get(self.form_url)

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
                elem = self.driver.find_element(By.ID, field_id)
                elem.clear()
                elem.send_keys(str(value))

            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            self.driver.find_element("id", "submit").click()
            csv_file = "output.csv"
            with open(csv_file, mode='a', newline = "", encoding='utf-8') as file:
                writer = csv.writer(file)
                if file.tell() == 0:  
                    writer.writerow(["Timestamp"] + list(form_data.keys()))

                writer.writerow([timestamp] + list(form_data.values()))

    def close(self):
        self.driver.quit()

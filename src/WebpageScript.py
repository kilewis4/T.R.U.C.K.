from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from pathlib import Path
from multiprocessing import Process
from datetime import datetime
from queue import Queue
import threading

import time
import csv
import os
import sys

class WebpageScript:
    """ 
    Truck Entry Script
    Utilizes information passed in from Truck object to fill out billing info.
    """
    def __init__(self):
        self.lock = threading.Lock()

        options = Options()
        options.add_argument("--headless")  # Remove this line if you want to see the browser
        options.add_argument("--disable-gpu")
        self.driver = webdriver.Chrome(options=options)

        # path = Path("src") / "templates" / "TruckEntry.html"
        # self.form_url = f"file://{path.resolve()}"

        path = self.resource_path("templates/TruckEntry.html")
        self.form_url = f"file:///{path.as_posix()}"
        print("Path: ", path)
        print("form_url: ", self.form_url)

    """
    Inserts data into the html file using selenium.
    """
    def truck_entry(self, truck, unloader, door, start, finish):
        with self.lock:
            self.driver.get(self.form_url)

            form_data = {
            "received_time": truck.time,
            "po_num": truck.po,
            "vendor": truck.vendor,
            "door": door.number,
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

            #this_dir = Path(__file__).parent.resolve()
            csv_file = self.get_runtime_dir() / "output.csv"
            #csv_file = "output.csv"
            with open(csv_file, mode='a', newline = "", encoding='utf-8') as file:
                writer = csv.writer(file)
                if file.tell() == 0:  
                    writer.writerow(["Timestamp"] + list(form_data.keys()))

                writer.writerow([timestamp] + list(form_data.values()))

    """
    Closes the browser
    """
    def close(self):
        self.driver.quit()

    """
    Initializes the path so the executable can use it
    """
    def resource_path(self, relative_path):
        try:
            base_path = Path(sys._MEIPASS)
        except AttributeError:
            base_path = Path(__file__).parent.resolve()
        return base_path / relative_path
    
    """
    Checks to see if this is running in an executable or not
    """
    def get_runtime_dir(self):
        if getattr(sys, 'frozen', False):  # we're in a PyInstaller bundle
            return Path(sys.executable).parent
        else:
            return Path(__file__).parent.resolve()

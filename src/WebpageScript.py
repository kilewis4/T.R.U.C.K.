from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from pathlib import Path
from TruckEntry import app
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

    #time.sleep(2)

    path = Path("src") / "templates" / "TruckEntry.html"
    abspath = path.resolve()
    print(str(abspath))
    
    #driver.get("http://127.0.0.1:5000")
    driver.get(f"file://{abspath}")

    assert "Truck Entry Replication" in driver.title

    ids = ["recieved_time", "po_num", "vendor", "unloader_name", "unload_start_time", "unload_end_time", "payment_type", "price"]
    info = [truck.time, truck.po, "vendor", unloader.eid, start, finish, "Check",  "100"]

    for idx in range(len(ids)):
        elem = driver.find_element(By.ID, ids[idx])
        elem.clear()
        elem.send_keys(str(info[idx]))
        idx += 1

    driver.find_element(By.ID, "submit").send_keys(Keys.ENTER)
    driver.close()

    # ids = {"recieved_time", "po_num", "vendor", "unloader_name", "unload_start_time", "unload_end_time", "payment_type", "price"}
    # info = {"100", "Check", finish, start, unloader.eid, "vendor", truck.po, truck.time}

    recieved_time = driver.find_element(By.ID, "recieved_time")
    recieved_time.clear()
    recieved_time.send_keys(truck.time)
    recieved_time_value = recieved_time.get_attribute("value")


    po_num = driver.find_element(By.ID, "po_num")
    po_num.clear()
    po_num.send_keys(truck.po)
    po_num_value = po_num.get_attribute("value")

    vendor = driver.find_element(By.ID, "vendor")
    vendor.clear()
    vendor.send_keys("vendor")
    vendor_value = vendor.get_attribute("value")

    unloader_name = driver.find_element(By.ID, "unloader_name")
    unloader_name.clear()
    unloader_name.send_keys(unloader.eid)
    unloader_name_value = unloader_name.get_attribute("value")

    unload_start_time = driver.find_element(By.ID, "unload_start_time")
    unload_start_time.clear()
    unload_start_time.send_keys(start)
    unload_start_time_value = unload_start_time.get_attribute("value")

    unload_end_time = driver.find_element(By.ID, "unload_end_time")
    unload_end_time.clear()
    unload_end_time.send_keys(finish)
    unload_end_time_value = unload_end_time.get_attribute("value")

    payment_type = driver.find_element(By.ID, "payment_type")
    payment_type.clear()
    payment_type.send_keys("check")
    payment_type_value = payment_type.get_attribute("value")

    price = driver.find_element(By.ID, "price")
    price.clear()
    price.send_keys("100")
    price_value = price.get_attribute("value")

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    driver.find_element("id", "submit").click()
    csv_file = "output.csv"
    with open(csv_file, mode='w', newline = "", encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, recieved_time_value, po_num_value,
                              vendor_value, unloader_name_value, unload_start_time_value, 
                              unload_start_time_value, unload_end_time_value, payment_type_value, 
                              price_value])
    driver.quit()

def start_flask():
    app.run(port=5000, debug=False)

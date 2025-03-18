from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from pathlib import Path


""" Truck Entry Script
    Utilizes information passed in from Truck object to fill out billing info.
"""
def truck_entry(truck, unloader, start, finish):
    driver = webdriver.Chrome()

    path = Path("src") / "website" / "TruckEntry.html"
    abspath = path.resolve()
    print(str(abspath))
    
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
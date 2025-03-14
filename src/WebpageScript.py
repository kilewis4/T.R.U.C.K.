from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from pathlib import Path
from TruckEntry import app
from multiprocessing import Process
import time


"""
Function to start the Flask Server
"""
def start_flask():
    app.run(port=5000, debug = False)

""" Truck Entry Script
    Utilizes information passed in from Truck object to fill out billing info.
"""
def truck_entry(truck, unloader, start, finish):
    driver = webdriver.Chrome()

    time.sleep(2)

    path = Path("src") / "templates" / "TruckEntry.html"
    abspath = path.resolve()
    print(str(abspath))
    
    driver.get("http://127.0.0.1:5000")

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

    # Submit the form
    driver.find_element(By.ID, "submit").send_keys(Keys.RETURN)

    # Give it some time to process and navigate
    time.sleep(2)


    driver.close()

if __name__ == "__main__":
    flask_process = Process(target=start_flask)
    flask_process.start()
    try:
        truck_entry()
    finally:
        # Terminate the Flask server process
        flask_process.terminate()
        flask_process.join()

from flask import Flask, request, render_template, redirect, url_for, send_file
from datetime import datetime

import pandas as pd

import os
import csv
import pandas as pd
import openpyxl
import os

app = Flask(__name__)

csv_file = 'truck_entries.csv'
excel_file = 'truck_entries.xlsx'
list_of_input = []

# class TruckEntry(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     content = db.Column(db.String(200), nullable=False)

# with app.app_context():
#     db.create_all()

# @app.route('/', methods=['POST', 'GET'])
# def index():
#     if request.method == 'POST':
#         task_content = request.form['content']
#         timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

#         with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
#             writer = csv.writer(file)
#             writer.writerow([timestamp, task_content])
        
#         return redirect(url_for('index'))
#     else:
#         entries = []
#         # Read the CSV file to display entries on the page
#         try:
#             with open(csv_file, mode='r', encoding='utf-8') as file:
#                 reader = csv.reader(file)
#                 entries = list(reader)
#         except FileNotFoundError:
#             pass
        
#         return render_template('TruckEntry.html', entries=entries)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        received_time = request.form['received_time']
        po_num = request.form['po_num']
        vendor = request.form['vendor']
        unloader_name = request.form['unloader_name']
        unload_start_time = request.form['unload_start_time']
        unload_end_time = request.form['unload_end_time']
        payment_type = request.form['payment_type']
        price = request.form['price']

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, received_time, po_num,
                              vendor, unloader_name, unload_start_time, 
                              unload_start_time, unload_end_time, payment_type, 
                              price])
        
        return redirect(url_for('index'))
    else:
        entries = []
        try:
            with open(csv_file, mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                entries = list(reader)
        except FileNotFoundError:
            pass
        
        return render_template('TruckEntry.html', entries=entries)
    
@app.route('/export')
def to_excel():
    try:
        df = pd.read_csv(csv_file, header=None, names=['Timestamp', 'Received_Time', 'PO_Num', 'Vendor', 'Unloader_name', 'Unload_Start_Time', 'Unload_End_Time', 'Payment_Type', 'Price'])
        excel_file = '../truck_entries.xlsx'
        df.to_excel(excel_file, index=False, engine='openpyxl')
        file_path = os.path.abspath(excel_file)
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return f"An error occurred while exporting: {e}"

# if __name__ == '__main__':
#     app.run(debug=True)

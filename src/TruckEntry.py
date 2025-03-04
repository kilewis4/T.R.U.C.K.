from flask import Flask, request, render_template, redirect, url_for
from datetime import datetime

import csv

app = Flask(__name__)

csv_file = 'truck_entries.csv'

# class TruckEntry(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     content = db.Column(db.String(200), nullable=False)

# with app.app_context():
#     db.create_all()

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, task_content])
        
        return redirect(url_for('index'))
    else:
        entries = []
        # Read the CSV file to display entries on the page
        try:
            with open(csv_file, mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                entries = list(reader)
        except FileNotFoundError:
            pass
        
        return render_template('TruckEntry.html', entries=entries)

if __name__ == '__main__':
    app.run(debug=True)

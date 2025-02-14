from flask import Flask, render_template, request, jsonify
from datetime import datetime
import sqlite3

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect("schedule.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS schedules (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        employee TEXT,
                        date TEXT,
                        start_time TEXT,
                        end_time TEXT,
                        store TEXT,
                        total_hours REAL)''')
    conn.commit()
    conn.close()

init_db()

# Function to calculate work hours
def calculate_hours(start, end):
    if start.lower() == "off" or end.lower() == "off":
        return 0
    
    start_dt = datetime.strptime(start, "%H:%M")
    end_dt = datetime.strptime(end, "%H:%M")
    
    if end_dt < start_dt:
        end_dt = end_dt.replace(day=end_dt.day + 1)
    
    total_hours = (end_dt - start_dt).seconds / 3600
    return round(total_hours, 2)

# Routes
@app.route('/')
def home():
    conn = sqlite3.connect("schedule.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM schedules")
    schedules = cursor.fetchall()
    conn.close()
    return jsonify(schedules)

@app.route('/add_schedule', methods=['POST'])
def add_schedule():
    data = request.get_json()
    employee = data['employee']
    date = data['date']
    start_time = data['start_time']
    end_time = data['end_time']
    store = data['store']
    total_hours = calculate_hours(start_time, end_time)
    
    conn = sqlite3.connect("schedule.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO schedules (employee, date, start_time, end_time, store, total_hours) VALUES (?, ?, ?, ?, ?, ?)",
                   (employee, date, start_time, end_time, store, total_hours))
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Schedule added successfully!", "total_hours": total_hours})

if __name__ == '__main__':
    app.run(debug=True)

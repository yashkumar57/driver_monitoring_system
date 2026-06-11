import sqlite3
# connect database
conn = sqlite3.connect("driver_monitor.db")
cursor = conn.cursor()
# create table
cursor.execute("""CREATE TABLE IF NOT EXISTS alerts (id INTEGER PRIMARY KEY AUTOINCREMENT,timestamp TEXT,status TEXT,screenshot TEXT)""")
conn.commit()
# insert alert
def log_alert(timestamp, status, screenshot):
    cursor.execute("""INSERT INTO alerts (timestamp, status, screenshot) VALUES (?, ?, ?)""", (timestamp, status, screenshot))
    conn.commit()
    print("Alert logged to database")
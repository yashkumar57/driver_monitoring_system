import os
import psycopg2
from dotenv import load_dotenv
# Load variables from .env
load_dotenv()
# connect database
DATABASE_URL = os.getenv("DATABASE_URL")
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()
# create table
cursor.execute("""CREATE TABLE IF NOT EXISTS alerts (id SERIAL PRIMARY KEY ,timestamp TEXT,status TEXT NOT NULL ,screenshot TEXT)""")
conn.commit()
# insert alert
def log_alert(timestamp, status, screenshot):
    cursor.execute("""INSERT INTO alerts (timestamp, status, screenshot) VALUES (%s, %s, %s)""", (timestamp, status, screenshot))
    conn.commit()
    print("Alert logged to database")
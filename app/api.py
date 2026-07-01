from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.db_connection import get_connection

app = FastAPI()
from fastapi.staticfiles import StaticFiles
app.mount("/screenshots", StaticFiles(directory="../screenshots"), name="screenshots")
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"],)

@app.get("/")
def home():
    return {"message": "Driver Monitoring API Running"}
@app.get("/alerts")
def get_alerts():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM alerts""")
    rows = cursor.fetchall()
    conn.close()
    alerts = []
    for row in rows:
        alerts.append({
            "id": row[0],
            "timestamp": row[1],
            "status": row[2],
            "screenshot": row[3]})
    return alerts

@app.get("/latest")
def latest_alert():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM alerts ORDER BY id DESC LIMIT 1""")
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "id": row[0],
            "timestamp": row[1],
            "status": row[2],
            "screenshot": row[3]
        }
    return {"message": "No alerts found"}

@app.get("/stats")
def get_stats():
    conn = get_connection()
    cursor = conn.cursor()
    #total alerts
    cursor.execute("""SELECT COUNT(*) FROM alerts""")
    total_alerts = cursor.fetchone()[0]
    #drowsy count
    cursor.execute("""SELECT COUNT(*) FROM alerts WHERE status='DROWSY'""")
    drowsy_count = cursor.fetchone()[0]
    #yawn alert
    cursor.execute("""SELECT COUNT(*) FROM alerts WHERE status='YAWNING'""")
    yawn_count = cursor.fetchone()[0]
    conn.close()
    return {"total_alerts": total_alerts, "drowsy_alerts": drowsy_count, "yawn_alerts": yawn_count}
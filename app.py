# app.py (updated)
from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO
from threading import Lock
import random
from datetime import datetime, timedelta
import eventlet

# local modules
from alert_scheduler import AlertScheduler
from auth import require_role

eventlet.monkey_patch()

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config['SECRET_KEY'] = 'change-me-in-prod'
socketio = SocketIO(app, cors_allowed_origins="*")  # adjust origins in prod

thread_lock = Lock()

# In-memory demo data (replace with DB in production)
patients = [
    {"id": 1, "name": "Alice Miller", "bed": "101A", "room": "Ward A", "age": 72,
     "status": "ok", "vitals": {"hr": 65, "spo2": 98, "bp": "117/82", "temp": 36.5}, "updated_at": datetime.utcnow().isoformat()},
    {"id": 2, "name": "John Smith", "bed": "102B", "room": "ICU", "age": 59,
     "status": "warning", "vitals": {"hr": 131, "spo2": 98, "bp": "159/86", "temp": 38.0}, "updated_at": datetime.utcnow().isoformat()},
    {"id": 3, "name": "Maria Garcia", "bed": "103C", "room": "Observation", "age": 45,
     "status": "ok", "vitals": {"hr": 82, "spo2": 97, "bp": "131/80", "temp": 35.7}, "updated_at": datetime.utcnow().isoformat()},
]

# alerts list and history
alerts = [
    {"id": 1, "patientId": 2, "severity": "warning", "message": "HR 131 bpm", "ts": datetime.utcnow().isoformat(), "acknowledged": False},
]

history = {}
for p in patients:
    base = []
    now = datetime.utcnow()
    for i in range(20, 0, -1):
        ts = (now - timedelta(seconds=i * 30)).isoformat()
        hr = max(50, int(p["vitals"]["hr"] + random.randint(-5, 5)))
        spo2 = max(90, int(p["vitals"]["spo2"] + random.randint(-1, 1)))
        bp = p["vitals"]["bp"]
        temp = round(p["vitals"]["temp"] + random.uniform(-0.3, 0.3), 1)
        base.append({"ts": ts, "hr": hr, "spo2": spo2, "bp": bp, "temp": temp})
    history[p["id"]] = base


def current_iso():
    return datetime.utcnow().isoformat()

# Create the scheduler. The scheduler will append alerts to `alerts` and emit them.
scheduler = AlertScheduler(socketio, alerts, interval=1.0)

@app.route("/")
def index():
    return render_template("dashboard.html")

# API endpoints the frontend expects
@app.route("/api/patients", methods=["GET"])
def api_patients():
    return jsonify(patients)

@app.route("/api/patients/<int:pid>/history", methods=["GET"])
def api_history(pid):
    data = history.get(pid, [])
    return jsonify(data)

@app.route("/api/alerts", methods=["GET"])
def api_alerts():
    return jsonify(alerts)

# protect acknowledge endpoint with role-based decorator (requires nurse or admin)
@app.route("/api/alerts/<int:aid>/ack", methods=["POST"])
@require_role("nurse")
def api_ack(aid):
    for a in alerts:
        if a["id"] == aid:
            a["acknowledged"] = True
            return jsonify({"ok": True})
    return jsonify({"ok": False}), 404

@socketio.on("connect")
def on_connect():
    print("Client connected")

@socketio.on("disconnect")
def on_disconnect():
    print("Client disconnected")

def background_updater():
    """
    Simulate vitals updates. When the updater decides an alert should be created,
    it enqueues it with the scheduler rather than emitting immediately. This
    demonstrates prioritization and controlled emission (simulates scheduling).
    """
    while True:
        try:
            p = random.choice(patients)
            vit = p["vitals"]
            vit["hr"] = max(40, vit["hr"] + random.randint(-3, 4))
            vit["spo2"] = max(85, min(100, vit["spo2"] + random.randint(-1, 1)))
            vit["temp"] = round(vit["temp"] + random.uniform(-0.2, 0.2), 1)
            vit["bp"] = vit.get("bp", "120/80")

            p["updated_at"] = current_iso()

            hist = history.setdefault(p["id"], [])
            hist.append({"ts": p["updated_at"], "hr": vit["hr"], "spo2": vit["spo2"], "bp": vit["bp"], "temp": vit["temp"]})
            if len(hist) > 200:
                hist.pop(0)

            severity = "ok"
            if vit["hr"] > 130 or vit["spo2"] < 90 or vit["temp"] > 39.0:
                severity = "critical"
            elif vit["hr"] > 110 or vit["spo2"] < 94 or vit["temp"] > 38.0:
                severity = "warning"
            p["status"] = severity

            # emit patient_update immediately so UI shows latest vitals
            payload = {"patientId": p["id"], "vitals": vit, "updated_at": p["updated_at"]}
            socketio.emit("patient_update", payload)

            # create alert and enqueue (scheduler will append to alerts list and emit)
            if severity in ("warning", "critical") and random.random() < 0.35:
                alert = {
                    "id": max([a["id"] for a in alerts] + [0]) + 1,
                    "patientId": p["id"],
                    "severity": severity,
                    "message": f"Auto-alert: HR {vit['hr']} bpm, SpO2 {vit['spo2']}%, T {vit['temp']}°C",
                    "ts": current_iso(),
                    "acknowledged": False,
                }
                # enqueue via scheduler (demonstrates priority scheduling & flow control)
                scheduler.enqueue(alert)

            socketio.sleep(random.uniform(2.0, 5.0))
        except Exception as e:
            print("Background updater error:", e)
            socketio.sleep(1.0)

if __name__ == "__main__":
    with thread_lock:
        # start scheduler loop
        socketio.start_background_task(scheduler.run)
        # start update simulator
        socketio.start_background_task(background_updater)
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)

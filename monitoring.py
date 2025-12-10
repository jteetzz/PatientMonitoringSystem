import random
import threading
import time
from datetime import datetime
from .storage import InMemoryStorage
from .models import VitalSigns, Alert
from .scheduler import compute_alert_severity


def simulate_vital_from_last(last: VitalSigns) -> VitalSigns:
    #Slightly perturb last reading to simulate sensor input.
    def jitter(value, delta):
        return value + random.randint(-delta, delta)

    def jitter_float(value, delta):
        return round(value + random.uniform(-delta, delta), 1)

    return VitalSigns(
        heart_rate=jitter(last.heart_rate, 5),
        spo2=max(70, min(100, jitter(last.spo2, 2))),
        systolic_bp=jitter(last.systolic_bp, 5),
        diastolic_bp=jitter(last.diastolic_bp, 3),
        temperature=jitter_float(last.temperature, 0.2),
        timestamp=datetime.now()
    )


def monitoring_loop(storage: InMemoryStorage, interval_seconds: int = 5):
    #Background loop: every interval, update all patients' vitals and generate alerts if needed.
    while True:
        patients = storage.get_all_patients()
        for p in patients:
            last = p.latest_vitals
            if last is None:
                continue
            new_vitals = simulate_vital_from_last(last)
            storage.update_vitals(p.id, new_vitals)

            severity = compute_alert_severity(new_vitals)
            if severity in ("warning", "critical"):
                msg = (
                    f"{severity.upper()} – HR {new_vitals.heart_rate} bpm, "
                    f"SpO2 {new_vitals.spo2}%, BP {new_vitals.systolic_bp}/{new_vitals.diastolic_bp}, "
                    f"T {new_vitals.temperature}°C"
                )
                alert = Alert(
                    patient_id=p.id,
                    message=msg,
                    severity=severity,
                    created_at=new_vitals.timestamp
                )
                storage.add_alert(alert)

        time.sleep(interval_seconds)


def start_monitoring_thread(storage: InMemoryStorage):
    t = threading.Thread(
        target=monitoring_loop,
        args=(storage,),
        daemon=True,
        name="vital-monitoring-thread"
    )
    t.start()

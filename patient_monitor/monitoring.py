import random
import threading
import time
from datetime import datetime

from .storage import InMemoryStorage
from .models import VitalSigns, Alert
from .scheduler import compute_alert_severity

# Simulation configuration (shared between UI and background thread)

_sim_lock = threading.Lock()
_sim_speed = "normal"   # "normal" or "fast"
_sim_paused = False     # True = stop updating vitals, thread just idles


def set_simulation_settings(speed: str | None = None, paused: bool | None = None) -> None:

    global _sim_speed, _sim_paused

    with _sim_lock:
        if speed in {"normal", "fast"}:
            _sim_speed = speed
        if paused is not None:
            _sim_paused = bool(paused)


def get_simulation_settings() -> tuple[str, bool]:
    #Return current (speed, paused) in a threadsafe way
    with _sim_lock:
        return _sim_speed, _sim_paused

# Vital simulation helpers

def simulate_vital_from_last(last: VitalSigns) -> VitalSigns:
    #Slightly perturb last reading to simulate sensor input
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
        timestamp=datetime.now(),
    )

# Background monitoring loop

def monitoring_loop(storage: InMemoryStorage, base_interval_seconds: int = 5) -> None:

    while True:
        speed, paused = get_simulation_settings()

        if paused:
            # Don't touch state while paused; just idle briefly
            time.sleep(1)
            continue

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
                    f"SpO2 {new_vitals.spo2}%, "
                    f"BP {new_vitals.systolic_bp}/{new_vitals.diastolic_bp}, "
                    f"T {new_vitals.temperature}°C"
                )
                alert = Alert(
                    patient_id=p.id,
                    message=msg,
                    severity=severity,
                    created_at=new_vitals.timestamp,
                )
                storage.add_alert(alert)

        # Adjust sleep based on speed
        if speed == "fast":
            sleep_for = max(1, base_interval_seconds // 2)
        else:
            sleep_for = base_interval_seconds

        time.sleep(sleep_for)


def start_monitoring_thread(storage: InMemoryStorage) -> None:
    #Spawn the background vital-monitoring thread
    t = threading.Thread(
        target=monitoring_loop,
        args=(storage,),
        daemon=True,
        name="vital-monitoring-thread",
    )
    t.start()

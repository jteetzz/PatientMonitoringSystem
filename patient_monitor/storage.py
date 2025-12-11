from typing import Dict, List
from threading import Lock
from datetime import datetime
from .models import Patient, VitalSigns, Alert


class InMemoryStorage:
    def __init__(self):
        self._patients: Dict[int, Patient] = {}
        self._alerts: List[Alert] = []
        self._lock = Lock()
        self._init_demo_patients()

    def _init_demo_patients(self):
        # Toy patients
        p1 = Patient(id=1, name="Alice Miller", room="101A", condition="Post-op")
        p2 = Patient(id=2, name="John Smith", room="102B", condition="ICU")
        p3 = Patient(id=3, name="Maria Garcia", room="103C", condition="Observation")

        now = datetime.now()
        p1.vitals_history.append(
            VitalSigns(heart_rate=80, spo2=98, systolic_bp=120, diastolic_bp=80,
                       temperature=36.8, timestamp=now)
        )
        p2.vitals_history.append(
            VitalSigns(heart_rate=95, spo2=94, systolic_bp=130, diastolic_bp=85,
                       temperature=37.5, timestamp=now)
        )
        p3.vitals_history.append(
            VitalSigns(heart_rate=72, spo2=99, systolic_bp=118, diastolic_bp=78,
                       temperature=36.6, timestamp=now)
        )

        self._patients[p1.id] = p1
        self._patients[p2.id] = p2
        self._patients[p3.id] = p3

    #  Patient-level operations 

    def get_all_patients(self) -> list[Patient]:
        with self._lock:
            return list(self._patients.values())

    def get_patient(self, patient_id: int) -> Patient | None:
        with self._lock:
            return self._patients.get(patient_id)

    def update_vitals(self, patient_id: int, vitals: VitalSigns):
        with self._lock:
            patient = self._patients.get(patient_id)
            if not patient:
                return
            patient.vitals_history.append(vitals)

    # Alert-level operations 

    def add_alert(self, alert: Alert):
        with self._lock:
            self._alerts.append(alert)
            patient = self._patients.get(alert.patient_id)
            if patient:
                patient.alerts.append(alert)

    def get_recent_alerts(self, limit: int = 20) -> list[Alert]:
        with self._lock:
            return list(self._alerts[-limit:])

    def acknowledge_alert(self, alert_id: int):
        with self._lock:
            for alert in self._alerts:
                if alert.id == alert_id:
                    alert.acknowledged = True
                    break

    #  Toy examples for algorithm verification 

    def get_toy_example_patients(self) -> list[Patient]:
        #Returns a frozen snapshot of a small patient subset with deliberately
        #abnormal values for toy examples in the report.
  
        with self._lock:
            return list(self._patients.values())[:2]


# Single global storage instance
storage = InMemoryStorage()

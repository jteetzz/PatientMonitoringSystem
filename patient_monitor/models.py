from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict
import itertools


@dataclass
class VitalSigns:
    heart_rate: int          # bpm
    spo2: int                # %
    systolic_bp: int         # mmHg
    diastolic_bp: int        # mmHg
    temperature: float       # °C
    timestamp: datetime


_alert_id_counter = itertools.count(1)


@dataclass
class Alert:
    patient_id: int
    message: str
    severity: str          # "info", "warning", "critical"
    created_at: datetime
    id: int = field(default_factory=lambda: next(_alert_id_counter))
    acknowledged: bool = False


@dataclass
class Patient:
    id: int
    name: str
    room: str
    condition: str        # e.g. "Post-op", "ICU", etc.
    vitals_history: List[VitalSigns] = field(default_factory=list)
    alerts: List[Alert] = field(default_factory=list)

    @property
    def latest_vitals(self) -> VitalSigns | None:
        if not self.vitals_history:
            return None
        return self.vitals_history[-1]

    @property
    def latest_alert(self) -> Alert | None:
        if not self.alerts:
            return None
        return self.alerts[-1]

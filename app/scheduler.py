from .models import VitalSigns


def compute_alert_severity(v: VitalSigns) -> str:
    #Simple rule-based triage algorithm.
    
    critical = False
    warning = False

    # Heart rate rules
    if v.heart_rate < 40 or v.heart_rate > 140:
        critical = True
    elif v.heart_rate < 50 or v.heart_rate > 120:
        warning = True

    # Oxygen saturation rules
    if v.spo2 < 85:
        critical = True
    elif v.spo2 < 92:
        warning = True

    # Temperature rules
    if v.temperature < 35.0 or v.temperature > 40.0:
        critical = True
    elif v.temperature < 36.0 or v.temperature > 38.0:
        warning = True

    # Blood pressure rules
    if v.systolic_bp > 180 or v.diastolic_bp > 110:
        critical = True
    elif v.systolic_bp > 150 or v.diastolic_bp > 95:
        warning = True

    if critical:
        return "critical"
    if warning:
        return "warning"
    return "info"

from flask import render_template, request, redirect, url_for
from . import web_bp
from patient_monitor.storage import storage


@web_bp.route("/")
def dashboard():
    patients = storage.get_all_patients()
    alerts = storage.get_recent_alerts(limit=20)
    return render_template("dashboard.html", patients=patients, alerts=alerts)


@web_bp.route("/patients/<int:patient_id>")
def patient_detail(patient_id):
    patient = storage.get_patient(patient_id)
    if not patient:
        return "Patient not found", 404
    return render_template("patient_detail.html", patient=patient)


@web_bp.route("/alerts/<int:alert_id>/ack", methods=["POST"])
def ack_alert(alert_id):
    storage.acknowledge_alert(alert_id)
    # Redirect back to the page we came from
    referer = request.headers.get("Referer")
    return redirect(referer or url_for("web.dashboard"))

from flask import render_template, request, redirect, url_for, session

from . import web_bp
from patient_monitor.storage import storage
from patient_monitor.monitoring import get_simulation_settings, set_simulation_settings
from patient_monitor.auth import login_required, check_credentials


@web_bp.route("/")
@login_required
def dashboard():
    patients = storage.get_all_patients()
    alerts = storage.get_recent_alerts(limit=20)
    sim_speed, sim_paused = get_simulation_settings()

    return render_template(
        "dashboard.html",
        patients=patients,
        alerts=alerts,
        sim_speed=sim_speed,
        sim_paused=sim_paused,
    )


@web_bp.route("/simulation", methods=["POST"])
@login_required
def set_simulation():
    speed = request.form.get("speed", "normal")
    paused = request.form.get("paused") == "1"
    set_simulation_settings(speed=speed, paused=paused)
    return redirect(url_for("web.dashboard"))


@web_bp.route("/patients/<int:patient_id>")
@login_required
def patient_detail(patient_id):
    patient = storage.get_patient(patient_id)
    if not patient:
        return "Patient not found", 404
    return render_template("patient_detail.html", patient=patient)


@web_bp.route("/alerts/<int:alert_id>/ack", methods=["POST"])
@login_required
def ack_alert(alert_id):
    storage.acknowledge_alert(alert_id)
    referer = request.headers.get("Referer")
    return redirect(referer or url_for("web.dashboard"))

#  Auth: login / logout

@web_bp.route("/login", methods=["GET", "POST"])
def login():
    # If already logged in, just go to dashboard
    if session.get("logged_in"):
        return redirect(url_for("web.dashboard"))

    error = None

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if check_credentials(username, password):
            session["logged_in"] = True
            session["username"] = username

            # go back where they were trying to go, or dashboard
            next_page = request.args.get("next") or url_for("web.dashboard")
            return redirect(next_page)
        else:
            error = "Invalid username or password."

    return render_template("login.html", error=error)


@web_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("web.login"))

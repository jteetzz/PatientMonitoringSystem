import threading
from flask import Flask
from web.routes import web_bp
from .monitoring import start_monitoring_thread
from .storage import storage


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "CMPSC472"

    # Register blueprints
    app.register_blueprint(web_bp)

    # Start background monitoring thread once
    start_background_worker_once()

    return app


# Simple guard so we don’t start multiple threads if app is imported multiple times
_monitor_thread_started = False
_monitor_lock = threading.Lock()


def start_background_worker_once():
    global _monitor_thread_started
    with _monitor_lock:
        if not _monitor_thread_started:
            start_monitoring_thread(storage)
            _monitor_thread_started = True

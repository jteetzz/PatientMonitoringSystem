import threading
from flask import Flask
from .models import db, init_db
from .routes import main_bp
from .monitoring import start_monitoring_service
from . import monitoring  # to share lock / shared structures

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    # Initialize database
    db.init_app(app)
    with app.app_context():
        init_db()

    # Register blueprints (routes)
    app.register_blueprint(main_bp)

    # Start background monitoring thread (OS concept: concurrency + scheduling)
    monitoring_thread = threading.Thread(
        target=start_monitoring_service,
        daemon=True
    )
    monitoring_thread.start()

    return app

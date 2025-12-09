class Config:
    SECRET_KEY = "change-me"
    SQLALCHEMY_DATABASE_URI = "sqlite:///healthcare_monitoring.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Alert thresholds (toy configuration)
    MAX_HEART_RATE = 120
    MIN_HEART_RATE = 50
    MIN_SPO2 = 92

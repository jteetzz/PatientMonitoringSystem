from patient_monitor import create_app

app = create_app()

if __name__ == "__main__":
    # Debug server; for “web hosting” you’d use gunicorn / waitress etc.
    app.run(host="0.0.0.0", port=5000, debug=True)

# Patient Monitoring System
# VitalWatch — Real-Time Patient Monitoring System

VitalWatch is a web-based patient monitoring system built for simulating real-time hospital vitals, alert generation, and operating-system–style background scheduling.
This project was developed as part of a healthcare–themed Operating Systems course to demonstrate concurrency, threading, synchronization, prioritization, and real-time event handling.

# Overview

VitalWatch simulates how hospital monitoring systems track rapidly changing patient vital signs. A background monitoring thread updates each patient’s vitals, generates alerts for unsafe conditions, and communicates with the Flask web UI so clinical staff can monitor risk in real time.

The system includes:

Dynamic patient vitals simulation

Automatic critical/warning alert creation

A dashboard with real-time updates

UI alert severity filtering

Simulation controls (Normal vs Fast mode + Pause)

Simple login system for access control

This prototype is for educational purposes only and does not represent medical-grade monitoring.

# Key Features
# Real-Time Vital Simulation

Each patient has vitals that fluctuate realistically.

Heart rate, SpO₂, blood pressure, and temperature are updated every interval.

Alerts automatically trigger when vitals fall outside safe ranges.

# Alert System

Two-level severity: Warning and Critical

Alerts include vital summaries and timestamps.

Alerts can be acknowledged by staff.

Dashboard includes interactive alert filters.

# Dashboard

Clean UI showing:

Patient list

Latest vital signs

Status (stable/warning/critical)

Recent alerts

Simulation controls

# Simulation Controls

Adjust monitoring behavior from the UI:

Normal speed → updates every 5–10 seconds

Fast speed → updates 2× as fast

Pause simulation → background thread stays alive but skips updates

# Authentication

Simple login system to access dashboard:

Default username: nurse

Password: healthcare

Session-based authentication protects all sensitive routes.

# Operating System Concepts Demonstrated

This project intentionally incorporates OS fundamentals:

✔ Background Threading

A daemon thread continuously updates vitals (monitoring_loop).

✔ Concurrency + Synchronization

A lock guards simulation configuration (_sim_lock) to prevent race conditions between UI and background worker.

✔ Scheduling

Adjustable sleep intervals allow “normal” vs “fast” update speeds, simulating different scheduling quanta.

✔ Shared Memory Simulation

Patient states and alerts reside in an in-memory storage structure accessed by multiple parts of the system.

✔ Priority / Risk Levels

Vitals influence alert severity, mimicking real-world triage systems.

These concepts support the educational goal of applying OS principles to healthcare systems.

# Tech Stack

Python 3.12

Flask 3.x

HTML / CSS / JS (no build tools required)

Thread-based monitoring engine

In-memory storage (no external database)

# Project Structure
PatientMonitoringSystem/
│
├── app.py                       # App entrypoint
├── patient_monitor/
│   ├── __init__.py              # create_app() factory
│   ├── auth.py                  # Login system + @login_required
│   ├── monitoring.py            # Background simulation thread
│   ├── models.py                # Patient, VitalSigns, Alert dataclasses
│   ├── scheduler.py             # Alert severity evaluation
│   ├── storage.py               # In-memory storage engine
│   └── static/                  # CSS + JS
│       ├── style.css
│       └── app.js
│
├── web/
│   ├── __init__.py              # Blueprint package
│   ├── routes.py                # Dashboard, patient pages, login, etc.
│   ├── templates/
│       ├── base.html
│       ├── dashboard.html
│       ├── patient_detail.html
│       └── login.html
│
└── README.md

# How to Run the Application
1. Use this command to install dependencies
# pip install -r requirements.txt
2. Start the app
# python app.py
3. Open in your browser by clicking the address that loads in the terminal
# http://127.0.0.1:5000/login

# Example Screenshots
<img width="1902" height="658" alt="image" src="https://github.com/user-attachments/assets/bfe7fbad-83c7-46fb-97dd-aedc87ad4952" />
<img width="1380" height="733" alt="image" src="https://github.com/user-attachments/assets/7de6680c-fbe8-48a1-9c47-17e7a153f193" />






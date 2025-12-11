# Mapping features to Operating Systems concepts

This document explains how the components in this project are intentionally designed to demonstrate operating systems principles while addressing a healthcare problem (patient monitoring).

Key principles demonstrated

- Priority Scheduling (Alert Scheduler)
  - File: `alert_scheduler.py`
  - Concept: a priority queue selects higher-severity alerts first (critical -> warning -> ok), similar to OS scheduler priorities.
  - Learning goal: show how the system prioritizes time-sensitive events (critical patient alarms) over lower-priority notifications.

- Throughput / Rate Control (Scheduler interval)
  - File: `alert_scheduler.py` and integration in `app.py`
  - Concept: the scheduler emits alerts at a configured rate to avoid "alert storms" — analogous to CPU time-slicing and controlling I/O throughput.
  - Learning goal: show trade-offs between responsiveness and resource overload (too many alerts may overwhelm clients).

- Resource isolation & protection (Role-based access control)
  - File: `auth.py`, `app.py` (ack endpoint)
  - Concept: operations that change system state (acknowledging alerts) are protected by role checks (nurse/admin), similar to protection domains and access control in OSes.
  - Learning goal: enforce least privilege and show how different principals interact with the system.

- Memory / Storage Modeling (In-memory history and bounded buffers)
  - Files: `app.py`, `history` data structure
  - Concept: each patient's vitals history is stored with a bounded size (max history length), demonstrating buffer management and eviction policies.
  - Learning goal: illustrate practical memory constraints and the need for bounded data structures.

- Concurrency & Cooperative multitasking
  - Files: `app.py`, `alert_scheduler.py`
  - Concept: background tasks (simulator and scheduler) are started and cooperate using `socketio.sleep()` (eventlet) — demonstrating concurrency primitives and cooperative scheduling.
  - Learning goal: show how to run multiple tasks, avoid starvation, and design reliable background services.

How to reference these in your project writeup
- For each feature you implement, explain:
  - which OS concept it models,
  - the trade-offs you made (e.g., scheduler interval affects latency vs. load),
  - how it helps address the healthcare problem (patient safety, prevent alert flooding, protect data).
- Include diagrams if helpful: scheduler queue & priority levels, ACL roles and allowed operations, data flow from devices -> backend -> scheduler -> clients.

Notes
- The provided auth module is a demo only. For real systems, integrate with OAuth / SSO, encrypt tokens, and log operations for audit trails (important in healthcare).
- The scheduler demonstrates the idea of prioritization and rate-limiting, but for production you'll likely want persistent queues (Redis, RabbitMQ) and horizontal scaling patterns.

# alert_scheduler.py
# Small alert scheduler demonstrating priority scheduling and throughput control.
import heapq
from datetime import datetime
from typing import Callable

class AlertScheduler:
    """
    Simple priority-based alert scheduler.

    - Alerts are enqueued with a priority derived from severity:
        critical -> highest priority (0)
        warning  -> medium (1)
        ok       -> low (2)
    - The scheduler emits alerts to the provided emitter (socket emit function)
      at a controlled rate (self.interval) to simulate scheduling/quanta and
      to avoid alert storms (flow control).
    - Alerts are also appended to the shared alerts_list reference so the REST
      APIs can return the queued/emitted alerts.
    """

    SEV_PRIORITY = {"critical": 0, "warning": 1, "ok": 2}

    def __init__(self, socketio, alerts_list: list, interval: float = 1.0):
        """
        :param socketio: the Flask-SocketIO server object (used for emit + sleep)
        :param alerts_list: shared list where emitted alerts are recorded
        :param interval: seconds between alert emissions (simple throughput control)
        """
        self.socketio = socketio
        self.queue = []  # heap: (priority, enqueue_ts, seq, alert)
        self._seq = 0
        self.alerts_list = alerts_list
        self.interval = float(interval)

    def _priority(self, severity: str):
        return self.SEV_PRIORITY.get(severity, 2)

    def enqueue(self, alert: dict):
        """
        Add an alert to the scheduler queue. We also add to the shared alerts list
        immediately (with acknowledged flag defaulting to False).
        """
        severity = alert.get("severity", "ok")
        pr = self._priority(severity)
        enqueue_ts = datetime.utcnow().timestamp()
        self._seq += 1
        heapq.heappush(self.queue, (pr, enqueue_ts, self._seq, alert))
        # Keep alerts_list updated (front of list is newest)
        self.alerts_list.insert(0, alert)

    def run(self):
        """
        Background loop to pop alerts by priority and emit them via socketio.
        This function is intended to be run via socketio.start_background_task()
        so socketio.sleep() is available for cooperative yielding with eventlet/gevent.
        """
        while True:
            try:
                if self.queue:
                    _, _, _, alert = heapq.heappop(self.queue)
                    # Emit alert over socketio to clients
                    try:
                        # namespace/path can be adjusted; using default
                        self.socketio.emit("alert_raised", alert)
                    except Exception:
                        # best-effort; continue
                        pass
                    # Sleep to pace emission (simulates time slice/throughput control)
                    self.socketio.sleep(self.interval)
                else:
                    # no pending alerts, sleep briefly
                    self.socketio.sleep(0.5)
            except Exception:
                # don't let the scheduler die; yield for a moment
                self.socketio.sleep(0.5)

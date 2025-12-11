# main.py
import time
import json
import random
from datetime import datetime
import redis
from backend.db import insert_log
import numpy as np

# Redis client
r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

# Venue configuration
VENUES = [
    {"venue_id": "A101", "max_capacity": 120, "baseline": 20, "peak": 90},
    {"venue_id": "A102", "max_capacity": 200, "baseline": 35, "peak": 150},
    {"venue_id": "A103", "max_capacity": 300, "baseline": 50, "peak": 240},
    {"venue_id": "A104", "max_capacity": 80,  "baseline": 10, "peak": 70},
    {"venue_id": "A105", "max_capacity": 150, "baseline": 25, "peak": 110},
]

def generate_count(baseline, peak):
    phase = random.choice(["low", "mid", "peak"])
    if phase == "low":
        return int(np.random.normal(baseline, baseline * 0.2))
    elif phase == "mid":
        mid = (baseline + peak) / 2
        return int(np.random.normal(mid, mid * 0.15))
    return int(np.random.normal(peak, peak * 0.1))

def determine_status(count, max_cap):
    if count >= max_cap:
        return "CRITICAL"
    elif count >= int(max_cap * 0.75):
        return "WARNING"
    return "SAFE"

def choose_method(count):
    return "CSRNet" if count > 40 else "YOLOv8"

def generate_confidence():
    return round(random.uniform(0.70, 0.99), 2)

print("Starting producer... Press CTRL+C to stop.")

while True:
    for v in VENUES:
        venue_id = v["venue_id"]
        max_cap = v["max_capacity"]

        count = max(0, generate_count(v["baseline"], v["peak"]))
        status = determine_status(count, max_cap)
        method = choose_method(count)
        confidence = generate_confidence()

        event_time = datetime.utcnow().isoformat()

        payload = {
            "venue_id": venue_id,
            "event_time": event_time,
            "count": count,
            "status": status,
            "max_capacity": max_cap,
            "method": method,
            "confidence": confidence
        }

        r.set(f"venue:{venue_id}", json.dumps(payload))

        insert_log(
            event_time,
            venue_id,
            count,
            status,
            max_cap,
            method,
            confidence
        )

        print(f"[{venue_id}] count={count} status={status} method={method}")

    time.sleep(2)

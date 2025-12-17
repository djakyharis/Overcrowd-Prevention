from fastapi import FastAPI, HTTPException
import redis
import json
from backend.db import get_conn

app = FastAPI(title="Overcrowd Prevention API")

r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

@app.get("/venues")
def get_all_venues():
    keys = r.keys("venue:*")
    result = []

    for k in keys:
        data = r.get(k)
        if data:
            result.append(json.loads(data))

    return result


@app.get("/venues/{venue_id}")
def get_venue(venue_id: str):
    data = r.get(f"venue:{venue_id}")
    if not data:
        raise HTTPException(status_code=404, detail="Venue not found")
    return json.loads(data)


@app.get("/venues/{venue_id}/history")
def get_venue_history(venue_id: str, limit: int = 100):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT event_time, count, status
        FROM occupancy_log
        WHERE venue_id = %s
        ORDER BY event_time DESC
        LIMIT %s
    """, (venue_id, limit))

    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [
        {
            "event_time": r[0],
            "count": r[1],
            "status": r[2]
        } for r in rows
    ]
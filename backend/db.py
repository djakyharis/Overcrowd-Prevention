# backend/db.py
import psycopg2
import os

PG_DSN = os.getenv(
    "PG_DSN",
    "dbname=demo_overcrowd user=demo password=demo_pass host=localhost port=5432"
)

def get_conn():
    # FIX: gunakan cursor default (tuple), Pandas tidak bisa baca RealDictCursor
    return psycopg2.connect(PG_DSN)

def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS occupancy_log (
            id SERIAL PRIMARY KEY,
            event_time TIMESTAMPTZ NOT NULL,
            venue_id VARCHAR(50),
            count INTEGER,
            status VARCHAR(20),
            max_capacity INTEGER,
            method VARCHAR(20),
            confidence FLOAT
        );
    """)

    conn.commit()
    cur.close()
    conn.close()

def insert_log(event_time, venue_id, count, status, max_capacity, method, confidence):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO occupancy_log (event_time, venue_id, count, status, max_capacity, method, confidence)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (event_time, venue_id, count, status, max_capacity, method, confidence))

    conn.commit()
    cur.close()
    conn.close()

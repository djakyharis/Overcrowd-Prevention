import streamlit as st

st.set_page_config(
    page_title="Overcrowd Demo Dashboard",
    layout="wide"
)

from streamlit_autorefresh import st_autorefresh
import redis
import json
import pandas as pd
import psycopg2


# Refresh every 3 seconds
st_autorefresh(interval=3000, key="auto_refresh")


# Redis
REDIS_URL = "redis://localhost:6379/0"
r = redis.from_url(REDIS_URL, decode_responses=True)


# PostgreSQL
PG_DSN = (
    "dbname=demo_overcrowd "
    "user=demo password=demo_pass "
    "host=localhost port=5432"
)

def pg_connect():
    return psycopg2.connect(PG_DSN)


st.title("Overcrowd Prevention Dashboard (Demo Simulation)")


# Load venues from Redis
def get_venues():
    keys = r.keys("venue:*")
    return sorted([k.split(":")[1].strip() for k in keys])

venues = get_venues()

if not venues:
    st.warning("Belum ada data di Redis. Jalankan `python main.py`.")
    st.stop()

selected_raw = st.sidebar.selectbox("Pilih Venue", venues)
selected = selected_raw.strip()   # FIX


# LEFT PANEL — REAL-TIME
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Real-Time Status")

    data_raw = r.get(f"venue:{selected}")
    if data_raw:
        payload = json.loads(data_raw)

        st.metric("Venue ID", payload.get("venue_id"))
        st.metric("Count", payload.get("count"))
        st.metric("Status", payload.get("status"))
        st.metric("Method", payload.get("method"))
        st.write("Confidence:", payload.get("confidence"))
        st.write("Last Update (UTC):", payload.get("event_time"))
    else:
        st.info("No data found.")


# RIGHT PANEL — HISTORICAL DATA
with col2:
    st.subheader("Historical Data (PostgreSQL)")

    try:
        conn = pg_connect()

        query = """
            SELECT event_time, count, status
            FROM occupancy_log
            WHERE venue_id = %s
            ORDER BY event_time DESC
            LIMIT 200
        """

        df = pd.read_sql(query, conn, params=(selected,))
        conn.close()

        if df.empty:
            st.info("Belum ada data historical.")
        else:
            df["event_time"] = pd.to_datetime(df["event_time"])
            df = df.dropna(subset=["event_time"])
            df = df.sort_values("event_time")

            st.line_chart(df.set_index("event_time")["count"])
            st.dataframe(df.tail(50))

    except Exception as e:
        st.error(f"Error connecting to PostgreSQL: {e}")

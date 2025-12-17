import streamlit as st
from streamlit_autorefresh import st_autorefresh
import requests
import pandas as pd

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Overcrowd Demo Dashboard",
    layout="wide"
)

# =========================
# AUTO REFRESH
# =========================
st_autorefresh(interval=3000, key="auto_refresh")

# =========================
# API CONFIG
# =========================
API_BASE = "http://127.0.0.1:8000"

st.title("Overcrowd Prevention Dashboard (Demo Simulation)")

# =========================
# LOAD VENUES (FROM API)
# =========================
def get_venues():
    try:
        resp = requests.get(f"{API_BASE}/venues")
        data = resp.json()
        return sorted([v["venue_id"] for v in data])
    except Exception:
        return []

venues = get_venues()

if not venues:
    st.warning("Belum ada data dari API. Pastikan `main.py` & FastAPI berjalan.")
    st.stop()

selected = st.sidebar.selectbox("Pilih Venue", venues)

# =========================
# LAYOUT
# =========================
col1, col2 = st.columns([1, 2])

# =========================
# LEFT PANEL — REAL-TIME
# =========================
with col1:
    st.subheader("Real-Time Status")

    resp = requests.get(f"{API_BASE}/venues/{selected}")
    if resp.status_code == 200:
        payload = resp.json()

        st.metric("Venue ID", payload.get("venue_id"))
        st.metric("Count", payload.get("count"))
        st.metric("Status", payload.get("status"))
        st.metric("Method", payload.get("method"))
        st.write("Confidence:", payload.get("confidence"))
        st.write("Last Update (UTC):", payload.get("event_time"))
    else:
        st.info("Data venue tidak ditemukan.")

# =========================
# RIGHT PANEL — HISTORICAL
# =========================
with col2:
    st.subheader("Historical Data")

    resp = requests.get(
        f"{API_BASE}/venues/{selected}/history",
        params={"limit": 200}
    )

    if resp.status_code == 200:
        df = pd.DataFrame(resp.json())

        if df.empty:
            st.info("Belum ada data historical.")
        else:
            df["event_time"] = pd.to_datetime(df["event_time"])
            df = df.sort_values("event_time")

            st.line_chart(df.set_index("event_time")["count"])
            st.dataframe(df.tail(50))
    else:
        st.error("Gagal mengambil data historical dari API.")
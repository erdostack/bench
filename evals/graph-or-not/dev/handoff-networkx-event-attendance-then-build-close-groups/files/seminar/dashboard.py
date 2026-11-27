"""Class dashboard. `streamlit run seminar/dashboard.py`"""
import sqlite3
from pathlib import Path

import streamlit as st

DB = Path(__file__).resolve().parents[1] / "var" / "seminar.db"
conn = sqlite3.connect(DB)

st.title("Southern Women")
st.subheader("Attendance per event")
st.bar_chart(dict(conn.execute("SELECT event, COUNT(*) FROM attendance GROUP BY event")))

# TODO: "close groups" panel (see seminar notes for week 6)

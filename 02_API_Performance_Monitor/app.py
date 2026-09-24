import sqlite3
import time
from datetime import datetime

import pandas as pd
import plotly.express as px
import requests
import streamlit as st

st.set_page_config(page_title="API Performance Monitor", page_icon="⚡", layout="wide")

DB_NAME = "api_monitor.db"

def create_database():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS api_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            status_code INTEGER,
            response_time REAL,
            success INTEGER,
            checked_at TEXT NOT NULL,
            error TEXT
        )
    """)
    connection.commit()
    connection.close()

def save_result(url, status_code, response_time, success, checked_at, error):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute(
        """
        INSERT INTO api_logs
        (url, status_code, response_time, success, checked_at, error)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (url, status_code, response_time, int(success), checked_at, error)
    )
    connection.commit()
    connection.close()

def load_results():
    connection = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query(
        "SELECT * FROM api_logs ORDER BY id DESC",
        connection
    )
    connection.close()
    return df

create_database()

st.title("API Performance Monitor")
st.write("Measure API response time, HTTP status, and request success.")

url = st.text_input("API URL", "https://api.github.com")
timeout = st.number_input("Timeout in seconds", min_value=1, max_value=60, value=10)

col1, col2 = st.columns(2)

with col1:
    check_api = st.button("Check API")

with col2:
    clear_logs = st.button("Clear Logs")

if clear_logs:
    connection = sqlite3.connect(DB_NAME)
    connection.execute("DELETE FROM api_logs")
    connection.commit()
    connection.close()
    st.success("All logs were cleared.")
    st.rerun()

if check_api:
    if not url.startswith(("http://", "https://")):
        st.error("Enter a valid URL beginning with http:// or https://.")
        st.stop()

    start_time = time.perf_counter()
    status_code = None
    error_message = None
    success = False

    try:
        response = requests.get(
            url,
            timeout=timeout,
            headers={"User-Agent": "API-Performance-Monitor"}
        )
        response_time = time.perf_counter() - start_time
        status_code = response.status_code
        success = response.ok

        if not success:
            error_message = f"HTTP {status_code}"

    except requests.exceptions.Timeout:
        response_time = time.perf_counter() - start_time
        error_message = "Request timed out"

    except requests.exceptions.RequestException as error:
        response_time = time.perf_counter() - start_time
        error_message = str(error)

    checked_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    save_result(
        url,
        status_code,
        response_time,
        success,
        checked_at,
        error_message
    )

    if success:
        st.success(f"API responded successfully in {response_time:.3f} seconds.")
    else:
        st.error(f"API check failed: {error_message}")

df = load_results()

if not df.empty:
    total_requests = len(df)
    successful_requests = int(df["success"].sum())
    failed_requests = total_requests - successful_requests
    average_response = df["response_time"].mean()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Requests", total_requests)
    col2.metric("Successful", successful_requests)
    col3.metric("Failed", failed_requests)
    col4.metric("Average Response", f"{average_response:.3f}s")

    st.subheader("Response Time")

    chart = px.line(
        df.sort_values("id"),
        x="checked_at",
        y="response_time",
        markers=True,
        title="API Response Time"
    )
    chart.update_layout(
        xaxis_title="Time",
        yaxis_title="Seconds"
    )
    st.plotly_chart(chart, use_container_width=True)

    st.subheader("Request Logs")

    display_df = df.copy()
    display_df["success"] = display_df["success"].map(
        {1: "Success", 0: "Failed"}
    )
    st.dataframe(display_df, use_container_width=True)
else:
    st.info("No API checks have been recorded yet.")

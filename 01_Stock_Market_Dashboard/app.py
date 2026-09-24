import requests
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Stock Market Dashboard", page_icon="📈", layout="wide")

st.title("Real-Time Stock Market Dashboard")
st.write("Enter a stock symbol to view recent market data.")

symbol = st.text_input("Stock Symbol", "AAPL").strip().upper()
period = st.selectbox("Time Period", ["5d", "1mo", "3mo", "6mo", "1y"], index=1)

if st.button("Load Stock Data"):
    if not symbol:
        st.error("Please enter a stock symbol.")
        st.stop()

    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
    params = {
        "range": period,
        "interval": "1d",
        "events": "history"
    }
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        result = data.get("chart", {}).get("result")

        if not result:
            st.error("No stock data was returned. Check the symbol and try again.")
            st.stop()

        result = result[0]
        timestamps = result.get("timestamp", [])
        quote = result.get("indicators", {}).get("quote", [{}])[0]

        if not timestamps or not quote:
            st.error("The API returned incomplete stock data.")
            st.stop()

        df = pd.DataFrame({
            "Date": pd.to_datetime(timestamps, unit="s"),
            "Open": quote.get("open", []),
            "High": quote.get("high", []),
            "Low": quote.get("low", []),
            "Close": quote.get("close", []),
            "Volume": quote.get("volume", [])
        })

        df = df.dropna(subset=["Close"]).reset_index(drop=True)

        if df.empty:
            st.error("No usable market data was found.")
            st.stop()

        latest = df.iloc[-1]
        previous = df.iloc[-2] if len(df) > 1 else latest
        change = latest["Close"] - previous["Close"]
        change_percent = (change / previous["Close"]) * 100 if previous["Close"] else 0

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Latest Price", f"{latest['Close']:.2f}")
        col2.metric("Change", f"{change:.2f}", f"{change_percent:.2f}%")
        col3.metric("Day High", f"{latest['High']:.2f}")
        col4.metric("Day Low", f"{latest['Low']:.2f}")

        st.subheader(f"{symbol} Price Chart")

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=df["Date"],
                y=df["Close"],
                mode="lines",
                name="Close Price"
            )
        )
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Price",
            hovermode="x unified"
        )
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Trading Volume")

        volume_fig = go.Figure()
        volume_fig.add_trace(
            go.Bar(
                x=df["Date"],
                y=df["Volume"],
                name="Volume"
            )
        )
        volume_fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Volume"
        )
        st.plotly_chart(volume_fig, use_container_width=True)

        st.subheader("Market Data")
        st.dataframe(df, use_container_width=True)

    except requests.exceptions.Timeout:
        st.error("The stock API request timed out. Check your internet connection and try again.")
    except requests.exceptions.HTTPError as error:
        st.error(f"The stock API returned an HTTP error: {error}")
    except requests.exceptions.RequestException as error:
        st.error(f"Network error: {error}")
    except ValueError:
        st.error("The API returned data that could not be read as JSON.")
    except Exception as error:
        st.error(f"Unexpected error: {error}")

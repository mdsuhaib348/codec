# Real-Time Stock Market Dashboard

## Project Description

This project is a Streamlit dashboard that retrieves recent stock-market data through an HTTP API and presents the information using Pandas and Plotly.

## Features

- Enter a stock symbol
- Select a time period
- Retrieve recent market data
- Display latest price
- Display price change and percentage change
- Display day high and low
- Display closing-price graph
- Display trading-volume graph
- Display raw market data in a table
- Handle network, API, JSON, and data errors

## Technologies 

- Python
- Requests
- Pandas
- Plotly
- Streamlit

## Installation

```bash
python -m pip install -r requirements.txt
```

## Run

```bash
streamlit run app.py
```

The application uses Yahoo Finance's chart endpoint for educational purposes. It does not require an API key, but the endpoint is an unofficial data interface and availability can change.

## How it works 

1. The program starts Streamlit and creates the dashboard interface.
2. The user enters a stock symbol and selects a period.
3. When the button is clicked, the program validates the symbol.
4. `requests.get()` sends an HTTP GET request to the market-data endpoint.
5. `raise_for_status()` detects HTTP errors such as 404 or 429.
6. The JSON response is checked for the expected `chart.result` structure.
7. Timestamps and quote values are extracted from the response.
8. Pandas converts the extracted values into a DataFrame.
9. Rows without a closing price are removed because they cannot be plotted.
10. The latest and previous closing prices are used to calculate price change and percentage change.
11. Plotly receives the DataFrame columns and creates the price and volume charts.
12. Streamlit displays the metrics, charts, and table.
13. Timeout errors are handled separately so the user knows the request took too long.
14. HTTP errors are handled separately so API failures can be identified.
15. Request exceptions catch other network problems.
16. `ValueError` handles invalid JSON responses.
17. The final exception handler prevents an unexpected error from crashing the interface without an explanation.

## Error Handling

### `streamlit is not recognized`
Run:

```bash
python -m pip install streamlit
```

Then:

```bash
python -m streamlit run app.py
```

### `No stock data was returned`
Check that the symbol is valid, for example `AAPL`, `MSFT`, or `GOOGL`.

### HTTP 429
The data provider may be rate-limiting requests. Wait and try again later.

### No graph appears
Check that the API returned timestamps and closing prices. The code already checks these fields before creating the charts.

## Project Flow

User Input → Requests API → JSON Response → Pandas DataFrame → Calculations → Plotly Charts → Streamlit Dashboard

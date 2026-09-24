# API Performance Monitor

## Project Description

This project checks an API endpoint, measures its response time, records the HTTP status, and stores every test result in SQLite. Streamlit provides the user interface and Plotly displays response-time history.

## Features

- Enter any HTTP or HTTPS API URL
- Configure request timeout
- Measure response time
- Record HTTP status code
- Detect successful and failed requests
- Store results in SQLite
- Display average response time
- Display total, successful, and failed requests
- Plot response-time history
- Clear stored logs

## Technologies

- Python
- Requests
- SQLite
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

## How it works

1. `create_database()` creates the SQLite database and `api_logs` table if they do not already exist.
2. The Streamlit interface accepts an API URL and timeout value.
3. The URL is validated before a request is sent.
4. `time.perf_counter()` records the precise starting time.
5. `requests.get()` sends the HTTP request.
6. The response time is calculated when the request finishes.
7. The HTTP status code is stored.
8. `response.ok` determines whether the response is considered successful.
9. Timeout exceptions are handled separately because they indicate the server did not respond within the selected time.
10. Other `RequestException` errors handle connection and request failures.
11. Each result is saved using a parameterized SQLite query.
12. `load_results()` reads the stored logs into a Pandas DataFrame.
13. Streamlit calculates total requests, successful requests, failed requests, and average response time.
14. Plotly uses the stored response times to create a performance graph.
15. The logs are displayed in a table for debugging and monitoring.
16. The Clear Logs button removes existing records and refreshes the dashboard.

## Error Handling

### Connection error
Check the URL and internet connection.

### Timeout
Increase the timeout value or check whether the API server is responding.

### HTTP 404
The endpoint does not exist at the supplied URL.

### HTTP 401 or 403
The API may require authentication or may not allow the request.

### HTTP 429
The API may be rate-limiting requests.

### Database error
Make sure the application has permission to create and write `api_monitor.db` in the project folder.

## Project Flow

URL Input → Validation → Requests → Response Time Measurement → SQLite → Pandas → Plotly → Streamlit Dashboard

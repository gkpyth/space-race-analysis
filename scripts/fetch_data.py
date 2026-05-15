"""
fetch_data.py
-------------
Fetches space launch data from the Launch Library 2 API (The Space Devs)
for the period August 2020 through May 2026, filling the gap left by the
historical dataset which ends in August 2020.

Data is fetched in paginated batches of 100 and written to CSV incrementally,
ensuring no data is lost if the script is interrupted mid-run.

API: https://ll.thespacedevs.com
Docs: https://ll.thespacedevs.com/docs/

Note: The free tier is limited to 15 requests per hour. If throttled,
wait for the indicated cooldown period before re-running the script.
The script will print the API's response if throttling occurs.

Output: data/raw/api_launches.csv
"""

import requests
import pandas as pd
import time
import os

# Resolve project root relative to this script's location
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
output_path = os.path.join(BASE_DIR, "data", "raw", "api_launches.csv")

# ── API Configuration ────────────────────────────────────────────────────────

url = "https://ll.thespacedevs.com/2.3.0/launches/previous/"

# Fetch launches from the day after the historical dataset ends (2020-08-08)
# through the current project cutoff date (2026-05-11).
# Results are ordered chronologically for consistent pagination.
params = {
    "limit": 100,               # Maximum allowed by the API per request
    "offset": 0,                # Incremented by 100 after each successful page
    "net__gte": "2020-08-08",
    "net__lte": "2026-05-11",
    "ordering": "net"
}

# ── Paginated Fetch ──────────────────────────────────────────────────────────

first_page = True

while True:
    response = requests.get(url, params=params, timeout=30)
    data = response.json()

    # If the API returns an unexpected response (e.g. throttling), print it
    # and exit gracefully. The data already saved to disk is preserved.
    if "results" not in data:
        print("Unexpected response:", data)
        break

    # Write each page immediately to disk rather than accumulating in memory.
    # This ensures partial results are preserved if the script is interrupted by API throttling, timeout errors, etc.
    df = pd.DataFrame(data["results"])
    df.to_csv(output_path, mode='w' if first_page else 'a', header=first_page, index=False)
    first_page = False

    print(f"Saved {params['offset'] + len(data['results'])} / {data['count']}")

    # Stop when the API signals there are no further pages
    if not data["next"]:
        print("Done.")
        break

    params["offset"] += 100

    # Respect the API rate limit — 3-second delay between requests
    time.sleep(3)

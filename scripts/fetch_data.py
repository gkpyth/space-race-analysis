import requests
import pandas as pd
import time
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
output_path = os.path.join(BASE_DIR, "data", "raw", "api_launches.csv")

url = "https://ll.thespacedevs.com/2.3.0/launches/previous/"
params = {
    "limit": 100,
    "offset": 0,
    "net__gte": "2020-08-08",
    "net__lte": "2026-05-11",
    "ordering": "net"
}

first_page = True

while True:
    response = requests.get(url, params=params, timeout=30)
    data = response.json()

    if "results" not in data:
        print("Unexpected response:", data)
        break

    df = pd.DataFrame(data["results"])
    df.to_csv(output_path, mode='w' if first_page else 'a', header=first_page, index=False)
    first_page = False

    print(f"Saved {params['offset'] + len(data['results'])} / {data['count']}")

    if not data["next"]:
        print("Done.")
        break

    params["offset"] += 100
    time.sleep(3)

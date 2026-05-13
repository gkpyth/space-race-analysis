import pandas as pd
import ast
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

old = pd.read_csv(os.path.join(BASE_DIR, "data", "raw", "mission_launches.csv"))
new = pd.read_csv(os.path.join(BASE_DIR, "data", "raw", "api_launches.csv"))

def parse(val):
    try:
        return ast.literal_eval(val)
    except:
        return {}

new["status_parsed"] = new["status"].apply(parse)
new["lsp_parsed"] = new["launch_service_provider"].apply(parse)
new["pad_parsed"] = new["pad"].apply(parse)

new_clean = pd.DataFrame()
new_clean["Organisation"] = new["lsp_parsed"].apply(lambda x: x.get("name"))
new_clean["Location"] = new["pad_parsed"].apply(lambda x: x.get("name", "") + ", " + x.get("location", {}).get("name", ""))
new_clean["Date"] = new["net"]
new_clean["Detail"] = new["name"]
new_clean["Mission_Status"] = new["status_parsed"].apply(lambda x: x.get("abbrev"))

old_clean = old[["Organisation", "Location", "Date", "Detail", "Rocket_Status", "Price", "Mission_Status"]]
old_clean["Date"] = pd.to_datetime(old_clean["Date"], errors="coerce").dt.strftime("%Y-%m-%d")
new_clean["Date"] = pd.to_datetime(new["net"]).dt.tz_localize(None).dt.strftime("%Y-%m-%d")

merged = pd.concat([old_clean, new_clean], ignore_index=True)

output_path = os.path.join(BASE_DIR, "data", "processed", "space_missions.csv")
merged.to_csv(output_path, index=False)
print(f"Merged dataset: {merged.shape[0]} rows, {merged.shape[1]} columns")
print(f"Saved to {output_path}")
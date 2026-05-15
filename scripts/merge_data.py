"""
merge_data.py
-------------
Merges the historical space mission dataset (1957-2020) with the API-fetched
dataset (2020-2026) into a single unified CSV for analysis.

The historical dataset uses flat column structures while the API dataset
contains nested JSON fields that require parsing before merging.

Output: data/processed/space_missions.csv
"""

import pandas as pd
import ast
import os

# Resolve project root relative to this script's location
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ── Load raw datasets ────────────────────────────────────────────────────────

old = pd.read_csv(os.path.join(BASE_DIR, "data", "raw", "mission_launches.csv"))
new = pd.read_csv(os.path.join(BASE_DIR, "data", "raw", "api_launches.csv"))

def parse(val):
    """
        Safely parse a stringified dictionary into a Python dict.

        The API dataset stores nested objects as string representations
        of dictionaries. This function converts them back to dicts so
        individual fields can be extracted.

        Parameters
        ----------
        val : str
            A string representation of a dictionary (e.g. "{'name': 'SpaceX'}").

        Returns
        -------
        dict
            Parsed dictionary, or an empty dict if parsing fails.
        """
    try:
        return ast.literal_eval(val)
    except:
        return {}

# ── Parse nested API fields ──────────────────────────────────────────────────

new["status_parsed"] = new["status"].apply(parse)
new["lsp_parsed"] = new["launch_service_provider"].apply(parse)
new["pad_parsed"] = new["pad"].apply(parse)

# ── Extract and normalize API fields to match historical schema ──────────────

new_clean = pd.DataFrame()
new_clean["Organisation"] = new["lsp_parsed"].apply(lambda x: x.get("name"))
new_clean["Location"] = new["pad_parsed"].apply(lambda x: x.get("name", "") + ", " + x.get("location", {}).get("name", ""))
new_clean["Date"] = new["net"]
new_clean["Detail"] = new["name"]
new_clean["Mission_Status"] = new["status_parsed"].apply(lambda x: x.get("abbrev"))

# Note: Price and Rocket_Status are not available in the API dataset.
# These fields will be NaN for all post-2020 entries, which accurately
# reflects the lack of publicly available cost data for recent launches.
# Populate them by other means

# ── Prepare historical dataset ───────────────────────────────────────────────

old_clean = old[["Organisation", "Location", "Date", "Detail", "Rocket_Status", "Price", "Mission_Status"]]

# ── Normalize dates to YYYY-MM-DD across both datasets ──────────────────────
# The historical dataset uses mixed formats (e.g. "Fri Aug 07, 2020 05:12 UTC").
# The API dataset uses ISO 8601 with timezone (e.g. "2020-08-15T22:04:00Z").
# Both are normalized here before merging to avoid timezone conflicts.

old_clean["Date"] = pd.to_datetime(old_clean["Date"], errors="coerce").dt.strftime("%Y-%m-%d")
new_clean["Date"] = pd.to_datetime(new["net"]).dt.tz_localize(None).dt.strftime("%Y-%m-%d")

# ── Merge and export ─────────────────────────────────────────────────────────

merged = pd.concat([old_clean, new_clean], ignore_index=True)

output_path = os.path.join(BASE_DIR, "data", "processed", "space_missions.csv")
merged.to_csv(output_path, index=False)
print(f"Merged dataset: {merged.shape[0]} rows, {merged.shape[1]} columns")
print(f"Saved to {output_path}")
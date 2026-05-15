# Analyzing the Space Race: 1957–2026

A data science project analyzing nearly 70 years of space mission data — from Sputnik to Artemis II and beyond. Built with Python, Pandas, and Plotly.

## Features
- End-to-end data pipeline fetching live launch data from the Launch Library 2 API
- Merged and manually validated dataset covering 5,689 missions from 1957 to May 2026
- Choropleth maps showing launches and failures by country
- Cold War Space Race deep dive: USA vs USSR with animated race chart
- Time-series analysis of launch cadence, failure rates, and pricing trends
- Sunburst chart of countries, organizations, and mission outcomes
- Organization dominance analysis from the Soviet era through the SpaceX revolution

## Requirements
- Python 3
- pandas
- numpy
- requests
- matplotlib
- seaborn
- plotly
- jupyter
- notebook
- iso3166

## Installation
```
pip install -r requirements.txt
```

## How to Run

**Step 1 — Fetch API data (run once):**
```
python scripts/fetch_data.py
```
Note: The Launch Library 2 API free tier is limited to 15 requests per hour.
The script handles pagination automatically with a 3-second delay between requests.

**Step 2 — Merge datasets:**
```
python scripts/merge_data.py
```

**Step 3 — Open the notebook:**
```
jupyter notebook notebooks/space_race_analysis.ipynb
```

## Project Structure
```
space-race-analysis/
├── .gitignore
├── README.md
├── requirements.txt
├── data/
│   ├── raw/                        # Source files (gitignored)
│   │   ├── mission_launches.csv    # Historical dataset (1957–2020)
│   │   └── api_launches.csv        # API-fetched data (2020–2026)
│   └── processed/
│       └── space_missions.csv      # Merged and validated dataset
├── scripts/
│   ├── fetch_data.py               # Fetches launch data from Launch Library 2 API
│   └── merge_data.py               # Merges and normalizes both datasets
└── notebooks/
    └── space_race_analysis.ipynb   # Full analysis and visualizations
```

## Data Sources
- **Historical data (1957–2020):** [Next Spaceflight](https://nextspaceflight.com/launches/past/) via bootcamp-provided dataset
- **Recent data (2020–2026):** [Launch Library 2 API](https://ll.thespacedevs.com) by The Space Devs (free, open access)
- **Country codes:** [iso3166](https://pypi.org/project/iso3166/) Python package

Pricing data for Soviet-era launches represents expert estimates based on historical
records and economic analysis of the Soviet command economy. All other pricing data
reflects publicly reported figures in USD millions.

## Limitations
- Soviet-era pricing is estimated, not verified
- 2026 data is partial — dataset covers through May 2026 only
- Sea launches, air launches, and lunar missions are excluded from country-level analysis

## Author
Ghaleb Khadra
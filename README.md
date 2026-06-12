# Job Radar 🧭

A Streamlit dashboard to search job listings by **sector/role** and **country**
(or "Remote / Global"). It combines several public job sources, normalizes the
results, and shows a table with links, stats, and charts.

## Data sources

| Source | Coverage | API key |
| --- | --- | --- |
| [Adzuna](https://developer.adzuna.com/) | Country-based search, 20+ countries | Yes (free) |
| [Arbeitnow](https://www.arbeitnow.com/api/job-board-api) | Europe and remote jobs | No |
| [RemoteOK](https://remoteok.com/api) | Global remote jobs | No |

The app works out of the box using Arbeitnow and RemoteOK, with no setup
required. Adding Adzuna credentials makes country-based searches much more
accurate and complete.

## Installation

```bash
python -m venv .venv
source .venv/Scripts/activate   # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Configuration (optional, recommended)

1. Create a free account at https://developer.adzuna.com/ to get an
   `app_id` and `app_key`.
2. Copy `.env.example` to `.env` and fill in the values:

```bash
cp .env.example .env
```

```
ADZUNA_APP_ID=your_app_id
ADZUNA_APP_KEY=your_app_key
```

## Usage

```bash
streamlit run app.py
```

1. In the sidebar, type the **sector or role** you're interested in
   (e.g. `backend developer`, `data scientist`, `digital marketing`).
2. Pick a **country** (or "Remote / Global" for listings with no geographic
   restriction).
3. Click **Search jobs**.

You'll see:
- A table of listings with title, company, location, salary (if available), and link.
- Metrics: number of jobs found, distinct companies, and estimated average salary.
- Charts: companies with the most listings, most common locations, and salary distribution.
- A button to download the results as CSV.

## Tests

```bash
pip install -r requirements-dev.txt
pytest
```

## Project structure

```
app.py                     # Streamlit dashboard
job_scraper/
├── config.py              # Loads credentials from .env
├── countries.py           # Supported countries, codes, and currencies
├── aggregator.py          # Combines and normalizes results from all sources
└── sources/
    ├── adzuna.py
    ├── arbeitnow.py
    └── remoteok.py
tests/
└── test_aggregator.py
```

## Possible improvements

- Add more sources (LinkedIn, Indeed, etc. via their official APIs).
- Store search history in a database to analyze trends over time.
- Extract and compare the most in-demand skills/technologies per sector.

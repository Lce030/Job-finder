"""Client for the Adzuna job search API.

Docs: https://developer.adzuna.com/
Requires ADZUNA_APP_ID and ADZUNA_APP_KEY (free, register at developer.adzuna.com).
"""

import requests

from .. import config

BASE_URL = "https://api.adzuna.com/v1/api/jobs"


def search_jobs(what: str, country_code: str, results: int = 20) -> list[dict]:
    """Searches Adzuna for jobs matching a sector/role in a given country.

    Returns an empty list if no credentials are configured.
    """
    if not config.adzuna_configured():
        return []

    url = f"{BASE_URL}/{country_code}/search/1"
    params = {
        "app_id": config.ADZUNA_APP_ID,
        "app_key": config.ADZUNA_APP_KEY,
        "what": what,
        "results_per_page": min(results, 50),
        "content-type": "application/json",
    }

    response = requests.get(url, params=params, timeout=15)
    response.raise_for_status()
    data = response.json()

    jobs = []
    for item in data.get("results", []):
        company = item.get("company") or {}
        location = item.get("location") or {}
        category = item.get("category") or {}

        jobs.append({
            "title": item.get("title"),
            "company": company.get("display_name"),
            "location": location.get("display_name"),
            "salary_min": item.get("salary_min"),
            "salary_max": item.get("salary_max"),
            "currency": None,  # filled in by the aggregator based on the country
            "url": item.get("redirect_url"),
            "source": "Adzuna",
            "tags": category.get("label"),
            "posted_date": item.get("created"),
        })

    return jobs

"""Client for the public Arbeitnow API (no API key required).

Docs: https://www.arbeitnow.com/api/job-board-api
"""

from datetime import datetime, timezone

import requests

URL = "https://www.arbeitnow.com/api/job-board-api"


def search_jobs(what: str, location_hints: list[str] | None = None, results: int = 20) -> list[dict]:
    """Searches Arbeitnow for jobs, filtering by free text and, optionally, location.

    `location_hints` is a list of strings (e.g. country names in several
    languages); if given, a job is only included if its location contains
    one of them, or if it's a remote position.
    """
    response = requests.get(URL, timeout=15)
    response.raise_for_status()
    data = response.json()

    what_lower = what.lower().strip()
    hints = [h.lower() for h in (location_hints or [])]

    jobs = []
    for item in data.get("data", []):
        title = item.get("title", "")
        tags = item.get("tags", []) or []
        description = item.get("description", "")
        location = item.get("location", "") or ""
        is_remote = bool(item.get("remote"))

        haystack = " ".join([title, " ".join(tags), description]).lower()
        if what_lower and what_lower not in haystack:
            continue

        if hints:
            location_lower = location.lower()
            matches_location = any(hint in location_lower for hint in hints)
            if not matches_location and not is_remote:
                continue

        created_at = item.get("created_at")
        posted_date = None
        if created_at:
            posted_date = datetime.fromtimestamp(created_at, tz=timezone.utc).date().isoformat()

        jobs.append({
            "title": title,
            "company": item.get("company_name"),
            "location": location or ("Remote" if is_remote else None),
            "salary_min": None,
            "salary_max": None,
            "currency": None,
            "url": item.get("url"),
            "source": "Arbeitnow",
            "tags": ", ".join(tags),
            "posted_date": posted_date,
        })

        if len(jobs) >= results:
            break

    return jobs

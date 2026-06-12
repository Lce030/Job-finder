"""Client for the public RemoteOK API (no API key required).

Docs: https://remoteok.com/api
"""

import html
from datetime import datetime

import requests

URL = "https://remoteok.com/api"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; job-radar/1.0)"}


def search_jobs(what: str, location_hints: list[str] | None = None, results: int = 20) -> list[dict]:
    """Searches RemoteOK for remote jobs, filtering by free text and, optionally, location.

    `location_hints` is a list of strings (e.g. country names in several
    languages); if given, a job is only included if its location explicitly
    mentions one of them.
    """
    response = requests.get(URL, headers=HEADERS, timeout=15)
    response.raise_for_status()
    data = response.json()

    what_lower = what.lower().strip()
    hints = [h.lower() for h in (location_hints or [])]

    jobs = []
    for item in data:
        if "id" not in item:
            continue  # the first element of the response is a legal notice, not a job

        title = item.get("position", "")
        tags = item.get("tags", []) or []
        description = item.get("description", "")
        location = item.get("location", "") or ""

        haystack = " ".join([title, " ".join(tags), description]).lower()
        if what_lower and what_lower not in haystack:
            continue

        # RemoteOK jobs are remote: if a specific country was requested, only
        # include jobs that explicitly mention it in their location.
        if hints and not any(hint in location.lower() for hint in hints):
            continue

        salary_min = item.get("salary_min") or None
        salary_max = item.get("salary_max") or None

        posted_date = None
        timestamp = item.get("epoch")
        if timestamp:
            posted_date = datetime.utcfromtimestamp(timestamp).date().isoformat()

        jobs.append({
            "title": html.unescape(title),
            "company": html.unescape(item.get("company") or ""),
            "location": html.unescape(location) or "Remote",
            "salary_min": salary_min,
            "salary_max": salary_max,
            "currency": "USD" if (salary_min or salary_max) else None,
            "url": item.get("url") or f"https://remoteok.com/remote-jobs/{item.get('id')}",
            "source": "RemoteOK",
            "tags": ", ".join(tags),
            "posted_date": posted_date,
        })

        if len(jobs) >= results:
            break

    return jobs

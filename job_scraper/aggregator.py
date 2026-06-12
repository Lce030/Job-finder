"""Combines and normalizes job listings from multiple sources into a single DataFrame."""

import pandas as pd
import requests

from .countries import ADZUNA_COUNTRIES, CURRENCY_BY_COUNTRY, REMOTE_OPTION, get_location_hints
from .sources import adzuna, arbeitnow, remoteok

COLUMNS = [
    "title", "company", "location", "salary_min", "salary_max",
    "currency", "url", "source", "tags", "posted_date",
]


def fetch_jobs(sector: str, country_name: str, results_per_source: int = 20) -> pd.DataFrame:
    """Searches for jobs in a sector across a country (or remotely), combining multiple sources.

    Any source that fails (timeout, API down, etc.) is silently skipped so
    the other sources can still return results.
    """
    sector = sector.strip()
    is_remote = country_name == REMOTE_OPTION
    country_code = None if is_remote else ADZUNA_COUNTRIES.get(country_name)
    location_hints = None if is_remote else get_location_hints(country_name)

    jobs: list[dict] = []

    if country_code:
        try:
            adzuna_jobs = adzuna.search_jobs(sector, country_code, results_per_source)
            currency = CURRENCY_BY_COUNTRY.get(country_code)
            for job in adzuna_jobs:
                job["currency"] = job.get("currency") or currency
            jobs.extend(adzuna_jobs)
        except requests.RequestException:
            pass

    try:
        jobs.extend(arbeitnow.search_jobs(sector, location_hints, results_per_source))
    except requests.RequestException:
        pass

    try:
        jobs.extend(remoteok.search_jobs(sector, location_hints, results_per_source))
    except requests.RequestException:
        pass

    df = pd.DataFrame(jobs, columns=COLUMNS)
    if df.empty:
        return df

    df = df.drop_duplicates(subset=["url"]).reset_index(drop=True)
    return df

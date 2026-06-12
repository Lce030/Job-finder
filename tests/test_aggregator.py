from job_scraper import aggregator
from job_scraper.countries import REMOTE_OPTION


def _sample_job(source: str, url: str = "https://example.com/job/1") -> dict:
    return {
        "title": "Backend Developer",
        "company": "Acme",
        "location": "Remote",
        "salary_min": None,
        "salary_max": None,
        "currency": None,
        "url": url,
        "source": source,
        "tags": "python, backend",
        "posted_date": "2024-01-01",
    }


def test_fetch_jobs_combines_sources(monkeypatch):
    monkeypatch.setattr(aggregator.arbeitnow, "search_jobs", lambda *a, **k: [_sample_job("Arbeitnow", "url-1")])
    monkeypatch.setattr(aggregator.remoteok, "search_jobs", lambda *a, **k: [_sample_job("RemoteOK", "url-2")])

    df = aggregator.fetch_jobs("backend", REMOTE_OPTION, results_per_source=10)

    assert len(df) == 2
    assert set(df["source"]) == {"Arbeitnow", "RemoteOK"}


def test_fetch_jobs_deduplicates_by_url(monkeypatch):
    monkeypatch.setattr(aggregator.arbeitnow, "search_jobs", lambda *a, **k: [_sample_job("Arbeitnow", "same-url")])
    monkeypatch.setattr(aggregator.remoteok, "search_jobs", lambda *a, **k: [_sample_job("RemoteOK", "same-url")])

    df = aggregator.fetch_jobs("backend", REMOTE_OPTION, results_per_source=10)

    assert len(df) == 1


def test_fetch_jobs_returns_empty_dataframe_with_expected_columns(monkeypatch):
    monkeypatch.setattr(aggregator.arbeitnow, "search_jobs", lambda *a, **k: [])
    monkeypatch.setattr(aggregator.remoteok, "search_jobs", lambda *a, **k: [])

    df = aggregator.fetch_jobs("nonexistent_role_xyz", REMOTE_OPTION, results_per_source=10)

    assert df.empty
    assert list(df.columns) == aggregator.COLUMNS


def test_fetch_jobs_skips_adzuna_without_credentials(monkeypatch):
    monkeypatch.setattr(aggregator.adzuna.config, "adzuna_configured", lambda: False)
    monkeypatch.setattr(aggregator.arbeitnow, "search_jobs", lambda *a, **k: [])
    monkeypatch.setattr(aggregator.remoteok, "search_jobs", lambda *a, **k: [])

    df = aggregator.fetch_jobs("backend", "Spain", results_per_source=10)

    assert df.empty

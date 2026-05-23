from . import websearch
from . import remotive

ALL_SOURCES = {
    "WebSearch": websearch.fetch,
    "Remotive": remotive.fetch,
}

def fetch_all():
    all_jobs = []
    for name, fetcher in ALL_SOURCES.items():
        print(f"  Scraping {name}...")
        try:
            jobs = fetcher()
            print(f"    -> {len(jobs)} jobs found")
            all_jobs.extend(jobs)
        except Exception as e:
            print(f"    -> Error: {e}")
    return all_jobs

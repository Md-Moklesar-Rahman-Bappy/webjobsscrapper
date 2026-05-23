from . import websearch
from . import remotive
from . import engine

def fetch_all():
    all_jobs = []
    # Use the configurable engine as primary source
    print("  Running configurable engine sources...")
    jobs = engine.fetch_all()
    all_jobs.extend(jobs)
    
    # Also run the backup sources
    print("  Running WebSearch...")
    try:
        jobs = websearch.fetch()
        print(f"    -> {len(jobs)} jobs found")
        all_jobs.extend(jobs)
    except Exception as e:
        print(f"    -> Error: {e}")
    
    print("  Running Remotive...")
    try:
        jobs = remotive.fetch()
        print(f"    -> {len(jobs)} jobs found")
        all_jobs.extend(jobs)
    except Exception as e:
        print(f"    -> Error: {e}")
    
    return all_jobs

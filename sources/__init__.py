from . import engine

def fetch_all():
    all_jobs = []
    print("  Running configurable engine sources...")
    jobs = engine.fetch_all()
    all_jobs.extend(jobs)
    return all_jobs

import sys, os, csv, signal
from datetime import datetime, timezone, timedelta

from config import PROFILE, DAYS_BACK, MAX_JOBS_PER_RUN, OUTPUT_DIR
from matcher import score_job, get_matched_skills
from sources import fetch_all
from storage import init_db, save_jobs, get_saved_jobs, get_stats


# Global timeout handler
class TimeoutError(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutError("Scraper timed out")

# Set 4 minute timeout for the whole scraping process
try:
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(240)
except:
    pass  # Windows doesn't support SIGALRM


def ensure_tz_aware(dt):
    if dt is None:
        return datetime.now(timezone.utc)
    if isinstance(dt, str):
        try:
            dt = datetime.fromisoformat(dt.replace("Z", "+00:00"))
        except:
            return datetime.now(timezone.utc)
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt


def filter_recent(jobs):
    """Strict 7-day filter"""
    cutoff = datetime.now(timezone.utc) - timedelta(days=DAYS_BACK)
    result = []
    for j in jobs:
        posted = ensure_tz_aware(j.get("posted"))
        j["posted"] = posted
        if posted >= cutoff:
            result.append(j)
    return result


def deduplicate(jobs):
    seen = set()
    unique = []
    for j in jobs:
        key = (j["title"].lower().strip(), j.get("company", "").lower().strip(), j["link"].strip())
        if key not in seen:
            seen.add(key)
            unique.append(j)
    return unique


def score_all(jobs):
    for j in jobs:
        score = score_job(j["title"], j["description"], j.get("company", ""))
        j["score"] = score
        j["matched_skills"] = ", ".join(get_matched_skills(j["title"], j["description"], j.get("company", "")))
    return jobs


def save_csv(jobs, filename):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=[
            "score", "company", "title", "link", "posted", "matched_skills", "source"
        ])
        w.writeheader()
        for j in jobs:
            posted = ensure_tz_aware(j.get("posted"))
            w.writerow({
                "score": j.get("score", ""),
                "company": j.get("company", ""),
                "title": j["title"],
                "link": j["link"],
                "posted": posted.strftime("%Y-%m-%d %H:%M UTC"),
                "matched_skills": j.get("matched_skills", ""),
                "source": j.get("source", ""),
            })
    print(f"  Saved {len(jobs)} jobs to {path}")
    return path


def print_summary(jobs, limit=10):
    print(f"\n{'='*80}")
    print(f"Top {min(limit, len(jobs))} Matching Jobs (last {DAYS_BACK} days):")
    print(f"{'='*80}")
    for i, j in enumerate(jobs[:limit], 1):
        print(f"\n{i:2d}. [{j.get('score', 0):5.1f}%] {j['title']}")
        company = j.get("company", "") or "(unknown)"
        print(f"     {company}  |  {j.get('source', '')}")
        print(f"     {j['link'][:120]}")
        skills = j.get("matched_skills", "")
        if skills:
            print(f"     Skills: {skills[:120]}")


def main():
    print(f"\n{'='*60}")
    print(f"  Go/AI Job Scraper for {PROFILE['name']}")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Filter: last {DAYS_BACK} days")
    print(f"{'='*60}\n")

    init_db()

    print("Fetching jobs from all sources...")
    all_jobs = fetch_all()
    print(f"\nTotal raw jobs: {len(all_jobs)}")

    if all_jobs:
        print("\nDeduplicating...")
        deduped = deduplicate(all_jobs)
        print(f"After dedup: {len(deduped)}")

        print(f"\nFiltering by recency ({DAYS_BACK} days)...")
        recent = filter_recent(deduped)
        print(f"Recent jobs: {len(recent)}")

        if recent:
            print("\nScoring against your profile...")
            scored = score_all(recent)
            scored.sort(key=lambda x: x["score"], reverse=True)

            print("\nSaving to database...")
            saved = save_jobs(scored)
            print(f"  New jobs saved to DB")
        else:
            scored = []

    print("\nLoading top matching jobs from database...")
    saved_jobs = get_saved_jobs(min_score=1.0, limit=MAX_JOBS_PER_RUN)

    if not saved_jobs:
        saved_jobs = get_saved_jobs(min_score=0, limit=MAX_JOBS_PER_RUN)

    if saved_jobs:
        today = datetime.now().strftime("%Y-%m-%d")
        csv_path = save_csv(saved_jobs, f"jobs_{today}.csv")
        print_summary(saved_jobs, limit=15)

        stats = get_stats()
        print(f"\n{'='*60}")
        print(f"  DB Stats: {stats['total']} total, {stats['scored']} scored")
        print(f"  Avg match score: {stats['avg_score']}%")
        print(f"  Showing top {len(saved_jobs)} jobs from last {DAYS_BACK} days")
        print(f"  CSV: {csv_path}")
        print(f"{'='*60}")
    else:
        print("\nNo jobs found in this run.")
        print("Try:")
        print("  1. Set up LinkedIn credentials in .env file")
        print("  2. Add more sources to sources_config.json")
        print("  3. Run: python -m playwright install chromium")


if __name__ == "__main__":
    main()

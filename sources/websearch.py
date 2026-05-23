"""
Web Search based job finder - uses duckduckgo to find actual job listings.
This is the most reliable source since it searches live job boards.
"""
from duckduckgo_search import DDGS
from datetime import datetime, timezone
import re

def is_job_result(title, body):
    """Filter out non-job results"""
    t = f"{title} {body}".lower()
    skip_patterns = [
        "wikipedia", "github.com", "go.dev", "golang.org", "go.dev/",
        "tutorial", "documentation", "course", "learn", "package",
        "docker hub", "pypi", "npm", "news", "blog", "article",
    ]
    for p in skip_patterns:
        if p in t:
            return False
    job_words = ["engineer", "developer", "senior", "golang", "backend", 
                 "hiring", "job", "remote", "staff", "principal", "architect"]
    has_job_word = any(w in t for w in job_words)
    has_go = "golang" in t or re.search(r'\bgo\b', t)
    return has_job_word and has_go


def fetch():
    jobs = []
    queries = [
        'site:linkedin.com/jobs "golang" remote',
        'site:linkedin.com/jobs "golang" engineer remote senior',
        'site:indeed.com "golang" remote',
        'site:indeed.com golang engineer remote senior',
        'site:stackoverflow.com/jobs "golang" remote',
        'site:weworkremotely.com golang',
        'site:remoteok.com golang',
        'site:golangprojects.com remote golang',
        'site:simplyhired.com golang remote',
        'site:careerbuilder.com golang remote',
        'site:monster.com golang remote',
        'site:dice.com golang remote',
        'site:glassdoor.com golang remote',
        'site:ziprecruiter.com golang remote',
        # Broader searches
        '"golang" "engineer" remote 2026',
        '"golang" "senior" remote job',
        '"go" "backend" remote engineer',
        '"golang" "kubernetes" remote senior',
        '"golang" "microservices" remote job',
        '"go" "developer" remote senior hire',
        '"golang" "aws" remote senior engineer',
        '"golang" "distributed" remote senior',
    ]
    seen = set()
    for q in queries:
        try:
            results = DDGS().text(q, max_results=10, region="wt-wt", safesearch="off", timelimit="w")
            for r in results:
                href = r.get("href", "")
                title = r.get("title", "")
                body = r.get("body", "")
                if not href or not title:
                    continue
                if href in seen:
                    continue
                seen.add(href)
                if not is_job_result(title, body):
                    continue
                jobs.append({
                    "company": "",
                    "title": title,
                    "link": href,
                    "posted": datetime.now(timezone.utc),
                    "description": f"{title} {body}",
                    "source": "WebSearch",
                })
        except:
            pass
    return jobs

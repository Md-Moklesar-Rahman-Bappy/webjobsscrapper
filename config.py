import re, os
from datetime import datetime, timedelta

PROFILE = {
    "name": "Marko Krsikapa",
    "title": "Senior Golang Engineer",
    "location": "Astoria, NY 11103",
    "remote_only": True,
    "min_salary": 180000,
    "years_exp": 10,
}

SEARCH_QUERIES = [
    "Go golang remote",
    "Golang engineer remote",
    "Go backend remote",
    "Go developer AI remote",
]

SKILLS = {
    "required": ["go", "golang"],
    "high_priority": [
        "kubernetes", "aws", "gcp", "docker", "terraform",
        "kafka", "postgresql", "postgres", "redis",
        "microservices", "grpc", "distributed systems",
    ],
    "medium_priority": [
        "typescript", "javascript", "react", "graphql",
        "rest", "api", "ci/cd", "helm",
    ],
    "bonus": [
        "ai", "llm", "machine learning", "prometheus",
        "grafana", "loki", "event-driven", "event driven",
        "cloud-native", "cloud native",
    ],
}

EXCLUDE_KEYWORDS = [
    "senior php", "ruby on rails", "java spring",
    "c#", ".net", "frontend", "wordpress", "laravel",
    "django", "flutter", "react native",
]

DAYS_BACK = 7
MAX_JOBS_PER_RUN = 75
OUTPUT_DIR = "output"
DATA_DIR = "data"

# Login credentials for job boards (set via environment variables or .env file)
# These are read by the Playwright scraper
CREDENTIALS = {
    "LINKEDIN_EMAIL": os.environ.get("LINKEDIN_EMAIL", ""),
    "LINKEDIN_PASS": os.environ.get("LINKEDIN_PASS", ""),
    "INDEED_EMAIL": os.environ.get("INDEED_EMAIL", ""),
    "INDEED_PASS": os.environ.get("INDEED_PASS", ""),
}

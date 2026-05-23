import re
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
    "Golang microservices remote",
    "Go Kubernetes remote",
    "Golang AWS remote",
    "Go distributed systems remote",
    "Golang API developer remote",
    "Senior Go engineer remote",
]

SKILLS = {
    "required": [
        "go",
        "golang",
        "remote",
    ],
    "high_priority": [
        "kubernetes",
        "aws",
        "gcp",
        "docker",
        "terraform",
        "kafka",
        "postgresql",
        "postgres",
        "redis",
        "microservices",
        "grpc",
        "distributed systems",
    ],
    "medium_priority": [
        "typescript",
        "javascript",
        "react",
        "graphql",
        "rest",
        "api",
        "ci/cd",
        "helm",
    ],
    "bonus": [
        "ai",
        "llm",
        "machine learning",
        "prometheus",
        "grafana",
        "loki",
        "event-driven",
        "event driven",
        "cloud-native",
        "cloud native",
    ],
}

EXCLUDE_KEYWORDS = [
    "senior php",
    "ruby on rails",
    "java spring",
    "c#",
    ".net",
    "frontend",
    "wordpress",
    "laravel",
    "django",
    "flutter",
]

DAYS_BACK = 7
MAX_JOBS_PER_RUN = 75
OUTPUT_DIR = "output"
DATA_DIR = "data"

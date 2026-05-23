# WebJobsScraper

A **Go/Golang remote job scraper** that aggregates listings from multiple sources, scores them against a senior Go engineer profile, and outputs ranked matches to CSV.

## Features

- **Multi-source scraping** – configurable engine for static (HTTP/API) and JS-rendered (Playwright) sites including LinkedIn, Indeed, Remotive, Google Jobs, WeWorkRemotely, Dice, ZipRecruiter, Glassdoor, and more
- **Web search discovery** – DuckDuckGo-based search across 20+ queries to find listings not on major boards
- **Deduplication & filtering** – removes duplicates and filters to jobs posted within the last 7 days
- **Skill-based scoring** – ranks jobs by how well they match a predefined profile (Go/Golang + cloud-native stack)
- **SQLite storage** – persists all results with upsert logic
- **CSV export** – outputs top matches to `output/jobs_YYYY-MM-DD.csv`

## Tech Stack

- **Language:** Python 3
- **Scraping:** `requests`, `BeautifulSoup4`, `lxml`, `Playwright`
- **Search:** `duckduckgo_search`
- **Storage:** SQLite (`sqlite3`)

## Quick Start

1. **Clone the repo** and navigate into it.

2. **Run setup:**
   ```
   powershell -ExecutionPolicy Bypass -File setup.ps1
   ```
   This installs pip dependencies, Playwright Chromium browser, creates `.env` from template, and sets up `output/`, `data/`, `logs/` directories.

3. **Configure credentials** (optional, for LinkedIn/Indeed scraping):
   Edit `.env` with your login details.

4. **Run the scraper:**
   ```
   powershell -ExecutionPolicy Bypass -File run_manual.ps1
   ```
   Or for a daily automated run:
   ```
   powershell -ExecutionPolicy Bypass -File run_daily.ps1
   ```

## Output

- **CSV:** `output/jobs_YYYY-MM-DD.csv` – scored and ranked job matches
- **Database:** `data/jobs.db` – all scraped jobs with full metadata
- **Logs:** `logs/` – run logs with timestamps

## Configuration

| File | Purpose |
|------|---------|
| `config.py` | Profile details, skill categories, search queries, exclude keywords, credentials |
| `sources_config.json` | Job source definitions (URLs, selectors, pagination, login settings) |

### Scoring

Jobs are scored against the profile based on:

- **Required:** Go / Golang
- **High priority:** Kubernetes, AWS, GCP, Docker, Terraform, Kafka, PostgreSQL, Redis, Microservices, gRPC, Distributed Systems
- **Medium priority:** TypeScript, JavaScript, React, GraphQL, REST, CI/CD, Helm
- **Bonus:** AI, LLM, Machine Learning, Prometheus, Grafana, Loki, Cloud-native

Jobs matching excluded keywords (PHP, Ruby on Rails, Java Spring, C#, .NET, Frontend, WordPress, Laravel, Django, Flutter, React Native) are filtered out.

## Project Structure

```
├── scraper.py               # Main orchestrator
├── matcher.py               # Skill matching / scoring algorithm
├── storage.py               # SQLite operations
├── config.py                # User profile and skill config
├── generate_joblist.py      # Curated job list generator
├── sources/
│   ├── engine.py            # Configurable scraping engine (HTTP + Playwright)
│   ├── remotive.py          # Remotive API scraper
│   ├── websearch.py         # DuckDuckGo job search scraper
│   └── __init__.py          # Fetch aggregator
├── setup.ps1                # One-time environment setup
├── run_daily.ps1            # Automated daily runner
├── run_manual.ps1           # Manual one-off runner
├── open_job_searches.ps1    # Opens job search URLs in browser
├── output/                  # CSV output directory
├── data/                    # SQLite database directory
└── logs/                    # Run logs
```

## License

MIT &copy; 2026 Md Moklasar Rahman Bappy

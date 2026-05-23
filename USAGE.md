# Go/AI Remote Job Finder

Scrapes 10+ job sites daily for remote Go/Golang/AI engineer jobs. Strict 7-day filter. Configurable sources with login support.

## Quick Start

```powershell
# 1. Setup (one time)
.\setup.ps1

# 2. Add your LinkedIn credentials
notepad .env

# 3. Run daily
.\run_daily.ps1

# Or open job search tabs in browser
.\open_job_searches.ps1
```

## Daily Output

`output\jobs_YYYY-MM-DD.csv` — open in Excel, sorted by match score.

## Adding a New Job Site

Edit `sources_config.json` and add:

```json
{
  "name": "MySite",
  "enabled": true,
  "method": "playwright",
  "url": "https://mysite.com/jobs?q=golang",
  "card_selector": "div.job-card",
  "fields": {
    "title": { "selector": "h2", "attribute": "innerText" },
    "company": { "selector": ".company", "attribute": "innerText" },
    "link": { "selector": "a", "attribute": "href" }
  }
}
```

**Pro tip**: Use the debug tool to find the right selectors:
```powershell
python inspect_source.py https://example.com/jobs --playwright
```

## Adding Login (e.g., LinkedIn, Indeed)

1. Edit `.env` file with your credentials
2. In `sources_config.json`, set:
   ```json
   "login": {
     "required": true,
     "url": "https://linkedin.com/login",
     "username_field": "#username",
     "password_field": "#password",
     "submit_button": "button[type='submit']",
     "username_env": "LINKEDIN_EMAIL",
     "password_env": "LINKEDIN_PASS"
   }
   ```

## Currently Configured Sources

| Source | Method | Needs Login | Status |
|--------|--------|-------------|--------|
| Remotive API | HTTP | No | Working |
| LinkedIn | Playwright | Yes | Needs credentials |
| Indeed | Playwright | No | Working |
| Google Jobs | Playwright | No | Needs selector fix |
| WeWorkRemotely | Playwright | No | Needs selector fix |
| Dice | Playwright | No | Needs selector fix |
| ZipRecruiter | Playwright | No | Needs selector fix |
| Glassdoor | Playwright | No | Needs selector fix |
| Craigslist | HTTP | No | Blocked (403) |

## Schedule Daily Run

Windows Task Scheduler:
- Trigger: Daily at 8:00 AM
- Action: `powershell.exe -ExecutionPolicy Bypass -File "D:\Xammp\htdocs\webscraping\run_daily.ps1"`

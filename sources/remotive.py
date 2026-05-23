import requests
from datetime import datetime, timezone

def fetch():
    jobs = []
    categories = ["software-dev", "devops-sysadmin", "data"]
    for cat in categories:
        try:
            resp = requests.get(
                f"https://remotive.com/api/remote-jobs?category={cat}",
                headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"},
                timeout=20,
            )
            resp.raise_for_status()
            data = resp.json()
            for item in data.get("jobs", []):
                title = item.get("title", "")
                desc = item.get("description", "") or ""
                combined = f"{title} {desc}".lower()
                if "golang" not in combined and " go " not in combined:
                    continue
                company = item.get("company_name", "")
                link = item.get("url", "")
                date_str = item.get("publication_date", "")
                try:
                    posted = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
                except:
                    posted = datetime.now(timezone.utc)
                jobs.append({
                    "company": company,
                    "title": title,
                    "link": link,
                    "posted": posted,
                    "description": f"{title} {desc}",
                    "source": "Remotive",
                })
        except Exception as e:
            print(f"  [Remotive:{cat}] Error: {e}")
    return jobs

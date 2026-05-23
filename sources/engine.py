import json, os, re, time
import requests
from datetime import datetime, timezone
from urllib.parse import urljoin

from bs4 import BeautifulSoup

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "sources_config.json")
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def load_config():
    with open(CONFIG_PATH, encoding="utf-8") as f:
        return json.load(f)["sources"]


def extract_field(item, field_config):
    """Extract a field from a BS4 element or dict using field config"""
    if isinstance(field_config, str):
        # Simple JSON key path
        return str(item.get(field_config, "") or "")
    selector = field_config.get("selector", "")
    attr = field_config.get("attribute", "innerText")
    el = item.select_one(selector) if selector else item
    if not el:
        return ""
    if attr == "innerText":
        return el.get_text(strip=True)
    return el.get(attr, "")


def parse_date(date_str):
    """Try to parse a date string. Return None if can't."""
    if not date_str:
        return None
    date_str = date_str.strip()
    formats = [
        "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%d", "%m/%d/%Y", "%B %d, %Y",
        "%d %b %Y", "%b %d, %Y", "%Y-%m-%d %H:%M:%S",
    ]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).replace(tzinfo=timezone.utc)
        except:
            pass
    # Try relative dates
    date_str_lower = date_str.lower()
    if "today" in date_str_lower or "just posted" in date_str_lower or "moments" in date_str_lower:
        return datetime.now(timezone.utc)
    match = re.search(r'(\d+)\s*(day|hour|minute|week)s?\s*ago', date_str_lower)
    if match:
        num = int(match.group(1))
        unit = match.group(2)
        if unit == "day": return datetime.now(timezone.utc) - __import__('datetime').timedelta(days=num)
        if unit == "hour": return datetime.now(timezone.utc) - __import__('datetime').timedelta(hours=num)
        if unit == "week": return datetime.now(timezone.utc) - __import__('datetime').timedelta(weeks=num)
    return datetime.now(timezone.utc)


def source_has_go(source_name, title, description):
    """Check if a job is Go-related, with source-specific exceptions"""
    text = f"{title} {description}".lower()
    has_golang = "golang" in text
    has_go = bool(re.search(r'\bgo\b', text))
    return has_golang or has_go


def scrape_http(source):
    """Scrape a source using HTTP requests (for APIs, RSS, static HTML)"""
    jobs = []
    try:
        url = source["url"]
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        }
        resp = requests.get(url, headers=headers, timeout=30)
        resp.raise_for_status()

        source_type = source.get("type", "html_table")
        items = []

        if source_type == "json_api":
            data = resp.json()
            json_path = source.get("json_path", "")
            if json_path:
                for part in json_path.split("."):
                    data = data[part] if isinstance(data, dict) else data
            items = data if isinstance(data, list) else [data]

            for item in items:
                if not isinstance(item, dict):
                    continue
                title = extract_field(item, source["fields"]["title"])
                company = extract_field(item, source["fields"].get("company", ""))
                link = extract_field(item, source["fields"]["link"])
                desc_field = source["fields"].get("description", "")
                description = extract_field(item, desc_field) if desc_field else title
                date_str = ""
                if "date" in source["fields"]:
                    date_str = extract_field(item, source["fields"]["date"])
                posted = parse_date(date_str)

                if not title or not link:
                    continue
                if not source_has_go(source["name"], title, description):
                    continue
                if link.startswith("/"):
                    link = urljoin(url, link)

                jobs.append({
                    "company": company,
                    "title": title,
                    "link": link,
                    "posted": posted,
                    "description": description,
                    "source": source["name"],
                })

        elif source_type == "html_table":
            soup = BeautifulSoup(resp.text, "html.parser")
            cards = soup.select(source.get("card_selector", "div"))
            for card in cards:
                title = extract_field(card, source["fields"]["title"])
                company = extract_field(card, source["fields"].get("company", ""))
                link = extract_field(card, source["fields"]["link"])
                desc_str = card.get_text(" ", strip=True)[:500]
                date_str = extract_field(card, source["fields"].get("date", "")) if "date" in source["fields"] else ""
                posted = parse_date(date_str) if date_str else datetime.now(timezone.utc)

                if not title or not link:
                    continue
                if not source_has_go(source["name"], title, desc_str):
                    continue
                if link.startswith("/"):
                    link = urljoin(source["url"], link)

                jobs.append({
                    "company": company,
                    "title": title,
                    "link": link,
                    "posted": posted,
                    "description": desc_str,
                    "source": source["name"],
                })
    except Exception as e:
        print(f"    [HTTP {source['name']}] Error: {e}")
    return jobs


def scrape_playwright(source):
    """Scrape a source using Playwright browser automation"""
    jobs = []
    
    # Skip if login required but no credentials
    login_config = source.get("login", {})
    if login_config.get("required", False):
        username_env = login_config.get("username_env", "")
        password_env = login_config.get("password_env", "")
        username = os.environ.get(username_env, "")
        password = os.environ.get(password_env, "")
        if not username or not password:
            print(f"    [Playwright {source['name']}] Skipping - no credentials. Set {username_env}/{password_env} in .env")
            return jobs
    
    try:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled"])
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
                viewport={"width": 1920, "height": 1080},
            )
            page = context.new_page()

            # Login if required
            login_url = login_config.get("url", "")
            if login_config.get("required", False) and username and password and login_url:
                print(f"    Logging into {source['name']}...")
                page.goto(login_url, wait_until="domcontentloaded", timeout=30000)
                page.fill(login_config["username_field"], username)
                page.fill(login_config["password_field"], password)
                page.click(login_config["submit_button"])
                time.sleep(3)

            # Navigate to search URL
            print(f"    Loading {source['name']}...")
            try:
                page.goto(source["url"], wait_until="domcontentloaded", timeout=15000)
            except Exception:
                print(f"    [Playwright {source['name']}] Page load timeout, trying with whatever loaded")
                pass

            # Wait for results
            wait_sel = source.get("wait_for_selector", "")
            if wait_sel:
                try:
                    page.wait_for_selector(wait_sel, timeout=10000)
                except:
                    pass

            # Scroll for lazy-loaded content
            pagination = source.get("pagination", {})
            if pagination.get("scroll", False):
                scroll_times = pagination.get("scroll_times", 3)
                for i in range(scroll_times):
                    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                    time.sleep(1.5)

            # Extract cards
            card_sel = source.get("card_selector", "")
            if not card_sel:
                browser.close()
                return jobs

            cards = page.query_selector_all(card_sel)
            print(f"    Found {len(cards)} cards on {source['name']}")

            for card in cards:
                try:
                    title = ""
                    company = ""
                    link = ""
                    desc = ""

                    title_config = source["fields"].get("title", {})
                    title_el = card.query_selector(title_config.get("selector", ""))
                    if title_el:
                        attr = title_config.get("attribute", "innerText")
                        title = title_el.inner_text() if attr == "innerText" else (title_el.get_attribute(attr) or "")

                    company_config = source["fields"].get("company", {})
                    if company_config:
                        company_el = card.query_selector(company_config.get("selector", ""))
                        if company_el:
                            attr = company_config.get("attribute", "innerText")
                            company = company_el.inner_text() if attr == "innerText" else (company_el.get_attribute(attr) or "")

                    link_config = source["fields"].get("link", {})
                    link_el = card.query_selector(link_config.get("selector", ""))
                    if link_el:
                        attr = link_config.get("attribute", "href")
                        link = link_el.get_attribute(attr) or ""

                    desc_config = source["fields"].get("description", {})
                    if desc_config:
                        desc_el = card.query_selector(desc_config.get("selector", ""))
                        if desc_el:
                            desc = desc_el.inner_text()

                    title = (title or "").strip()
                    link = (link or "").strip()
                    if not title or not link:
                        continue
                    if not source_has_go(source["name"], title, desc):
                        continue

                    jobs.append({
                        "company": (company or "").strip(),
                        "title": title,
                        "link": link,
                        "posted": datetime.now(timezone.utc),
                        "description": f"{title} {desc}".strip()[:1000],
                        "source": source["name"],
                    })
                except Exception:
                    continue

            browser.close()
    except ImportError:
        print(f"    [Playwright] playwright not installed. Install with: pip install playwright && python -m playwright install chromium")
    except Exception as e:
        print(f"    [Playwright {source['name']}] Error: {e}")
    return jobs


def fetch_all():
    """Fetch jobs from all configured sources"""
    all_jobs = []
    configs = load_config()
    for source in configs:
        if not source.get("enabled", True):
            print(f"  Skipping {source['name']} (disabled)")
            continue
        print(f"  Scraping {source['name']}...")
        method = source.get("method", "http")
        if method == "playwright":
            jobs = scrape_playwright(source)
        else:
            jobs = scrape_http(source)
        print(f"    -> {len(jobs)} jobs found")
        all_jobs.extend(jobs)
    return all_jobs

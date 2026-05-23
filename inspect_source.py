"""Debug tool: inspect a URL and suggest selectors for job cards"""
import sys, json
from bs4 import BeautifulSoup
import requests
from playwright.sync_api import sync_playwright

def inspect_url(url, use_playwright=False):
    print(f"\nInspecting: {url}")
    print(f"{'='*60}")
    
    if use_playwright:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, wait_until="domcontentloaded", timeout=20000)
            html = page.content()
            # Print common job-related elements
            for sel in ["h2", "h3", "a[href*='job']", "[class*=job]", "[class*=card]", "[class*=result]", 
                        "[class*=listing]", "article", "[role='listitem']"]:
                els = page.query_selector_all(sel)
                if els:
                    print(f"\n  Selector '{sel}': {len(els)} elements")
                    for el in els[:5]:
                        text = (el.inner_text() or "").strip()[:80]
                        href = el.get_attribute("href") or ""
                        print(f"    '{text}' -> {href[:60]}")
            browser.close()
    else:
        resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=20)
        soup = BeautifulSoup(resp.text, "html.parser")
        for sel in ["h2", "h3", "a[href*='job']", "[class*=job]", "[class*=card]", "[class*=result]",
                    "article", "[role='listitem']", "li[class]", "div[class*=job]"]:
            els = soup.select(sel)
            if els:
                print(f"\n  Selector '{sel}': {len(els)} elements")
                for el in els[:5]:
                    text = el.get_text(strip=True)[:80]
                    href = ""
                    if el.name == "a":
                        href = el.get("href", "")[:60]
                    print(f"    '{text}' -> {href}")
    
    print(f"\n{'='*60}")
    print("Suggestions for sources_config.json:")
    print('  "card_selector": "div.job-card, article, li[class*=job]"')
    print('  "title": { "selector": "h2, h3, .title", "attribute": "innerText" }')
    print('  "company": { "selector": ".company, .employer", "attribute": "innerText" }')
    print('  "link": { "selector": "a[href]", "attribute": "href" }')

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python inspect_source.py <url> [--playwright]")
        print("Example: python inspect_source.py https://www.dice.com/jobs?q=golang --playwright")
    else:
        url = sys.argv[1]
        use_pw = "--playwright" in sys.argv
        inspect_url(url, use_pw)

from playwright.sync_api import sync_playwright
import os
from dotenv import load_dotenv
load_dotenv()

with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1280, "height": 800})
    
    # WTTJ login
    print("=== WTTJ Login ===")
    page.goto("https://app.welcometothejungle.com/auth/sign-in", wait_until="domcontentloaded", timeout=30000)
    page.wait_for_timeout(2000)
    page.fill("input[name='email']", os.environ.get("WTTJ_EMAIL", ""))
    page.fill("input[name='password']", os.environ.get("WTTJ_PASS", ""))
    page.click("button[type='submit']")
    page.wait_for_timeout(5000)
    
    print(f"URL after login: {page.url}")
    
    # Go to jobs search
    page.goto("https://app.welcometothejungle.com/jobs?query=golang", wait_until="domcontentloaded", timeout=30000)
    page.wait_for_timeout(3000)
    print(f"URL after search: {page.url}")
    
    # Print page content
    body = page.inner_text("body")[:2000]
    print(f"Body text: {body[:1000]}")
    
    # Find all job-like elements
    for sel in ["a[href*='/jobs/']", "[data-testid*='job']", "article", "div[class*=card]", "div[class*=job]", "li[class*=job]"]:
        els = page.query_selector_all(sel)
        print(f"  Selector '{sel}': {len(els)} elements")
        for el in els[:3]:
            text = (el.inner_text() or "")[:80]
            href = el.get_attribute("href") or ""
            print(f"    text='{text}' href='{href[:60]}'")
    
    browser.close()

"""Quick test of Playwright-based scraping"""
from playwright.sync_api import sync_playwright

try:
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://www.google.com", wait_until="domcontentloaded", timeout=15000)
        title = page.title()
        print(f"Playwright working! Page title: {title}")
        browser.close()
except Exception as e:
    print(f"Playwright error: {e}")
    print("Run: python -m playwright install chromium")

"""Debug WTTJ job search URL"""
from playwright.sync_api import sync_playwright

with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1920, "height": 1080})
    
    # Login
    print("Logging into WTTJ...")
    page.goto("https://app.welcometothejungle.com/auth/sign-in", wait_until="domcontentloaded", timeout=15000)
    page.fill("input[name='email']", "ronluke11652@gmail.com")
    page.fill("input[name='password']", "Sm@rtlee0208!!")
    page.click("button[type='submit']")
    page.wait_for_timeout(5000)
    print(f"After login URL: {page.url}")
    
    # Try the jobs URL again
    print("\nNavigating to jobs search...")
    page.goto("https://app.welcometothejungle.com/en/jobs", wait_until="domcontentloaded", timeout=15000)
    page.wait_for_timeout(3000)
    print(f"After navigate URL: {page.url}")
    print(f"Title: {page.title()}")
    
    # Screenshot for debugging
    page.screenshot(path="wttj.png")
    print("Screenshot saved to wttj.png")
    
    # Check what's on the page
    body = page.inner_text("body")
    print(f"\nBody text (first 500 chars): {body[:500]}")
    
    # Check all links
    links = page.query_selector_all("a")
    job_links = [l for l in links if l.get_attribute("href") and "job" in (l.get_attribute("href") or "").lower()]
    print(f"\nJob-related links: {len(job_links)}")
    for link in job_links[:10]:
        txt = (link.inner_text() or "").strip()[:60]
        href = link.get_attribute("href") or ""
        print(f"  '{txt}' -> {href[:100]}")

    # Check for any dynamic content containers
    containers = page.query_selector_all("div[class*='container'], main, section, [role='main']")
    print(f"\nMain containers: {len(containers)}")
    for c in containers[:5]:
        cls = c.get_attribute("class") or ""
        txt = (c.inner_text() or "").strip()[:100]
        if txt:
            print(f"  class='{cls}' txt='{txt}'")

    browser.close()

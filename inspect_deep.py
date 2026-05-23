"""Deep inspect WTTJ after login and BuiltIn login page"""
from playwright.sync_api import sync_playwright

with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1920, "height": 1080})

    # === WTTJ ===
    print("="*60)
    print("Welcome To The Jungle - Full job page after login")
    print("="*60)
    
    # Login
    page.goto("https://app.welcometothejungle.com/auth/sign-in", wait_until="domcontentloaded", timeout=15000)
    page.fill("input[name='email']", "ronluke11652@gmail.com")
    page.fill("input[name='password']", "Sm@rtlee0208!!")
    page.click("button[type='submit']")
    page.wait_for_timeout(3000)
    
    # Go to job search
    page.goto("https://app.welcometothejungle.com/en/jobs?query=golang&remote=remote", wait_until="domcontentloaded", timeout=15000)
    page.wait_for_timeout(3000)
    print(f"URL: {page.url[:150]}")
    print(f"Title: {page.title()[:100]}")
    
    # Scroll to load jobs
    for _ in range(5):
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(1000)
    
    # Check for job cards
    cards_selectors = [
        "a[data-testid='job-card']", "div[data-testid*='job']", "a[class*=card]",
        "article", "li[class*=job]", "div[class*=job-card]", "div[class*=search-result]",
        "a[href*='/en/jobs/']", "div[role='listitem']",
    ]
    for sel in cards_selectors:
        cards = page.query_selector_all(sel)
        if cards:
            print(f"\nSelector '{sel}': {len(cards)} cards found")
            for card in cards[:5]:
                inner = (card.inner_text() or "").strip()[:100]
                href = card.get_attribute("href") or ""
                if href:
                    print(f"  '{inner}' -> {href[:80]}")
                else:
                    print(f"  '{inner}'")
    
    # Get all links that look like job listings
    all_links = page.query_selector_all("a[href*='/en/jobs/']")
    print(f"\nAll links with '/en/jobs/': {len(all_links)}")
    for link in all_links[:10]:
        text = (link.inner_text() or "").strip()[:100]
        href = link.get_attribute("href") or ""
        if text and href and "?" not in href.split("/")[-1]:
            print(f"  '{text}' -> {href[:80]}")
    
    # === BuiltIn ===
    print(f"\n{'='*60}")
    print("BuiltIn - check login page structure")
    print("="*60)
    page.goto("https://builtin.com/login", wait_until="domcontentloaded", timeout=15000)
    print(f"Title: {page.title()[:100]}")
    
    # List all form fields
    inputs = page.query_selector_all("input")
    print(f"\nInput fields: {len(inputs)}")
    for inp in inputs:
        typ = inp.get_attribute("type") or ""
        name = inp.get_attribute("name") or ""
        pid = inp.get_attribute("id") or ""
        ph = inp.get_attribute("placeholder") or ""
        print(f"  type='{typ}' name='{name}' id='{pid}' placeholder='{ph}'")
    
    buttons = page.query_selector_all("button, a[role='button']")
    print(f"\nButtons: {len(buttons)}")
    for btn in buttons[:5]:
        txt = (btn.inner_text() or "").strip()[:60]
        cls = (btn.get_attribute("class") or "")[:60]
        print(f"  text='{txt}' class='{cls}'")

    # === Workable ===
    print(f"\n{'='*60}")
    print("Workable - check page structure")
    print("="*60)
    page.goto("https://jobs.workable.com/search?keywords=golang&remote=on", wait_until="domcontentloaded", timeout=15000)
    page.wait_for_timeout(2000)
    print(f"Title: {page.title()[:100]}")
    
    # Scroll
    for _ in range(3):
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(1000)
    
    # Find job cards
    for sel in ["article", "li[class*=job]", "div[class*=card]", "a[href*='/jobs/']",
                "div[role='listitem']", "section[class*=job]"]:
        els = page.query_selector_all(sel)
        if els:
            print(f"\nSelector '{sel}': {len(els)}")
            for el in els[:3]:
                text = (el.inner_text() or "").strip()[:80]
                print(f"  '{text}'")

    # === Greenhouse ===
    print(f"\n{'='*60}")
    print("Greenhouse - check what my.greenhouse.io is")
    print("="*60)
    page.goto("https://my.greenhouse.io/", wait_until="domcontentloaded", timeout=15000)
    print(f"Title: {page.title()[:100]}")
    body = (page.inner_text("body") or "")[:300]
    print(f"Body: {body}")
    
    # Greenhouse actual job search
    print("\nGreenhouse public job search alternative:")
    page.goto("https://boards.greenhouse.io/search?q=golang", wait_until="domcontentloaded", timeout=15000)
    print(f"URL: {page.url[:120]}")
    print(f"Title: {page.title()[:100]}")
    
    for sel in ["div[class*=job]", "li[class*=job]", "a[href*='/jobs/']", "section[class*=job]",
                "h2", "h3", "article"]:
        els = page.query_selector_all(sel)
        if els:
            print(f"\nSelector '{sel}': {len(els)}")
            for el in els[:5]:
                text = (el.inner_text() or "").strip()[:80]
                if text and len(text) > 15:
                    print(f"  '{text}'")

    browser.close()

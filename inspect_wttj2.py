"""Check WTTJ /jobs page and BuiltIn login page"""
from playwright.sync_api import sync_playwright

with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1920, "height": 1080})

    # === WTTJ Jobs Page ===
    print("="*60)
    print("WTTJ - Jobs page")
    print("="*60)
    page.goto("https://app.welcometothejungle.com/auth/sign-in", wait_until="domcontentloaded", timeout=15000)
    page.fill("input[name='email']", "ronluke11652@gmail.com")
    page.fill("input[name='password']", "Sm@rtlee0208!!")
    page.click("button[type='submit']")
    page.wait_for_timeout(3000)

    page.goto("https://app.welcometothejungle.com/jobs?query=golang&remote=remote", wait_until="domcontentloaded", timeout=15000)
    page.wait_for_timeout(3000)
    print(f"URL: {page.url[:150]}")
    print(f"Title: {page.title()[:100]}")

    for _ in range(5):
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(1000)

    # Find job cards
    for sel in ["a[href*='/jobs/']", "article", "div[class*=job]", "li[class*=job]",
                "div[data-testid*='job']", "[role='listitem']", "a[class*=card]"]:
        els = page.query_selector_all(sel)
        if els:
            print(f"\nSelector '{sel}': {len(els)}")
            for el in els[:5]:
                text = (el.inner_text() or "").strip()[:80]
                href = el.get_attribute("href") or ""
                print(f"  '{text}' -> {href[:80]}")

    body_text = page.inner_text("body")
    if "golang" in body_text.lower():
        print("\n*** 'golang' found in body! ***")

    # === BuiltIn ===
    print(f"\n{'='*60}")
    print("BuiltIn - check actual login mechanism")
    print("="*60)
    page.goto("https://builtin.com/login", wait_until="domcontentloaded", timeout=15000)
    page.wait_for_timeout(2000)
    print(f"URL: {page.url}")
    print(f"Title: {page.title()}")
    
    # Try to find iframe or shadow DOM
    frames = page.frames
    print(f"Frames: {len(frames)}")
    
    # Check for any interactive elements 
    body_html = page.content()
    if "email" in body_html.lower():
        print("'email' found in HTML source")
    if "password" in body_html.lower():
        print("'password' found in HTML source")

    # Look for any login form
    forms = page.query_selector_all("form")
    print(f"Forms: {len(forms)}")
    for form in forms:
        print(f"  form action={form.get_attribute('action')}")

    browser.close()
